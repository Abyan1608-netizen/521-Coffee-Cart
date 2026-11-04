package id.coffee521.pos;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.HashSet;
import java.util.Set;

/**
 * Pengingat produk jadi H-1 kedaluwarsa. Jadwal disimpan di SharedPreferences dan dipasang ke AlarmManager
 * (tidak butuh izin "exact alarm"). Dijadwalkan ulang otomatis setelah HP dinyalakan ulang / aplikasi diperbarui.
 */
public class AlertReceiver extends BroadcastReceiver {

    static final String ACTION_FIRE = "id.coffee521.pos.ALERT";
    private static final String PREF = "alerts", K_ITEMS = "items", K_KITEMS = "kitems", K_FIRED = "fired";
    private static final long GRACE = 36L * 3600_000L; // pengingat stok: lewat >36 jam tidak relevan lagi
    private static final long KGRACE = 45L * 60_000L;  // pengingat promo/kabar: hanya bila terlambat < 45 menit

    @Override
    public void onReceive(Context ctx, Intent intent) {
        String a = intent.getAction();
        try {
            if (ACTION_FIRE.equals(a)) {
                fireDue(ctx);
            } else if (Intent.ACTION_BOOT_COMPLETED.equals(a) || Intent.ACTION_MY_PACKAGE_REPLACED.equals(a)) {
                scheduleAll(ctx);
                fireDue(ctx);
                if (!MainActivity.readServer(ctx).isEmpty()) KabarJob.schedule(ctx);
            }
        } catch (RuntimeException ignored) { } // pengingat gagal tidak boleh membuat aplikasi berhenti
    }

    /** Pengingat stok dari aplikasi (Stok → Produk jadi & bahan baku). Mengganti seluruh daftar stok. */
    static void setItems(Context ctx, JSONArray items) { store(ctx, K_ITEMS, items, 200); }

    /** Pengingat promo/diskon/kabar/kegiatan pada jam pilihan Owner (dihitung KabarJob). Mengganti seluruh daftar kabar. */
    static void setKabarItems(Context ctx, JSONArray items) { store(ctx, K_KITEMS, items, 120); }

    private static synchronized void store(Context ctx, String key, JSONArray items, int max) {
        SharedPreferences sp = ctx.getSharedPreferences(PREF, Context.MODE_PRIVATE);
        cancelList(ctx, load(sp, key));
        JSONArray clean = new JSONArray();
        Set<String> keep = new HashSet<>();
        for (int i = 0; i < items.length() && clean.length() < max; i++) {
            JSONObject o = items.optJSONObject(i);
            if (o == null) continue;
            String id = o.optString("id", "");
            long at = o.optLong("at", 0);
            if (id.isEmpty() || id.length() > 80 || at <= 0) continue;
            try {
                JSONObject c = new JSONObject();
                c.put("id", id);
                c.put("at", at);
                c.put("title", trim(o.optString("title", ""), 80));
                c.put("body", trim(o.optString("body", ""), 300));
                c.put("type", Notif.cleanType(o.optString("type", "exp")));
                c.put("snd", Notif.cleanSound(o.optString("snd", "ding")));
                c.put("open", "kabar".equals(o.optString("open")) ? "kabar" : "stok");
                clean.put(c);
                keep.add(id);
            } catch (Exception ignored) { }
        }
        // catatan "sudah dikirim" hanya disimpan untuk jadwal yang masih ada (di kedua daftar)
        JSONArray other = load(sp, K_ITEMS.equals(key) ? K_KITEMS : K_ITEMS);
        for (int i = 0; i < other.length(); i++) { JSONObject o = other.optJSONObject(i); if (o != null) keep.add(o.optString("id")); }
        Set<String> fired = new HashSet<>(sp.getStringSet(K_FIRED, new HashSet<>()));
        fired.retainAll(keep);
        sp.edit().putString(key, clean.toString()).putStringSet(K_FIRED, fired).apply();
        scheduleAll(ctx);
        fireDue(ctx);
    }

    private static String trim(String s, int n) { return s.length() > n ? s.substring(0, n) : s; }

    private static JSONArray load(SharedPreferences sp, String key) {
        try { return new JSONArray(sp.getString(key, "[]")); } catch (Exception e) { return new JSONArray(); }
    }

    private static PendingIntent pi(Context ctx, int code) {
        Intent i = new Intent(ctx, AlertReceiver.class).setAction(ACTION_FIRE);
        return PendingIntent.getBroadcast(ctx, code, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    private static void cancelList(Context ctx, JSONArray it) {
        AlarmManager am = (AlarmManager) ctx.getSystemService(Context.ALARM_SERVICE);
        if (am == null) return;
        for (int i = 0; i < it.length(); i++) {
            JSONObject o = it.optJSONObject(i);
            if (o != null) am.cancel(pi(ctx, o.optString("id").hashCode()));
        }
    }

    static void scheduleAll(Context ctx) {
        SharedPreferences sp = ctx.getSharedPreferences(PREF, Context.MODE_PRIVATE);
        AlarmManager am = (AlarmManager) ctx.getSystemService(Context.ALARM_SERVICE);
        if (am == null) return;
        long now = System.currentTimeMillis();
        for (String key : new String[]{K_ITEMS, K_KITEMS}) {
            JSONArray it = load(sp, key);
            for (int i = 0; i < it.length(); i++) {
                JSONObject o = it.optJSONObject(i);
                if (o == null) continue;
                long at = o.optLong("at");
                if (at > now) am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, at, pi(ctx, o.optString("id").hashCode()));
            }
        }
    }

    /** Kirim notifikasi untuk jadwal yang sudah lewat waktunya dan belum pernah dikirim. */
    static synchronized void fireDue(Context ctx) {
        SharedPreferences sp = ctx.getSharedPreferences(PREF, Context.MODE_PRIVATE);
        Set<String> fired = new HashSet<>(sp.getStringSet(K_FIRED, new HashSet<>()));
        long now = System.currentTimeMillis();
        boolean changed = false;
        for (String key : new String[]{K_ITEMS, K_KITEMS}) {
            long grace = K_KITEMS.equals(key) ? KGRACE : GRACE;
            JSONArray it = load(sp, key);
            for (int i = 0; i < it.length(); i++) {
                JSONObject o = it.optJSONObject(i);
                if (o == null) continue;
                String id = o.optString("id");
                long at = o.optLong("at");
                if (at <= now && now - at < grace && !fired.contains(id)) {
                    if (Notif.post(ctx, id.hashCode(), o.optString("type", "exp"), o.optString("snd", "ding"), o.optString("title"), o.optString("body"),
                            "kabar".equals(o.optString("open")) ? "kabar" : "stok")) {
                        fired.add(id);
                        changed = true;
                    }
                }
            }
        }
        if (changed) sp.edit().putStringSet(K_FIRED, fired).apply();
    }

}
