# Jembatan JS fallback (addJavascriptInterface) dipanggil lewat refleksi oleh WebView.
-keepclassmembers class id.coffee521.pos.MainActivity$JsBridge {
    @android.webkit.JavascriptInterface <methods>;
}
-keepattributes JavascriptInterface
