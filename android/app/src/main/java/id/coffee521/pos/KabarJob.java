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
        boolean first = !sp.getBoolean("init", false);
        JSONObject next = new JSONObject();
        List<String[]> out = new ArrayList<>(); // {type, title, body}
        String today = new SimpleDateFormat("yyyy-MM-dd", Locale.US).format(new Date());

        JSONArray posts = k.optJSONArray("posts");
        for (int i = 0; posts != null && i < posts.length(); i++) {
            JSONObject p = posts.optJSONObject(i);
            if (p == null || p.optBoolean("draft", false)) continue;
            String id = p.optString("id", ""), t = p.optString("type", "news");
            if (id.isEmpty()) continue;
            String end = p.optString("end", ""), date = p.optString("date", "");
            if (!end.isEmpty() && end.compareTo(today) < 0) continue;            // promo sudah berakhir
            if ("event".equals(t) && !date.isEmpty() && date.compareTo(today) < 0) continue; // kegiatan sudah lewat
            String type = "promo".equals(t) ? (p.optDouble("dval", 0) > 0 ? "diskon" : "promo") : "event".equals(t) ? "event" : "kabar";
            String sig = String.valueOf((p.optString("title") + "|" + p.optString("body") + "|" + p.optString("badge") + "|"
                    + p.optString("dval") + "|" + p.optString("start") + "|" + end + "|" + date).hashCode());
            next.put(id, sig);
            if (first) continue;
            boolean isNew = !known.has(id), changed = !isNew && !sig.equals(known.optString(id));
            if (!isNew && !(changed && notifyEdits)) continue;
            JSONObject tc = cfg.optJSONObject(type);
            boolean on = tc == null || tc.optInt("on", 1) == 1;
            String to = tc != null ? tc.optString("to", "semua") : "semua";
            boolean forMe = "semua".equals(to) || ("staf".equals(to) && !"pelanggan".equals(role)) || ("pelanggan".equals(to) && "pelanggan".equals(role));
            if (!on || !forMe || "owner".equals(role)) continue;
            String head;
            switch (type) {
                case "diskon": head = isNew ? "🏷️ Diskon: " : "✏️ Diskon diperbarui: "; break;
                case "promo": head = isNew ? "🎉 Promo baru: " : "✏️ Promo diperbarui: "; break;
                case "event": head = isNew ? "📅 Kegiatan: " : "✏️ Kegiatan diperbarui: "; break;
                default: head = isNew ? "📰 Kabar terbaru: " : "✏️ Kabar diperbarui: ";
            }
            String badge = p.optString("badge", ""), txt = p.optString("body", "");
            String msg = (badge.isEmpty() ? "" : badge + " · ") + txt;
            if (msg.length() > 160) msg = msg.substring(0, 157) + "…";
            out.add(new String[]{type, head + p.optString("title", ""), msg.isEmpty() ? "Buka aplikasi untuk melihat detailnya." : msg});
        }

        sp.edit().putLong("rev", nrev).putString("known", next.toString()).putBoolean("init", true).apply();
        if (foreground || out.isEmpty()) return; // aplikasi sedang dibuka: tampil sebagai tanda BARU di halaman Kabar

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

    private static String defSound(String type) {
        switch (type) {
            case "diskon": return "kaching";
            case "promo": return "ceria";
            case "kabar": return "lonceng";
            default: return "ding";
        }
    }
}
