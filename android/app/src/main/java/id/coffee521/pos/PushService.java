package id.coffee521.pos;

import android.content.Context;

import com.google.firebase.FirebaseApp;
import com.google.firebase.messaging.FirebaseMessaging;
import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

/**
 * Notifikasi instan (Firebase Cloud Messaging).
 * Server 521 hanya mengirim "colekan" ke topik k521 saat Owner menambah/mengubah promo, diskon, kabar, atau kegiatan.
 * HP lalu mengambil data terbaru dan menampilkan notifikasinya sendiri (aturan penerima, suara, & jam tetap dari Atur → Notifikasi).
 * Tanpa konfigurasi Firebase (android-web/config.json → "fcm"), kelas ini tidak aktif dan cek berkala tetap berjalan.
 */
public class PushService extends FirebaseMessagingService {

    static final String TOPIC = "k521";

    @Override
    public void onMessageReceived(RemoteMessage m) {
        try { KabarJob.check(getApplicationContext()); } catch (Exception ignored) { }
    }

    @Override
    public void onNewToken(String token) { subscribe(getApplicationContext()); }

    /** Daftarkan HP ini ke topik kabar 521 (aman dipanggil berkali-kali). */
    static void subscribe(Context c) {
        try {
            if (!configured(c)) return;
            FirebaseMessaging.getInstance().subscribeToTopic(TOPIC).addOnCompleteListener(t ->
                    c.getSharedPreferences("kabar", MODE_PRIVATE).edit().putBoolean("push", t.isSuccessful()).apply());
        } catch (Throwable ignored) { }
    }

    static boolean configured(Context c) {
        try { return !FirebaseApp.getApps(c).isEmpty(); } catch (Throwable t) { return false; }
    }
}
