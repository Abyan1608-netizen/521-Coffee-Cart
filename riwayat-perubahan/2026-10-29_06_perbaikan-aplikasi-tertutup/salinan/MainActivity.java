package id.coffee521.pos;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Insets;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.view.Window;
import android.view.WindowInsets;
import android.view.WindowInsetsController;
import android.webkit.JavascriptInterface;
import android.webkit.RenderProcessGoneDetail;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.Toast;
import android.window.OnBackInvokedDispatcher;

import androidx.webkit.WebViewAssetLoader;
import androidx.webkit.WebViewCompat;
import androidx.webkit.WebViewFeature;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.regex.Pattern;

/**
 * 521 Coffee App — satu Activity + WebView, tanpa AppCompat/Kotlin supaya APK sekecil mungkin.
 * Konten web dimuat dari aset aplikasi lewat https://appassets.androidplatform.net (origin aman, tanpa akses file://).
 */
public class MainActivity extends Activity {

    private static final String HOST = "appassets.androidplatform.net";
    private static final String ORIGIN = "https://" + HOST;
    private static final String START_URL = ORIGIN + "/app/index.html";
    private static final Pattern SAFE_PATH = Pattern.compile("^[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*$");
    private static final Pattern MEDIA_NAME = Pattern.compile("^[a-f0-9]{8,64}\\.(jpg|png|webp|gif|avif)$");
    private static final int REQ_FILE = 11, REQ_SAVE = 12, REQ_NOTIF = 13;
    private static final int MAX_MEDIA = 12 * 1024 * 1024, MAX_K = 8 * 1024 * 1024;

    private final Handler main = new Handler(Looper.getMainLooper());
    private WebView web;
    private FrameLayout root;
    private String server = "";
    private ValueCallback<Uri[]> fileCb;
    private String pendingSaveData;
    private Reply pendingSaveReply;

    interface Reply { void send(String json); }

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        server = readServer();

        root = new FrameLayout(this);
        root.setBackgroundColor(0xFF120504);
        web = new WebView(this);
        web.setBackgroundColor(0xFF120504);
        root.addView(web, new FrameLayout.LayoutParams(-1, -1));
        setContentView(root);
        setupInsets();

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);
        s.setSupportMultipleWindows(false);
        s.setJavaScriptCanOpenWindowsAutomatically(false);
        s.setMediaPlaybackRequiresUserGesture(true);
        s.setGeolocationEnabled(false);
        s.setSaveFormData(false);
        s.setTextZoom(100); // tata letak kasir dirancang presisi
        s.setSafeBrowsingEnabled(true);
        s.setOffscreenPreRaster(false);
        WebView.setWebContentsDebuggingEnabled(BuildConfig.DEBUG);

        final WebViewAssetLoader loader = new WebViewAssetLoader.Builder()
                .setDomain(HOST)
                .addPathHandler("/app/", this::serve)
                .build();

        web.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView v, WebResourceRequest r) {
                return loader.shouldInterceptRequest(r.getUrl());
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r) {
                Uri u = r.getUrl();
                if (HOST.equals(u.getHost()) && "https".equals(u.getScheme())) return false;
                openExternal(u.toString());
                return true;
            }

            @Override
            public void onPageFinished(WebView v, String url) {
                runPendingOpen();
            }

            @Override
            public boolean onRenderProcessGone(WebView v, RenderProcessGoneDetail d) {
                // Mesin WebView berhenti (mis. memori penuh): buat ulang tampilan, data tetap aman di penyimpanan.
                recreate();
                return true;
            }
        });

        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView v, ValueCallback<Uri[]> cb, FileChooserParams p) {
                if (fileCb != null) fileCb.onReceiveValue(null);
                fileCb = cb;
                boolean images = true;
                for (String t : p.getAcceptTypes()) if (t != null && !t.isEmpty() && !t.startsWith("image")) images = false;
                Intent i = new Intent(Intent.ACTION_GET_CONTENT);
                i.addCategory(Intent.CATEGORY_OPENABLE);
                i.setType(images ? "image/*" : "*/*");
                if (p.getMode() == FileChooserParams.MODE_OPEN_MULTIPLE) i.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
                try {
                    startActivityForResult(Intent.createChooser(i, null), REQ_FILE);
                } catch (ActivityNotFoundException e) {
                    fileCb = null;
                    return false;
                }
                return true;
            }
        });

        installBridge();
        setupBack();
        pendingOpen = getIntent() != null ? getIntent().getStringExtra("open") : null;
        // cek promo/kabar baru berkala untuk notifikasi; fitur tambahan tidak boleh membuat aplikasi tertutup
        if (!server.isEmpty()) {
            try { KabarJob.schedule(this); } catch (RuntimeException ignored) { }
        }

        if (state != null) web.restoreState(state);
        if (web.getUrl() == null) web.loadUrl(START_URL);
    }

    // ---------- Penyajian file: aset bawaan, data Kabar terbaru, dan cache foto dari server ----------

    private WebResourceResponse serve(String path) {
        try {
            if (!SAFE_PATH.matcher(path).matches()) return notFound();
            if (path.equals("kdata.js")) {
                File f = new File(getFilesDir(), "kdata.js");
                if (f.isFile()) return resp("kdata.js", new FileInputStream(f));
            }
            if (path.startsWith("media/")) {
                String name = path.substring(6);
                File dir = new File(getFilesDir(), "media");
                File f = new File(dir, name);
                if (f.isFile()) return resp(name, new FileInputStream(f));
                try {
                    return resp(name, getAssets().open("www/" + path));
                } catch (IOException ignored) { }
                if (!server.isEmpty() && MEDIA_NAME.matcher(name).matches()) {
                    byte[] b = download(server + "/media/" + name, MAX_MEDIA);
                    if (b != null) {
                        dir.mkdirs();
                        File tmp = new File(dir, name + ".tmp");
                        try (OutputStream o = new FileOutputStream(tmp)) { o.write(b); }
                        tmp.renameTo(f);
                        return resp(name, new java.io.ByteArrayInputStream(b));
                    }
                }
                return notFound();
            }
            return resp(path, getAssets().open("www/" + path));
        } catch (IOException e) {
            return notFound();
        }
    }

    private static WebResourceResponse resp(String name, InputStream in) {
        String n = name.toLowerCase(Locale.ROOT), mime = "application/octet-stream", enc = null;
        if (n.endsWith(".html")) { mime = "text/html"; enc = "utf-8"; }
        else if (n.endsWith(".js")) { mime = "text/javascript"; enc = "utf-8"; }
        else if (n.endsWith(".css")) { mime = "text/css"; enc = "utf-8"; }
        else if (n.endsWith(".json")) { mime = "application/json"; enc = "utf-8"; }
        else if (n.endsWith(".jpg") || n.endsWith(".jpeg")) mime = "image/jpeg";
        else if (n.endsWith(".png")) mime = "image/png";
        else if (n.endsWith(".webp")) mime = "image/webp";
        else if (n.endsWith(".gif")) mime = "image/gif";
        else if (n.endsWith(".avif")) mime = "image/avif";
        else if (n.endsWith(".woff")) mime = "font/woff";
        else if (n.endsWith(".woff2")) mime = "font/woff2";
        else if (n.endsWith(".svg")) mime = "image/svg+xml";
        Map<String, String> h = new HashMap<>();
        h.put("X-Content-Type-Options", "nosniff");
        h.put("Referrer-Policy", "no-referrer");
        h.put("Cache-Control", n.startsWith("kdata") || n.endsWith(".html") ? "no-cache" : "max-age=31536000");
        return new WebResourceResponse(mime, enc, 200, "OK", h, in);
    }

    private static WebResourceResponse notFound() {
        return new WebResourceResponse("text/plain", "utf-8", 404, "Not Found", Collections.emptyMap(), null);
    }

    private static byte[] download(String url, int max) {
        HttpURLConnection c = null;
        try {
            c = (HttpURLConnection) new URL(url).openConnection();
            c.setConnectTimeout(8000);
            c.setReadTimeout(15000);
            c.setInstanceFollowRedirects(false);
            if (c.getResponseCode() != 200) return null;
            String ct = String.valueOf(c.getContentType());
            if (!ct.startsWith("image/")) return null;
            try (InputStream in = c.getInputStream()) {
                ByteArrayOutputStream bo = new ByteArrayOutputStream();
                byte[] buf = new byte[16384];
                int n, tot = 0;
                while ((n = in.read(buf)) > 0) {
                    tot += n;
                    if (tot > max) return null;
                    bo.write(buf, 0, n);
                }
                return bo.toByteArray();
            }
        } catch (IOException e) {
            return null;
        } finally {
            if (c != null) c.disconnect();
        }
    }

    private String readServer() { return readServer(this); }

    static String readServer(Context c) {
        try (InputStream in = c.getAssets().open("www/a521.json")) {
            String s = new JSONObject(new String(readAll(in), StandardCharsets.UTF_8)).optString("server", "");
            return s.startsWith("https://") ? s.replaceAll("/+$", "") : "";
        } catch (Exception e) {
            return "";
        }
    }

    private static byte[] readAll(InputStream in) throws IOException {
        ByteArrayOutputStream bo = new ByteArrayOutputStream();
        byte[] b = new byte[8192];
        int n;
        while ((n = in.read(b)) > 0) bo.write(b, 0, n);
        return bo.toByteArray();
    }

    // ---------- Jembatan JS <-> Android ----------

    private void installBridge() {
        if (WebViewFeature.isFeatureSupported(WebViewFeature.WEB_MESSAGE_LISTENER)) {
            // Hanya halaman dari origin aplikasi sendiri yang bisa memanggil jembatan.
            WebViewCompat.addWebMessageListener(web, "A521Native", Collections.singleton(ORIGIN),
                    (view, msg, origin, isMainFrame, proxy) -> {
                        if (!isMainFrame || msg.getData() == null) return;
                        handle(msg.getData(), json -> main.post(() -> proxy.postMessage(json)));
                    });
        } else {
            web.addJavascriptInterface(new JsBridge(), "A521Native");
        }
    }

    final class JsBridge {
        @JavascriptInterface
        public void postMessage(String data) {
            main.post(() -> {
                String u = web.getUrl();
                if (u == null || !u.startsWith(ORIGIN + "/")) return;
                handle(data, json -> main.post(() ->
                        web.evaluateJavascript("window.__a521reply&&window.__a521reply(" + JSONObject.quote(json) + ")", null)));
            });
        }
    }

    private void handle(String raw, Reply reply) {
        final int id;
        final String m;
        final JSONObject a;
        try {
            JSONObject o = new JSONObject(raw);
            id = o.getInt("id");
            m = o.getString("m");
            a = o.optJSONObject("a") != null ? o.optJSONObject("a") : new JSONObject();
        } catch (Exception e) {
            return;
        }
        Reply r = json -> reply.send(json);
        try {
            switch (m) {
                case "copy": {
                    ClipboardManager cm = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
                    cm.setPrimaryClip(ClipData.newPlainText("521", a.optString("text")));
                    if (Build.VERSION.SDK_INT < 33) Toast.makeText(this, R.string.copied, Toast.LENGTH_SHORT).show();
                    ok(r, id);
                    break;
                }
                case "share": {
                    Intent i = new Intent(Intent.ACTION_SEND).setType("text/plain").putExtra(Intent.EXTRA_TEXT, a.optString("text"));
                    startActivity(Intent.createChooser(i, getString(R.string.share_title)));
                    ok(r, id);
                    break;
                }
                case "open":
                    if (openExternal(a.optString("url"))) ok(r, id); else fail(r, id, "no_app");
                    break;
                case "save": {
                    if (pendingSaveReply != null) { fail(r, id, "busy"); break; }
                    String data = a.optString("data");
                    Intent i = new Intent(Intent.ACTION_CREATE_DOCUMENT).addCategory(Intent.CATEGORY_OPENABLE)
                            .setType(a.optString("mime", "text/plain"))
                            .putExtra(Intent.EXTRA_TITLE, a.optString("name", "521coffee.txt").replaceAll("[/\\\\]", "_"));
                    pendingSaveData = data;
                    pendingSaveReply = json -> r.send(json);
                    pendingSaveId = id;
                    startActivityForResult(i, REQ_SAVE);
                    break;
                }
                case "kStore": {
                    String text = a.optString("text");
                    if (!text.startsWith("window.__KREV=") || text.length() > MAX_K) { fail(r, id, "bad"); break; }
                    File f = new File(getFilesDir(), "kdata.js"), tmp = new File(getFilesDir(), "kdata.js.tmp");
                    try (OutputStream o = new FileOutputStream(tmp)) { o.write(text.getBytes(StandardCharsets.UTF_8)); }
                    if (!tmp.renameTo(f)) { fail(r, id, "io"); break; }
                    ok(r, id);
                    break;
                }
                case "notifySet": {
                    org.json.JSONArray items = a.optJSONArray("items");
                    AlertReceiver.setItems(this, items != null ? items : new org.json.JSONArray());
                    ok(r, id);
                    break;
                }
                case "notifyPerm":
                    if (Build.VERSION.SDK_INT >= 33
                            && checkSelfPermission(android.Manifest.permission.POST_NOTIFICATIONS) != android.content.pm.PackageManager.PERMISSION_GRANTED) {
                        requestPermissions(new String[]{android.Manifest.permission.POST_NOTIFICATIONS}, REQ_NOTIF);
                    }
                    ok(r, id);
                    break;
                case "notifyConfig":
                    KabarJob.setRole(this, a.optString("role", "pelanggan"));
                    ok(r, id);
                    break;
                case "notifStatus":
                    okJ(r, id, HpSettings.status(this));
                    break;
                case "openSettings":
                    if (HpSettings.open(this, a.optString("what", "app"))) ok(r, id); else fail(r, id, "no_settings");
                    break;
                case "playSound":
                    Notif.play(this, a.optString("name", "ding"));
                    ok(r, id);
                    break;
                case "kabarSync": {
                    final Context app = getApplicationContext();
                    new Thread(() -> { try { KabarJob.check(app); } catch (Exception ignored) { } }).start();
                    ok(r, id);
                    break;
                }
                case "bars":
                    applyBars(a.optString("bg"));
                    ok(r, id);
                    break;
                case "exit":
                    moveTaskToBack(true);
                    ok(r, id);
                    break;
                default:
                    fail(r, id, "unknown");
            }
        } catch (Exception e) {
            fail(r, id, "failed");
        }
    }

    private int pendingSaveId;

    private static void ok(Reply r, int id) {
        r.send("{\"id\":" + id + ",\"ok\":true}");
    }

    private static void okJ(Reply r, int id, String json) {
        r.send("{\"id\":" + id + ",\"ok\":true,\"r\":" + json + "}");
    }

    private static void fail(Reply r, int id, String code) {
        r.send("{\"id\":" + id + ",\"ok\":false,\"e\":" + JSONObject.quote(code) + "}");
    }

    private boolean openExternal(String url) {
        Uri u = Uri.parse(url);
        String sc = u.getScheme() == null ? "" : u.getScheme().toLowerCase(Locale.ROOT);
        if (!(sc.equals("https") || sc.equals("http") || sc.equals("mailto") || sc.equals("tel")
                || sc.equals("whatsapp") || sc.equals("geo"))) return false;
        try {
            startActivity(new Intent(Intent.ACTION_VIEW, u).addCategory(Intent.CATEGORY_BROWSABLE));
            return true;
        } catch (ActivityNotFoundException e) {
            Toast.makeText(this, R.string.no_app, Toast.LENGTH_SHORT).show();
            return false;
        }
    }

    @Override
    protected void onActivityResult(int req, int res, Intent data) {
        super.onActivityResult(req, res, data);
        if (req == REQ_FILE) {
            if (fileCb == null) return;
            Uri[] out = null;
            if (res == RESULT_OK && data != null) {
                ClipData cd = data.getClipData();
                if (cd != null && cd.getItemCount() > 0) {
                    out = new Uri[cd.getItemCount()];
                    for (int i = 0; i < out.length; i++) out[i] = cd.getItemAt(i).getUri();
                } else if (data.getData() != null) {
                    out = new Uri[]{data.getData()};
                }
            }
            fileCb.onReceiveValue(out);
            fileCb = null;
        } else if (req == REQ_SAVE) {
            Reply r = pendingSaveReply;
            String d = pendingSaveData;
            int id = pendingSaveId;
            pendingSaveReply = null;
            pendingSaveData = null;
            if (r == null) return;
            if (res != RESULT_OK || data == null || data.getData() == null) { fail(r, id, "cancelled"); return; }
            try (OutputStream o = getContentResolver().openOutputStream(data.getData(), "wt")) {
                if (o == null) throw new IOException();
                o.write(d.getBytes(StandardCharsets.UTF_8));
                ok(r, id);
            } catch (IOException e) {
                fail(r, id, "io");
            }
        }
    }

    // ---------- Tampilan layar penuh (edge-to-edge), keyboard, tombol kembali ----------

    private void setupInsets() {
        if (Build.VERSION.SDK_INT >= 30) {
            Window w = getWindow();
            w.setDecorFitsSystemWindows(false);
            if (Build.VERSION.SDK_INT < 35) {
                w.setStatusBarColor(Color.TRANSPARENT);
                w.setNavigationBarColor(Color.TRANSPARENT);
            }
            root.setOnApplyWindowInsetsListener((v, ins) -> {
                Insets sys = ins.getInsets(WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                Insets ime = ins.getInsets(WindowInsets.Type.ime());
                v.setPadding(sys.left, sys.top, sys.right, Math.max(sys.bottom, ime.bottom));
                return WindowInsets.CONSUMED;
            });
        }
    }

    private void applyBars(String css) {
        java.util.regex.Matcher mt = Pattern.compile("rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)").matcher(css == null ? "" : css);
        if (!mt.find()) return;
        int rr = Integer.parseInt(mt.group(1)), gg = Integer.parseInt(mt.group(2)), bb = Integer.parseInt(mt.group(3));
        int color = Color.rgb(rr, gg, bb);
        boolean light = (0.299 * rr + 0.587 * gg + 0.114 * bb) > 150;
        root.setBackgroundColor(color);
        web.setBackgroundColor(color);
        if (Build.VERSION.SDK_INT >= 30) {
            WindowInsetsController c = getWindow().getInsetsController();
            if (c != null) {
                int f = WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS | WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS;
                c.setSystemBarsAppearance(light ? f : 0, f);
            }
        } else {
            getWindow().setStatusBarColor(color);
            getWindow().setNavigationBarColor(color);
            View d = getWindow().getDecorView();
            int flags = d.getSystemUiVisibility();
            flags = light ? (flags | View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR | View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR)
                    : (flags & ~View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR & ~View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR);
            d.setSystemUiVisibility(flags);
        }
    }

    private void setupBack() {
        if (Build.VERSION.SDK_INT >= 33) {
            getOnBackInvokedDispatcher().registerOnBackInvokedCallback(
                    OnBackInvokedDispatcher.PRIORITY_DEFAULT, this::goBack);
        }
    }

    @SuppressWarnings("deprecation")
    @Override
    public void onBackPressed() {
        goBack();
    }

    private void goBack() {
        web.evaluateJavascript("window.__a521back?window.__a521back():false", v -> {
            if (!"true".equals(v)) moveTaskToBack(true);
        });
    }

    @Override
    protected void onSaveInstanceState(Bundle out) {
        super.onSaveInstanceState(out);
        try { web.saveState(out); } catch (RuntimeException ignored) { }
    }

    @Override
    protected void onResume() {
        super.onResume();
        web.onResume();
        KabarJob.foreground = true;
        try { AlertReceiver.fireDue(this); } catch (RuntimeException ignored) { } // kirim pengingat yang terlewat saat HP tidur
    }

    private String pendingOpen;

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        pendingOpen = intent.getStringExtra("open");
        runPendingOpen();
    }

    /** Notifikasi diketuk: buka tab Stok → Produk jadi (setelah login). */
    private void runPendingOpen() {
        if (web == null || !("stok".equals(pendingOpen) || "kabar".equals(pendingOpen))) return;
        String w = pendingOpen;
        pendingOpen = null;
        web.evaluateJavascript("window.__a521open&&window.__a521open('" + w + "')", null);
    }

    @Override
    public void onRequestPermissionsResult(int code, String[] perms, int[] res) {
        super.onRequestPermissionsResult(code, perms, res);
        if (code == REQ_NOTIF) { try { AlertReceiver.fireDue(this); } catch (RuntimeException ignored) { } }
    }

    @Override
    protected void onPause() {
        KabarJob.foreground = false;
        web.onPause();
        super.onPause();
    }

    @Override
    protected void onDestroy() {
        if (fileCb != null) fileCb.onReceiveValue(null);
        root.removeView(web);
        web.destroy();
        super.onDestroy();
    }
}
