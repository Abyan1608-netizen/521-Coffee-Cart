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
    private static final String PREF = "alerts", K_ITEMS = "items", K_FIRED = "fired";
    private static final long GRACE = 36L * 3600_000L; // lewat >36 jam: tidak relevan lagi

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

    /** Ganti seluruh jadwal dengan daftar baru dari aplikasi. */
    static void setItems(Context ctx, JSONArray items) {
        SharedPreferences sp = ctx.getSharedPreferences(PREF, Context.MODE_PRIVATE);
        cancelAll(ctx, sp);
        JSONArray clean = new JSONArray();
        Set<String> keep = new HashSet<>();
        for (int i = 0; i < items.length() && i < 200; i++) {
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
                clean.put(c);
                keep.add(id);
            } catch (Exception ignored) { }
        }
        // Buang catatan "sudah dikirim" untuk batch yang sudah tidak ada
        Set<String> fired = new HashSet<>(sp.getStringSet(K_FIRED, new HashSet<>()));
        fired.retainAll(keep);
        sp.edit().putString(K_ITEMS, clean.toString()).putStringSet(K_FIRED, fired).apply();
        scheduleAll(ctx);
        fireDue(ctx);
    }

    private static String trim(String s, int n) { return s.length() > n ? s.substring(0, n) : s; }

    private static JSONArray load(SharedPreferences sp) {
        try { return new JSONArray(sp.getString(K_ITEMS, "[]")); } catch (Exception e) { return new JSONArray(); }
    }

    private static PendingIntent pi(Context ctx, int code) {
        Intent i = new Intent(ctx, AlertReceiver.class).setAction(ACTION_FIRE);
        return PendingIntent.getBroadcast(ctx, code, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    private static void cancelAll(Context ctx, SharedPreferences sp) {
        AlarmManager am = (AlarmManager) ctx.getSystemService(Context.ALARM_SERVICE);
        JSONArray it = load(sp);
        for (int i = 0; i < it.length(); i++) {
            JSONObject o = it.optJSONObject(i);
            if (o != null && am != null) am.cancel(pi(ctx, o.optString("id").hashCode()));
        }
    }

    static void scheduleAll(Context ctx) {
        SharedPreferences sp = ctx.getSharedPreferences(PREF, Context.MODE_PRIVATE);
        AlarmManager am = (AlarmManager) ctx.getSystemService(Context.ALARM_SERVICE);
        if (am == null) return;
        long now = System.currentTimeMillis();
        JSONArray it = load(sp);
        for (int i = 0; i < it.length(); i++) {
            JSONObject o = it.optJSONObject(i);
            if (o == null) continue;
            long at = o.optLong("at");
            if (at > now) am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, at, pi(ctx, o.optString("id").hashCode()));
        }
    }

    /** Kirim notifikasi untuk jadwal yang sudah lewat waktunya dan belum pernah dikirim. */
    static void fireDue(Context ctx) {
        SharedPreferences sp = ctx.getSharedPreferences(PREF, Context.MODE_PRIVATE);
        Set<String> fired = new HashSet<>(sp.getStringSet(K_FIRED, new HashSet<>()));
        long now = System.currentTimeMillis();
        JSONArray it = load(sp);
        boolean changed = false;
        for (int i = 0; i < it.length(); i++) {
            JSONObject o = it.optJSONObject(i);
            if (o == null) continue;
            String id = o.optString("id");
            long at = o.optLong("at");
            if (at <= now && now - at < GRACE && !fired.contains(id)) {
                if (Notif.post(ctx, id.hashCode(), o.optString("type", "exp"), o.optString("snd", "ding"), o.optString("title"), o.optString("body"), "stok")) {
                    fired.add(id);
                    changed = true;
                }
            }
        }
        if (changed) sp.edit().putStringSet(K_FIRED, fired).apply();
    }

}
