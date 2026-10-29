package id.coffee521.pos;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.database.Cursor;
import android.net.Uri;
import android.os.ParcelFileDescriptor;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.regex.Pattern;

/**
 * Menyajikan suara notifikasi hasil impor (hanya baca) supaya sistem Android bisa memutarnya
 * sebagai suara kanal notifikasi. Hanya file suara bernama hash di folder media aplikasi yang bisa dibuka.
 */
public class SoundProvider extends ContentProvider {

    static final Pattern NAME = Pattern.compile("^[a-f0-9]{32}\\.(mp3|ogg|m4a|aac|wav)$");

    static Uri uri(android.content.Context c, String file) {
        return Uri.parse("content://" + c.getPackageName() + ".sounds/" + file);
    }

    static File file(android.content.Context c, String name) {
        return new File(new File(c.getFilesDir(), "media"), name);
    }

    @Override public boolean onCreate() { return true; }

    @Override
    public ParcelFileDescriptor openFile(Uri uri, String mode) throws FileNotFoundException {
        if (mode == null || !mode.startsWith("r") || mode.contains("w")) throw new FileNotFoundException("read-only");
        String name = uri.getLastPathSegment();
        if (name == null || !NAME.matcher(name).matches() || getContext() == null) throw new FileNotFoundException();
        File f = file(getContext(), name);
        if (!f.isFile()) throw new FileNotFoundException();
        return ParcelFileDescriptor.open(f, ParcelFileDescriptor.MODE_READ_ONLY);
    }

    @Override
    public String getType(Uri uri) {
        String n = String.valueOf(uri.getLastPathSegment());
        if (n.endsWith(".mp3")) return "audio/mpeg";
        if (n.endsWith(".ogg")) return "audio/ogg";
        if (n.endsWith(".m4a")) return "audio/mp4";
        if (n.endsWith(".aac")) return "audio/aac";
        if (n.endsWith(".wav")) return "audio/wav";
        return null;
    }

    @Override public Cursor query(Uri u, String[] p, String s, String[] a, String o) { return null; }
    @Override public Uri insert(Uri u, ContentValues v) { return null; }
    @Override public int delete(Uri u, String s, String[] a) { return 0; }
    @Override public int update(Uri u, ContentValues v, String s, String[] a) { return 0; }
}
