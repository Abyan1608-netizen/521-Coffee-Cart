package id.coffee521.pos;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.AudioAttributes;
import android.media.MediaPlayer;
import android.media.Ringtone;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Build;
import android.provider.Settings;

/**
 * Notifikasi 521: satu kanal per jenis + suara (di Android 8+ suara melekat pada kanal),
 * sehingga Owner bisa memilih suara berbeda untuk promo, diskon, kabar, pengingat stok, dll.
 */
final class Notif {
    private Notif() { }

    static final String[] TYPES = {"exp", "low", "promo", "diskon", "kabar", "event"};
    private static final String[] SOUNDS = {"ding", "lonceng", "kaching", "ceria", "lembut", "bawaan", "senyap"};

    static String typeName(Context c, String type) {
        switch (type) {
            case "exp": return "Produk hampir kedaluwarsa";
            case "low": return "Stok bahan menipis";
            case "promo": return "Promo baru";
            case "diskon": return "Diskon";
            case "kabar": return "Kabar terbaru";
            case "event": return "Kegiatan";
            default: return "Pengingat 521";
        }
    }

    static String cleanType(String t) {
        for (String x : TYPES) if (x.equals(t)) return t;
        return "exp";
    }

    static String cleanSound(String s) {
        for (String x : SOUNDS) if (x.equals(s)) return s;
        if (s != null && s.startsWith("c:") && SoundProvider.NAME.matcher(s.substring(2)).matches()) return s;
        return "bawaan";
    }

    /** Suara impor tersedia di HP ini? (bila belum terunduh, pakai suara bawaan sementara) */
    static String usable(Context c, String snd) {
        snd = cleanSound(snd);
        if (snd.startsWith("c:") && !SoundProvider.file(c, snd.substring(2)).isFile()) return "bawaan";
        return snd;
    }

    static Uri soundUri(Context c, String snd) {
        if ("senyap".equals(snd)) return null;
        if ("bawaan".equals(snd)) return Settings.System.DEFAULT_NOTIFICATION_URI;
        if (snd.startsWith("c:")) {
            Uri u = SoundProvider.uri(c, snd.substring(2));
            try { c.grantUriPermission("com.android.systemui", u, Intent.FLAG_GRANT_READ_URI_PERMISSION); } catch (Exception ignored) { }
            return u;
        }
        return Uri.parse("android.resource://" + c.getPackageName() + "/raw/snd_" + snd);
    }

    /** Kanal "n_<jenis>_<suara>"; kanal lama jenis yang sama dengan suara lain dihapus supaya Pengaturan HP tetap rapi. */
    static String channel(Context c, String type, String snd) {
        type = cleanType(type);
        snd = usable(c, snd);
        String id = "n_" + type + "_" + (snd.startsWith("c:") ? "c" + snd.substring(2, 12) : snd);
        NotificationManager nm = c.getSystemService(NotificationManager.class);
        if (nm == null) return id;
        if (nm.getNotificationChannel(id) == null) {
            for (NotificationChannel ch : nm.getNotificationChannels()) {
                String cid = ch.getId();
                if (cid.startsWith("n_" + type + "_") || cid.equals("expiry")) nm.deleteNotificationChannel(cid);
            }
            NotificationChannel ch = new NotificationChannel(id, typeName(c, type),
                    "senyap".equals(snd) ? NotificationManager.IMPORTANCE_DEFAULT : NotificationManager.IMPORTANCE_HIGH);
            ch.setDescription("Notifikasi 521 Coffee App: " + typeName(c, type));
            Uri u = soundUri(c, snd);
            if (u == null) {
                ch.setSound(null, null);
            } else {
                ch.setSound(u, new AudioAttributes.Builder()
                        .setUsage(AudioAttributes.USAGE_NOTIFICATION)
                        .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION).build());
            }
            nm.createNotificationChannel(ch);
        }
        return id;
    }

    static boolean allowed(Context c) {
        return Build.VERSION.SDK_INT < 33
                || c.checkSelfPermission(android.Manifest.permission.POST_NOTIFICATIONS) == PackageManager.PERMISSION_GRANTED;
    }

    static boolean post(Context c, int nid, String type, String snd, String title, String body, String open) {
        if (!allowed(c)) return false;
        NotificationManager nm = c.getSystemService(NotificationManager.class);
        if (nm == null) return false;
        String ch = channel(c, type, snd);
        Intent i = new Intent(c, MainActivity.class).setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP)
                .putExtra("open", open);
        PendingIntent pi = PendingIntent.getActivity(c, nid, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        Notification n = new Notification.Builder(c, ch)
                .setSmallIcon(R.drawable.ic_stat_521)
                .setColor(0xFFC03200)
                .setContentTitle(title)
                .setContentText(body)
                .setStyle(new Notification.BigTextStyle().bigText(body))
                .setCategory("exp".equals(type) || "low".equals(type) ? Notification.CATEGORY_REMINDER : Notification.CATEGORY_PROMO)
                .setAutoCancel(true)
                .setContentIntent(pi)
                .build();
        nm.notify(nid, n);
        return true;
    }

    private static MediaPlayer player;

    /** Pratinjau suara di halaman Atur → Notifikasi. */
    static void play(Context c, String snd) {
        snd = cleanSound(snd);
        if ("senyap".equals(snd)) return;
        try {
            if (snd.startsWith("c:")) {
                java.io.File f = SoundProvider.file(c, snd.substring(2));
                if (!f.isFile()) return;
                if (player != null) { player.release(); player = null; }
                player = new MediaPlayer();
                player.setDataSource(f.getAbsolutePath());
                player.setOnCompletionListener(mp -> { mp.release(); if (player == mp) player = null; });
                player.prepare();
                player.start();
                return;
            }
            if ("bawaan".equals(snd)) {
                Ringtone r = RingtoneManager.getRingtone(c, Settings.System.DEFAULT_NOTIFICATION_URI);
                if (r != null) r.play();
                return;
            }
            int res = c.getResources().getIdentifier("snd_" + snd, "raw", c.getPackageName());
            if (res == 0) return;
            if (player != null) { player.release(); player = null; }
            player = MediaPlayer.create(c, res);
            if (player == null) return;
            player.setOnCompletionListener(mp -> { mp.release(); if (player == mp) player = null; });
            player.start();
        } catch (Exception ignored) { }
    }
}
