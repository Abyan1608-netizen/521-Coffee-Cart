package id.coffee521.pos;

import android.content.ActivityNotFoundException;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.os.PowerManager;
import android.provider.Settings;

import org.json.JSONObject;

import java.util.Locale;

/**
 * Membuka halaman pengaturan HP yang tepat agar notifikasi tidak tertahan
 * (Autostart / baterai di Xiaomi, Oppo, Realme, Vivo, Huawei, Samsung, dll).
 * Tidak memakai izin REQUEST_IGNORE_BATTERY_OPTIMIZATIONS (dibatasi Google Play):
 * pengguna sendiri yang memilih di layar pengaturan.
 */
final class HpSettings {
    private HpSettings() { }

    static String brand() {
        String m = (Build.MANUFACTURER + " " + Build.BRAND).toLowerCase(Locale.ROOT);
        if (m.contains("xiaomi") || m.contains("redmi") || m.contains("poco")) return "xiaomi";
        if (m.contains("oppo")) return "oppo";
        if (m.contains("realme")) return "realme";
        if (m.contains("oneplus")) return "oneplus";
        if (m.contains("vivo") || m.contains("iqoo")) return "vivo";
        if (m.contains("huawei") || m.contains("honor")) return "huawei";
        if (m.contains("samsung")) return "samsung";
        if (m.contains("infinix") || m.contains("tecno") || m.contains("itel")) return "transsion";
        if (m.contains("asus")) return "asus";
        return "lain";
    }

    /** HP yang dikenal agresif menahan aplikasi di latar belakang. */
    static boolean strict(String b) {
        return !"lain".equals(b) && !"asus".equals(b);
    }

    static String status(Context c) {
        try {
            String b = brand();
            PowerManager pm = c.getSystemService(PowerManager.class);
            boolean batt = pm != null && pm.isIgnoringBatteryOptimizations(c.getPackageName());
            JSONObject o = new JSONObject();
            o.put("perm", Notif.allowed(c));
            o.put("brand", b);
            o.put("strict", strict(b));
            o.put("battery", batt); // true = tidak dibatasi
            o.put("sdk", Build.VERSION.SDK_INT);
            return o.toString();
        } catch (Exception e) {
            return "{}";
        }
    }

    private static boolean start(Context c, Intent i) {
        try {
            i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            c.startActivity(i);
            return true;
        } catch (ActivityNotFoundException | SecurityException e) {
            return false;
        }
    }

    private static boolean comp(Context c, String pkg, String cls) {
        return start(c, new Intent().setComponent(new ComponentName(pkg, cls)));
    }

    private static boolean appDetails(Context c) {
        return start(c, new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:" + c.getPackageName())));
    }

    /** what: "notif" | "autostart" | "battery" | "app" */
    static boolean open(Context c, String what) {
        String pkg = c.getPackageName(), b = brand();
        switch (what) {
            case "notif": {
                Intent i = new Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS).putExtra(Settings.EXTRA_APP_PACKAGE, pkg);
                return start(c, i) || appDetails(c);
            }
            case "autostart":
                switch (b) {
                    case "xiaomi":
                        if (comp(c, "com.miui.securitycenter", "com.miui.permcenter.autostart.AutoStartManagementActivity")) return true;
                        break;
                    case "oppo": case "realme": case "oneplus":
                        if (comp(c, "com.coloros.safecenter", "com.coloros.safecenter.permission.startup.StartupAppListActivity")) return true;
                        if (comp(c, "com.coloros.safecenter", "com.coloros.safecenter.startupapp.StartupAppListActivity")) return true;
                        if (comp(c, "com.oplus.safecenter", "com.oplus.safecenter.permission.startup.StartupAppListActivity")) return true;
                        if (comp(c, "com.oppo.safe", "com.oppo.safe.permission.startup.StartupAppListActivity")) return true;
                        break;
                    case "vivo":
                        if (comp(c, "com.vivo.permissionmanager", "com.vivo.permissionmanager.activity.BgStartUpManagerActivity")) return true;
                        if (comp(c, "com.iqoo.secure", "com.iqoo.secure.ui.phoneoptimize.BgStartUpManager")) return true;
                        if (comp(c, "com.iqoo.secure", "com.iqoo.secure.ui.phoneoptimize.AddWhiteListActivity")) return true;
                        break;
                    case "huawei":
                        if (comp(c, "com.huawei.systemmanager", "com.huawei.systemmanager.startupmgr.ui.StartupNormalAppListActivity")) return true;
                        if (comp(c, "com.huawei.systemmanager", "com.huawei.systemmanager.optimize.process.ProtectActivity")) return true;
                        break;
                    case "transsion":
                        if (comp(c, "com.transsion.phonemaster", "com.cyin.himgr.autostart.AutoStartActivity")) return true;
                        break;
                    default:
                }
                return appDetails(c);
            case "battery":
                if ("xiaomi".equals(b)) {
                    Intent i = new Intent().setComponent(new ComponentName("com.miui.powerkeeper", "com.miui.powerkeeper.ui.HiddenAppsConfigActivity"))
                            .putExtra("package_name", pkg).putExtra("package_label", c.getString(R.string.app_name));
                    if (start(c, i)) return true;
                }
                if ("vivo".equals(b) && comp(c, "com.iqoo.powersaving", "com.iqoo.powersaving.PowerSavingManagerActivity")) return true;
                if ("huawei".equals(b) && comp(c, "com.huawei.systemmanager", "com.huawei.systemmanager.power.ui.HwPowerManagerActivity")) return true;
                // Oppo/Realme/Samsung/lainnya: pengaturan baterai ada di info aplikasi
                if (appDetails(c)) return true;
                return start(c, new Intent(Settings.ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS));
            default:
                return appDetails(c);
        }
    }
}
