package id.coffee521.pos;

import android.app.job.JobInfo;
import android.app.job.JobParameters;
import android.app.job.JobScheduler;
import android.app.job.JobService;
import android.content.ComponentName;
import android.content.Context;
import android.content.SharedPreferences;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

/**
 * Cek berkala (±15 menit, saat ada internet) apakah Owner menerbitkan promo/diskon/kabar/kegiatan baru.
 * Bila ada, kirim notifikasi sesuai pengaturan Owner (Atur → Notifikasi): aktif/tidak, untuk siapa, dan suaranya.
 * Tanpa Firebase: cukup server mini 521 yang sudah ada.
 */
public class KabarJob extends JobService {

    private static final int JOB_ID = 5210;
    private static final String PREF = "kabar";
    static volatile boolean foreground = false;

    static void schedule(Context c) {
        JobScheduler js = c.getSystemService(JobScheduler.class);
        if (js == null) return;
        for (JobInfo j : js.getAllPendingJobs()) if (j.getId() == JOB_ID) return;
        js.schedule(new JobInfo.Builder(JOB_ID, new ComponentName(c, KabarJob.class))
                .setRequiredNetworkType(JobInfo.NETWORK_TYPE_ANY)
                .setPeriodic(15 * 60 * 1000L)
                .setPersisted(true)
                .build());
    }

    static void setRole(Context c, String role) {
        if (!"owner".equals(role) && !"staf".equals(role)) role = "pelanggan";
        c.getSharedPreferences(PREF, MODE_PRIVATE).edit().putString("role", role).apply();
    }

    @Override
    public boolean onStartJob(JobParameters params) {
        new Thread(() -> {
            try { check(getApplicationContext()); } catch (Exception ignored) { }
            jobFinished(params, false);
        }).start();
        return true;
    }

    @Override
    public boolean onStopJob(JobParameters params) { return true; }

    /** Dipanggil oleh job berkala dan saat aplikasi dibuka. Aman dipanggil di thread latar belakang. */
    static synchronized void check(Context c) throws Exception {
        try { fetch(c); }
        finally { try { remind(c, readCache(c)); } catch (Exception ignored) { } }
    }

    /** Jenis notifikasi sebuah kabar: promo / diskon (promo berpotongan harga) / event / kabar. */
    private static String typeOf(JSONObject p) {
        String t = p.optString("type", "news");
        return "promo".equals(t) ? (p.optDouble("dval", 0) > 0 ? "diskon" : "promo") : "event".equals(t) ? "event" : "kabar";
    }

    /** Untuk siapa: "semua", "staf" (owner, admin, karyawan, reseller), "pelanggan". */
    private static boolean forMe(JSONObject tc, String role) {
        String to = tc != null ? tc.optString("to", "semua") : "semua";
        boolean cust = "pelanggan".equals(role);
        return "semua".equals(to) || ("staf".equals(to) && !cust) || ("pelanggan".equals(to) && cust);
    }

    private static void fetch(Context c) throws Exception {
        String server = MainActivity.readServer(c);
        if (server.isEmpty()) return;
        SharedPreferences sp = c.getSharedPreferences(PREF, MODE_PRIVATE);
        long rev = sp.getLong("rev", 0);
        HttpURLConnection h = (HttpURLConnection) new URL(server + "/k?since=" + rev).openConnection();
        h.setConnectTimeout(8000);
        h.setReadTimeout(15000);
        h.setInstanceFollowRedirects(false);
        String text;
        try {
            if (h.getResponseCode() != 200) return; // 204 = tidak ada perubahan
            try (InputStream in = h.getInputStream()) {
                ByteArrayOutputStream bo = new ByteArrayOutputStream();
                byte[] b = new byte[16384];
                int n, tot = 0;
                while ((n = in.read(b)) > 0) { tot += n; if (tot > 6_000_000) return; bo.write(b, 0, n); }
                text = new String(bo.toByteArray(), StandardCharsets.UTF_8);
            }
        } finally {
            h.disconnect();
        }
        JSONObject o = new JSONObject(text);
        long nrev = o.optLong("rev", 0);
        JSONObject k = o.optJSONObject("k");
        if (k == null || nrev <= rev) return;

        // Simpan data terbaru supaya aplikasi langsung tampil baru saat dibuka
        String body = "window.__KREV=" + nrev + ";window.__K=" + k.toString().replace("<", "\\u003c") + ";";
        File f = new File(c.getFilesDir(), "kdata.js"), tmp = new File(c.getFilesDir(), "kdata.js.job");
        try (OutputStream os = new FileOutputStream(tmp)) { os.write(body.getBytes(StandardCharsets.UTF_8)); }
        tmp.renameTo(f);

        JSONObject store = k.optJSONObject("store");
        if (store != null && store.optJSONArray("sounds") != null) {
            JSONArray ss = store.optJSONArray("sounds"), files = new JSONArray();
            for (int i = 0; i < ss.length(); i++) { JSONObject x = ss.optJSONObject(i); if (x != null) files.put(x.optString("f")); }
            MainActivity.syncSounds(c, files);
        }
        JSONObject cfg = store != null ? store.optJSONObject("notif") : null;
        if (cfg == null) cfg = new JSONObject();
        boolean notifyEdits = cfg.optInt("edit", 0) == 1;
        String role = sp.getString("role", "pelanggan");
        String name = store != null ? store.optString("name", "521 Coffee") : "521 Coffee";

        JSONObject known;
        try { known = new JSONObject(sp.getString("known", "{}")); } catch (Exception e) { known = new JSONObject(); }
        JSONObject seen;
        try { seen = new JSONObject(sp.getString("seen", "{}")); } catch (Exception e) { seen = new JSONObject(); }
        boolean first = !sp.getBoolean("init", false);
        JSONObject next = new JSONObject(), nseen = new JSONObject();
        List<String[]> out = new ArrayList<>(); // {type, title, body}
        String today = day(0);
        JSONArray keepPosts = new JSONArray();

        JSONArray posts = k.optJSONArray("posts");
        for (int i = 0; posts != null && i < posts.length(); i++) {
            JSONObject p = posts.optJSONObject(i);
            if (p == null || p.optBoolean("draft", false)) continue;
            String id = p.optString("id", "");
            if (id.isEmpty()) continue;
            String end = p.optString("end", ""), date = p.optString("date", "");
            String type = typeOf(p);
            nseen.put(id, seen.optString(id, today));
            if (!end.isEmpty() && end.compareTo(today) < 0) continue;            // promo sudah berakhir
            if ("event".equals(type) && !date.isEmpty() && date.compareTo(today) < 0) continue; // kegiatan sudah lewat
            JSONObject kp = new JSONObject();
            for (String f2 : new String[]{"id", "title", "body", "badge", "start", "end", "date"}) kp.put(f2, p.optString(f2, ""));
            kp.put("t", type);
            keepPosts.put(kp);
            String sig = String.valueOf((p.optString("title") + "|" + p.optString("body") + "|" + p.optString("badge") + "|"
                    + p.optString("dval") + "|" + p.optString("start") + "|" + end + "|" + date).hashCode());
            next.put(id, sig);
            if (first) continue;
            boolean isNew = !known.has(id), changed = !isNew && !sig.equals(known.optString(id));
            if (!isNew && !(changed && notifyEdits)) continue;
            JSONObject tc = cfg.optJSONObject(type);
            boolean on = tc == null || tc.optInt("on", 1) == 1;
            boolean now = tc == null || tc.optInt("now", 1) == 1;   // "Kirim langsung saat diterbitkan"
            if (!on || !now || !forMe(tc, role)) continue;
            String head;
            switch (type) {
                case "diskon": head = isNew ? "🏷️ Diskon: " : "✏️ Diskon diperbarui: "; break;
                case "promo": head = isNew ? "🎉 Promo baru: " : "✏️ Promo diperbarui: "; break;
                case "event": head = isNew ? "📅 Kegiatan: " : "✏️ Kegiatan diperbarui: "; break;
                default: head = isNew ? "📰 Kabar terbaru: " : "✏️ Kabar diperbarui: ";
            }
            out.add(new String[]{type, head + p.optString("title", ""), msg(p)});
        }

        // salinan ringkas untuk menghitung pengingat jam tanpa internet
        JSONObject cache = new JSONObject();
        cache.put("name", name);
        cache.put("notif", cfg);
        cache.put("posts", keepPosts);
        try (OutputStream os = new FileOutputStream(new File(c.getFilesDir(), "kabar_cache.json"))) { os.write(cache.toString().getBytes(StandardCharsets.UTF_8)); }

        sp.edit().putLong("rev", nrev).putString("known", next.toString()).putString("seen", nseen.toString()).putBoolean("init", true).apply();
        if (foreground || out.isEmpty()) return; // aplikasi sedang dibuka: tampil di aplikasi (tanda BARU & pemberitahuan)

        if (out.size() > 3) {
            String type = out.get(0)[0];
            JSONObject tc = cfg.optJSONObject(type);
            Notif.post(c, 5211, type, tc != null ? tc.optString("snd", "ceria") : "ceria",
                    "📣 Ada " + out.size() + " kabar & promo baru dari " + name, "Ketuk untuk melihat semuanya.", "kabar");
            return;
        }
        for (String[] m : out) {
            JSONObject tc = cfg.optJSONObject(m[0]);
            String snd = tc != null ? tc.optString("snd", defSound(m[0])) : defSound(m[0]);
            Notif.post(c, (m[1]).hashCode(), m[0], snd, m[1], m[2], "kabar");
        }
    }

    private static String msg(JSONObject p) {
        String badge = p.optString("badge", ""), txt = p.optString("body", "");
        String m = (badge.isEmpty() ? "" : badge + " · ") + txt;
        if (m.length() > 160) m = m.substring(0, 157) + "…";
        return m.isEmpty() ? "Buka aplikasi untuk melihat detailnya." : m;
    }

    private static String day(int plus) {
        java.util.Calendar cal = java.util.Calendar.getInstance();
        cal.add(java.util.Calendar.DATE, plus);
        return new SimpleDateFormat("yyyy-MM-dd", Locale.US).format(cal.getTime());
    }

    private static JSONObject readCache(Context c) {
        File f = new File(c.getFilesDir(), "kabar_cache.json");
        if (!f.isFile() || f.length() > 2_000_000) return null;
        try (InputStream in = new java.io.FileInputStream(f)) {
            ByteArrayOutputStream bo = new ByteArrayOutputStream();
            byte[] b = new byte[16384];
            int n;
            while ((n = in.read(b)) > 0) bo.write(b, 0, n);
            return new JSONObject(new String(bo.toByteArray(), StandardCharsets.UTF_8));
        } catch (Exception e) { return null; }
    }

    /** Masih berlaku pada hari "d"? Tanpa tanggal akhir: promo/diskon 7 hari, kegiatan 3 hari, kabar 2 hari sejak pertama terlihat. */
    private static boolean activeOn(JSONObject p, String d, String firstSeen) {
        String t = p.optString("t"), start = p.optString("start"), end = p.optString("end"), date = p.optString("date");
        if (!start.isEmpty() && start.compareTo(d) > 0) return false;
        String limit = "event".equals(t) && !date.isEmpty() ? date : end;
        if (!limit.isEmpty()) return limit.compareTo(d) >= 0;
        int max = "promo".equals(t) || "diskon".equals(t) ? 7 : "event".equals(t) ? 3 : 2;
        try {
            SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd", Locale.US);
            long diff = (fmt.parse(d).getTime() - fmt.parse(firstSeen).getTime()) / 86_400_000L;
            return diff >= 0 && diff < max;
        } catch (Exception e) { return false; }
    }

    /** Pengingat promo/diskon/kabar/kegiatan pada jam-jam pilihan Owner (Atur → Notifikasi), untuk hari ini & besok. */
    private static void remind(Context c, JSONObject cache) {
        JSONArray items = new JSONArray();
        if (cache != null) {
            SharedPreferences sp = c.getSharedPreferences(PREF, MODE_PRIVATE);
            String role = sp.getString("role", "pelanggan");
            JSONObject seen;
            try { seen = new JSONObject(sp.getString("seen", "{}")); } catch (Exception e) { seen = new JSONObject(); }
            JSONObject cfg = cache.optJSONObject("notif");
            JSONArray posts = cache.optJSONArray("posts");
            long now = System.currentTimeMillis();
            String[] types = {"promo", "diskon", "event", "kabar"};
            for (int dd = 0; dd < 2 && cfg != null && posts != null; dd++) {
                String d = day(dd);
                for (String type : types) {
                    JSONObject tc = cfg.optJSONObject(type);
                    JSONArray times = tc != null ? tc.optJSONArray("times") : null;
                    if (tc == null || tc.optInt("on", 1) != 1 || times == null || times.length() == 0 || !forMe(tc, role)) continue;
                    List<JSONObject> act = new ArrayList<>();
                    for (int i = 0; i < posts.length(); i++) {
                        JSONObject p = posts.optJSONObject(i);
                        if (p != null && type.equals(p.optString("t")) && activeOn(p, d, seen.optString(p.optString("id"), day(0)))) act.add(p);
                    }
                    if (act.isEmpty()) continue;
                    String title, body;
                    String label = "promo".equals(type) ? "promo" : "diskon".equals(type) ? "diskon" : "event".equals(type) ? "kegiatan" : "kabar";
                    String emo = "promo".equals(type) ? "🎉 " : "diskon".equals(type) ? "🏷️ " : "event".equals(type) ? "📅 " : "📰 ";
                    if (act.size() == 1) {
                        title = emo + ("event".equals(type) ? "Kegiatan: " : "kabar".equals(type) ? "Kabar: " : ("diskon".equals(type) ? "Diskon" : "Promo") + " hari ini: ") + act.get(0).optString("title");
                        body = msg(act.get(0));
                    } else {
                        title = emo + act.size() + " " + label + " berlaku hari ini dari " + cache.optString("name", "521 Coffee");
                        StringBuilder sb = new StringBuilder();
                        for (JSONObject p : act) { if (sb.length() > 0) sb.append(" · "); sb.append(p.optString("title")); }
                        body = sb.length() > 160 ? sb.substring(0, 157) + "…" : sb.toString();
                    }
                    for (int ti = 0; ti < times.length() && ti < 8; ti++) {
                        String tm = times.optString(ti, "");
                        if (!tm.matches("\\d{2}:\\d{2}")) continue;
                        try {
                            Date at = new SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.US).parse(d + " " + tm);
                            if (at == null || at.getTime() <= now) continue;
                            JSONObject it = new JSONObject();
                            it.put("id", "k-" + type + "-" + d + "-" + tm);
                            it.put("at", at.getTime());
                            it.put("type", type);
                            it.put("snd", tc.optString("snd", defSound(type)));
                            it.put("title", title);
                            it.put("body", body);
                            it.put("open", "kabar");
                            items.put(it);
                        } catch (Exception ignored) { }
                    }
                }
            }
        }
        AlertReceiver.setKabarItems(c, items);
    }

    private static String defSound(String type) {
        switch (type) {
            case "diskon": return "kaching";
            case "promo": return "ceria";
            case "kabar": return "lonceng";
            default: return "ding";
        }
    }
}
