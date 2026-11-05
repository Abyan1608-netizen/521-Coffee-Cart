package id.coffee521.pos;

import android.Manifest;
import android.annotation.SuppressLint;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothClass;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattService;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothProfile;
import android.bluetooth.BluetoothSocket;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.location.LocationManager;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;

import org.json.JSONObject;

import java.io.IOException;
import java.io.OutputStream;
import java.util.HashSet;
import java.util.Locale;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;
import java.util.regex.Pattern;

/**
 * Printer thermal Bluetooth (ESC/POS) untuk struk kasir.
 * - Bluetooth klasik (SPP) — kebanyakan printer 58/80 mm murah — dan Bluetooth LE (BLE) untuk printer yang hanya BLE.
 * - Byte ESC/POS dibuat oleh aplikasi (app.js); kelas ini hanya mencari, menyambung, dan mengirim byte.
 * - Printer pilihan disimpan, jadi kasir cukup menekan Cetak: aplikasi menyambung sendiri bila perlu.
 */
@SuppressLint("MissingPermission") // izin selalu dicek lewat hasPerms() sebelum dipakai; SecurityException ditangkap
final class BtPrinter {

    interface Emit { void emit(String json); }
    interface Done { void done(boolean ok, String info); }

    private static final UUID SPP = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    private static final String PREF = "btprinter";
    private static final long SCAN_MS = 12_000, IDLE_MS = 120_000;
    private static final Pattern PRINTER_NAME = Pattern.compile(
            "(?i).*(print|\\bpos\\b|pos-?\\d|pt-?\\d|mpt|rpp|xp-|zj-|goojprt|thermal|inner|mtp|ezpos|hoin|epson|bixolon|sunmi|cashino|"
                    + "p58|p80|58mm|80mm|qs-|mht|jp-?\\d|bluetooth p|blue ?printer|gprinter|xprinter|panda|mini ?printer|ttp|rongta|zebra).*");
    private static final String[] BLE_SVCS = {"000018f0-0000-1000-8000-00805f9b34fb", "0000ff00-0000-1000-8000-00805f9b34fb",
            "0000ffe0-0000-1000-8000-00805f9b34fb", "0000fee7-0000-1000-8000-00805f9b34fb", "e7810a71-73ae-499d-8c15-faa9aef0c3f2",
            "49535343-fe7d-4ae5-8fa9-9fafd205e455"};

    private static BtPrinter inst;

    static synchronized BtPrinter get(Context c) {
        if (inst == null) inst = new BtPrinter(c.getApplicationContext());
        return inst;
    }

    private final Context app;
    private final Handler main = new Handler(Looper.getMainLooper());
    private final ExecutorService io = Executors.newSingleThreadExecutor();
    private volatile Emit emit;

    private BluetoothSocket sock;
    private OutputStream out;
    private BluetoothGatt gatt;
    private BluetoothGattCharacteristic gch;
    private volatile int mtu = 23;
    private String connAddr;
    private final Semaphore writeDone = new Semaphore(0);

    private boolean scanning;
    private BroadcastReceiver rx;
    private ScanCallback leCb;
    private final Set<String> seen = new HashSet<>();
    private final Runnable stopScan = this::stopScan;
    private final Runnable idleClose = () -> io.execute(this::close);

    private BtPrinter(Context app) { this.app = app; }

    void setEmit(Emit e) { emit = e; }

    // ---------- izin & status ----------

    static String[] perms() {
        return Build.VERSION.SDK_INT >= 31
                ? new String[]{Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT}
                : new String[]{Manifest.permission.ACCESS_FINE_LOCATION};
    }

    static boolean hasPerms(Context c) {
        for (String p : perms()) if (c.checkSelfPermission(p) != PackageManager.PERMISSION_GRANTED) return false;
        return true;
    }

    BluetoothAdapter adapter() {
        BluetoothManager m = app.getSystemService(BluetoothManager.class);
        return m != null ? m.getAdapter() : null;
    }

    boolean isOn() {
        BluetoothAdapter a = adapter();
        try { return a != null && a.isEnabled(); } catch (SecurityException e) { return false; }
    }

    private boolean locationOff() {
        if (Build.VERSION.SDK_INT >= 31 || Build.VERSION.SDK_INT < 28) return false; // Android 12+: cari perangkat tanpa lokasi
        LocationManager lm = app.getSystemService(LocationManager.class);
        try { return lm != null && !lm.isLocationEnabled(); } catch (Exception e) { return false; }
    }

    String state() {
        try {
            SharedPreferences sp = app.getSharedPreferences(PREF, Context.MODE_PRIVATE);
            JSONObject o = new JSONObject();
            o.put("supported", adapter() != null);
            o.put("on", isOn());
            o.put("perm", hasPerms(app));
            o.put("locOff", locationOff());
            o.put("addr", sp.getString("addr", ""));
            o.put("name", sp.getString("name", ""));
            o.put("connected", connected());
            o.put("scanning", scanning);
            return o.toString();
        } catch (Exception e) { return "{}"; }
    }

    private synchronized boolean connected() { return (sock != null && sock.isConnected()) || (gatt != null && gch != null); }

    // ---------- mencari printer ----------

    void scan() {
        main.post(() -> {
            if (scanning) return;
            BluetoothAdapter a = adapter();
            if (a == null || !isOn() || !hasPerms(app)) { send("{\"ev\":\"done\",\"err\":\"" + (a == null ? "unsupported" : !hasPerms(app) ? "perm" : "off") + "\"}"); return; }
            scanning = true;
            seen.clear();
            try {
                for (BluetoothDevice d : a.getBondedDevices()) dev(d, true);
            } catch (SecurityException ignored) { }
            rx = new BroadcastReceiver() {
                @Override
                public void onReceive(Context c, Intent i) {
                    if (BluetoothDevice.ACTION_FOUND.equals(i.getAction())) {
                        BluetoothDevice d = Build.VERSION.SDK_INT >= 33 ? i.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE, BluetoothDevice.class)
                                : legacyDevice(i);
                        if (d != null) dev(d, false);
                    }
                }
            };
            IntentFilter f = new IntentFilter(BluetoothDevice.ACTION_FOUND);
            if (Build.VERSION.SDK_INT >= 33) app.registerReceiver(rx, f, Context.RECEIVER_EXPORTED);
            else app.registerReceiver(rx, f);
            try {
                if (a.isDiscovering()) a.cancelDiscovery();
                a.startDiscovery();
            } catch (SecurityException ignored) { }
            try {
                BluetoothLeScanner le = a.getBluetoothLeScanner();
                if (le != null) {
                    leCb = new ScanCallback() {
                        @Override public void onScanResult(int type, ScanResult r) { if (r != null && r.getDevice() != null) dev(r.getDevice(), false); }
                    };
                    le.startScan(leCb);
                }
            } catch (SecurityException | IllegalStateException ignored) { leCb = null; }
            main.postDelayed(stopScan, SCAN_MS);
        });
    }

    @SuppressWarnings("deprecation")
    private static BluetoothDevice legacyDevice(Intent i) { return i.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE); }

    void stopScan() {
        main.removeCallbacks(stopScan);
        if (!scanning) return;
        scanning = false;
        BluetoothAdapter a = adapter();
        try { if (a != null && a.isDiscovering()) a.cancelDiscovery(); } catch (SecurityException ignored) { }
        try { if (a != null && leCb != null && a.getBluetoothLeScanner() != null) a.getBluetoothLeScanner().stopScan(leCb); } catch (SecurityException | IllegalStateException ignored) { }
        leCb = null;
        if (rx != null) { try { app.unregisterReceiver(rx); } catch (IllegalArgumentException ignored) { } rx = null; }
        send("{\"ev\":\"done\"}");
    }

    private void dev(BluetoothDevice d, boolean bonded) {
        try {
            String addr = d.getAddress(), name = d.getName();
            if (addr == null || (name == null && !bonded) || !seen.add(addr)) return;
            BluetoothClass bc = d.getBluetoothClass();
            boolean printer = (bc != null && bc.getMajorDeviceClass() == BluetoothClass.Device.Major.IMAGING)
                    || (name != null && PRINTER_NAME.matcher(name).matches());
            JSONObject o = new JSONObject();
            o.put("ev", "dev");
            o.put("addr", addr);
            o.put("name", name == null ? addr : name);
            o.put("bonded", bonded || d.getBondState() == BluetoothDevice.BOND_BONDED);
            o.put("le", d.getType() == BluetoothDevice.DEVICE_TYPE_LE);
            o.put("printer", printer);
            send(o.toString());
        } catch (SecurityException | org.json.JSONException ignored) { }
    }

    private void send(String json) { Emit e = emit; if (e != null) main.post(() -> e.emit(json)); }

    // ---------- sambung & cetak ----------

    void connect(String addr, Done cb) {
        main.post(this::stopScan);
        io.execute(() -> {
            try {
                doConnect(addr);
                String name = "";
                try { name = adapter().getRemoteDevice(addr).getName(); } catch (SecurityException ignored) { }
                app.getSharedPreferences(PREF, Context.MODE_PRIVATE).edit().putString("addr", addr).putString("name", name == null ? "" : name).apply();
                idle();
                cb.done(true, name == null ? "" : name);
            } catch (Exception e) {
                close();
                cb.done(false, reason(e));
            }
        });
    }

    void print(byte[] data, Done cb) {
        io.execute(() -> {
            String addr = app.getSharedPreferences(PREF, Context.MODE_PRIVATE).getString("addr", "");
            if (addr.isEmpty()) { cb.done(false, "no_printer"); return; }
            for (int attempt = 0; attempt < 2; attempt++) {
                try {
                    if (!connected() || !addr.equals(connAddr)) doConnect(addr);
                    write(data);
                    idle();
                    cb.done(true, "");
                    return;
                } catch (Exception e) {
                    close();
                    if (attempt == 1) cb.done(false, reason(e));
                }
            }
        });
    }

    void forget() {
        io.execute(this::close);
        app.getSharedPreferences(PREF, Context.MODE_PRIVATE).edit().clear().apply();
    }

    private static String reason(Exception e) {
        if (e instanceof SecurityException) return "perm";
        String m = e.getMessage();
        return m == null || m.isEmpty() ? e.getClass().getSimpleName() : m;
    }

    private void idle() { main.removeCallbacks(idleClose); main.postDelayed(idleClose, IDLE_MS); }

    private void doConnect(String addr) throws IOException, InterruptedException {
        BluetoothAdapter a = adapter();
        if (a == null) throw new IOException("unsupported");
        if (!hasPerms(app)) throw new SecurityException("perm");
        if (!a.isEnabled()) throw new IOException("off");
        close();
        try { if (a.isDiscovering()) a.cancelDiscovery(); } catch (SecurityException ignored) { }
        BluetoothDevice d = a.getRemoteDevice(addr.toUpperCase(Locale.ROOT));
        int type = d.getType();
        if (type == BluetoothDevice.DEVICE_TYPE_LE) { gattConnect(d); connAddr = addr; return; }
        try {
            sppConnect(d);
        } catch (IOException e) {
            if (type == BluetoothDevice.DEVICE_TYPE_CLASSIC) throw e;
            gattConnect(d); // DUAL / UNKNOWN: coba BLE
        }
        connAddr = addr;
    }

    private void sppConnect(BluetoothDevice d) throws IOException {
        BluetoothSocket s = null;
        IOException last = null;
        for (int i = 0; i < 3 && s == null; i++) {
            BluetoothSocket t = null;
            try {
                if (i == 0) t = d.createRfcommSocketToServiceRecord(SPP);
                else if (i == 1) t = d.createInsecureRfcommSocketToServiceRecord(SPP);
                else t = (BluetoothSocket) d.getClass().getMethod("createRfcommSocket", int.class).invoke(d, 1);
                t.connect();
                s = t;
            } catch (IOException e) {
                last = e;
                if (t != null) try { t.close(); } catch (IOException ignored) { }
            } catch (ReflectiveOperationException e) {
                last = new IOException("connect_failed");
            }
        }
        if (s == null) throw last != null ? last : new IOException("connect_failed");
        synchronized (this) { sock = s; out = s.getOutputStream(); }
    }

    private void gattConnect(BluetoothDevice d) throws IOException, InterruptedException {
        CountDownLatch ready = new CountDownLatch(1);
        final boolean[] ok = {false};
        BluetoothGattCallback cb = new BluetoothGattCallback() {
            @Override
            public void onConnectionStateChange(BluetoothGatt g, int status, int st) {
                if (st == BluetoothProfile.STATE_CONNECTED) { if (!g.requestMtu(247)) g.discoverServices(); }
                else if (st == BluetoothProfile.STATE_DISCONNECTED) { synchronized (BtPrinter.this) { gch = null; } ready.countDown(); }
            }
            @Override public void onMtuChanged(BluetoothGatt g, int m, int status) { if (status == BluetoothGatt.GATT_SUCCESS) mtu = m; g.discoverServices(); }
            @Override
            public void onServicesDiscovered(BluetoothGatt g, int status) {
                BluetoothGattCharacteristic ch = pickChar(g);
                synchronized (BtPrinter.this) { gch = ch; }
                ok[0] = ch != null;
                ready.countDown();
            }
            @Override public void onCharacteristicWrite(BluetoothGatt g, BluetoothGattCharacteristic c, int status) { writeDone.release(); }
        };
        mtu = 23;
        BluetoothGatt g = d.connectGatt(app, false, cb, BluetoothDevice.TRANSPORT_LE);
        synchronized (this) { gatt = g; }
        if (!ready.await(15, TimeUnit.SECONDS) || !ok[0]) throw new IOException("not_printer");
    }

    private static BluetoothGattCharacteristic pickChar(BluetoothGatt g) {
        BluetoothGattCharacteristic any = null;
        for (BluetoothGattService s : g.getServices()) {
            boolean known = false;
            for (String u : BLE_SVCS) if (u.equalsIgnoreCase(s.getUuid().toString())) known = true;
            for (BluetoothGattCharacteristic c : s.getCharacteristics()) {
                int p = c.getProperties();
                if ((p & (BluetoothGattCharacteristic.PROPERTY_WRITE | BluetoothGattCharacteristic.PROPERTY_WRITE_NO_RESPONSE)) == 0) continue;
                if (known) return c;
                if (any == null) any = c;
            }
        }
        return any;
    }

    private void write(byte[] data) throws IOException, InterruptedException {
        OutputStream o;
        BluetoothGatt g;
        BluetoothGattCharacteristic c;
        synchronized (this) { o = out; g = gatt; c = gch; }
        if (o != null) {
            for (int i = 0; i < data.length; i += 512) {
                o.write(data, i, Math.min(512, data.length - i));
                o.flush();
                Thread.sleep(20); // beri waktu buffer printer
            }
            return;
        }
        if (g == null || c == null) throw new IOException("not_connected");
        boolean noResp = (c.getProperties() & BluetoothGattCharacteristic.PROPERTY_WRITE_NO_RESPONSE) != 0;
        int type = noResp ? BluetoothGattCharacteristic.WRITE_TYPE_NO_RESPONSE : BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT;
        int chunk = Math.max(20, Math.min(180, mtu - 3));
        writeDone.drainPermits();
        for (int i = 0; i < data.length; i += chunk) {
            byte[] part = java.util.Arrays.copyOfRange(data, i, Math.min(data.length, i + chunk));
            boolean sent = false;
            for (int t = 0; t < 20 && !sent; t++) {
                sent = gattWrite(g, c, part, type);
                if (!sent) Thread.sleep(25);
            }
            if (!sent) throw new IOException("write_failed");
            // tunggu konfirmasi tulis (tanpa-respons: hanya jeda singkat agar antrean BLE tidak penuh)
            if (!writeDone.tryAcquire(noResp ? 300 : 2000, TimeUnit.MILLISECONDS) && !noResp) throw new IOException("write_timeout");
        }
    }

    @SuppressWarnings("deprecation")
    private static boolean gattWrite(BluetoothGatt g, BluetoothGattCharacteristic c, byte[] v, int type) {
        if (Build.VERSION.SDK_INT >= 33) return g.writeCharacteristic(c, v, type) == BluetoothGatt.GATT_SUCCESS;
        c.setWriteType(type);
        c.setValue(v);
        return g.writeCharacteristic(c);
    }

    private synchronized void close() {
        try { if (sock != null) sock.close(); } catch (IOException ignored) { }
        try { if (gatt != null) { gatt.disconnect(); gatt.close(); } } catch (SecurityException ignored) { }
        sock = null; out = null; gatt = null; gch = null; connAddr = null;
    }
}
