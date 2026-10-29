/* 521 Coffee App — lapisan Android.
   Menyediakan window.claude.use(...) versi aplikasi (sinkron, terbit Kabar, Chat 521, simpan file)
   sehingga kode aplikasi web tidak perlu diubah. Dimuat SEBELUM app.js.
   Semua fitur jaringan opsional: tanpa server (A521_CFG.server kosong) aplikasi tetap jalan penuh offline. */
(function () {
  "use strict";
  var CFG = window.A521_CFG || {};
  var SRV = String(CFG.server || "").replace(/\/+$/, "");
  var LS = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} },
    del: function (k) { try { localStorage.removeItem(k); } catch (e) {} }
  };

  /* ---------- Data Kabar/menu: versi terbaru dari server (disimpan native) atau bawaan aplikasi ---------- */
  var KREV = +window.__KREV || 0;
  try {
    var kel = document.getElementById("kdata");
    if (kel && window.__K) kel.textContent = JSON.stringify(window.__K);
  } catch (e) {}

  /* ---------- Jembatan ke Android (WebMessageListener / fallback JavascriptInterface) ---------- */
  var N = window.A521Native || null, seq = 0, wait = {};
  function onReply(ev) {
    var m; try { m = JSON.parse(typeof ev === "string" ? ev : ev.data); } catch (e) { return; }
    var w = wait[m.id]; if (!w) return; delete wait[m.id];
    if (m.ok) w.res(m.r); else w.rej(Object.assign(new Error(m.e || "gagal"), { code: m.e || "failed" }));
  }
  if (N) { try { N.onmessage = onReply; } catch (e) {} }
  window.__a521reply = onReply;
  function call(method, args) {
    return new Promise(function (res, rej) {
      if (!N) return rej(Object.assign(new Error("no_native"), { code: "no_native" }));
      var id = ++seq; wait[id] = { res: res, rej: rej };
      try { N.postMessage(JSON.stringify({ id: id, m: method, a: args || {} })); }
      catch (e) { delete wait[id]; rej(e); }
    });
  }

  var A = window.A521 = {
    native: !!N,
    server: SRV,
    open: function (url) { if (N) call("open", { url: String(url) }).catch(function () {}); else window.open(url, "_blank", "noopener"); },
    /* Pengingat lokal (notifikasi HP), dijadwalkan oleh Android: [{id, at(ms), title, body}] */
    notify: function (items) { if (N) call("notifySet", { items: items || [] }).catch(function () {}); },
    notifyPerm: function () { if (N) call("notifyPerm", {}).catch(function () {}); },
    notifStatus: function () { return N ? call("notifStatus", {}) : Promise.resolve(null); },
    openSettings: function (what) { if (N) call("openSettings", { what: String(what || "app") }).catch(function () {}); },
    playSound: function (name) { if (N) call("playSound", { name: String(name || "ding") }).catch(function () {}); },
    /* Peran HP untuk penerima notifikasi: owner (HP Owner) / staf (pernah login atau tersambung tim) / pelanggan */
    syncRole: function () {
      if (!N) return;
      var role = "pelanggan";
      try { var d = JSON.parse(LS.get("pos521")) || {}, c = d.cfg || {}; if (c.staffDev || c.teamCode) role = "staf"; } catch (e) {}
      if (LS.get("a521ownerOk") === "1") role = "owner";
      call("notifyConfig", { role: role }).catch(function () {});
    },
    ownerLink: function (key) {
      if (!SRV) return Promise.resolve(false);
      return fetch(SRV + "/auth", { method: "POST", headers: { Authorization: "Bearer " + key } })
        .then(function (r) { if (!r.ok) return false; LS.set("a521owner", key); LS.set("a521ownerOk", "1"); return true; })
        .catch(function () { return false; });
    }
  };

  /* Salin & bagikan lewat Android (lebih andal daripada API web di WebView) */
  if (N) {
    try {
      var origClip = navigator.clipboard;
      Object.defineProperty(navigator, "clipboard", { configurable: true, value: {
        writeText: function (t) { return call("copy", { text: String(t) }); },
        readText: function () { return origClip && origClip.readText ? origClip.readText() : Promise.reject(new Error("no")); }
      } });
    } catch (e) {}
    try {
      navigator.share = function (d) { d = d || {}; return call("share", { text: [d.title, d.text, d.url].filter(Boolean).join("\n") }); };
    } catch (e) {}
  }

  /* Tombol kembali Android: tutup chat/lembar dulu, baru keluar */
  window.__a521back = function () {
    try {
      var rp = document.querySelector("#chat .crep");
      if (rp) { rp.remove(); return true; }
      var c = document.getElementById("chat");
      if (c && !c.hidden && !c.classList.contains("closing")) { chatClose(); return true; }
      var m = document.getElementById("m");
      if (m && !m.hidden) { shut(); return true; }
      var lg = document.getElementById("login");
      if (lg && !lg.hidden && !me) { showPub(); return true; }
    } catch (e) {}
    return false;
  };

  /* Notifikasi pengingat diketuk: buka Stok → Produk jadi (langsung bila sudah login, atau setelah login) */
  window.__a521open = function (w) {
    if (w === "kabar") { try { if (me) { tab = "kabar"; render(); } else showPub(); } catch (e) {} return; }
    if (w !== "stok") return;
    try { sessionStorage.setItem("a521goto", "stk"); } catch (e) {}
    try { if (me && can("stk")) { sessionStorage.removeItem("a521goto"); tab = "stk"; stkV = "fg"; render(); } } catch (e) {}
  };

  /* Warna status bar mengikuti tema terang/gelap aplikasi */
  if (N) {
    var lastBg = "";
    var syncBars = function () {
      try {
        var bg = getComputedStyle(document.body).backgroundColor;
        if (bg && bg !== lastBg) { lastBg = bg; call("bars", { bg: bg }).catch(function () {}); }
      } catch (e) {}
    };
    document.addEventListener("DOMContentLoaded", function () {
      syncBars();
      new MutationObserver(function () { setTimeout(syncBars, 60); setTimeout(syncBars, 760); })
        .observe(document.documentElement, { attributes: true, attributeFilter: ["data-ui", "class", "style"] });
    });
  }

  /* ---------- Util ---------- */
  function hex(buf) { return Array.prototype.map.call(new Uint8Array(buf), function (x) { return x.toString(16).padStart(2, "0"); }).join(""); }
  function sha(str) { return crypto.subtle.digest("SHA-256", new TextEncoder().encode(str)).then(hex); }
  function dataUrlBytes(u) {
    var m = /^data:(image\/[a-z+.-]+);base64,(.*)$/.exec(u); if (!m) return null;
    var bin = atob(m[2]), out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return { type: m[1], bytes: out, ext: ({ "image/jpeg": "jpg", "image/png": "png", "image/webp": "webp", "image/gif": "gif", "image/avif": "avif" })[m[1]] || "img" };
  }
  function ownerKey() { return LS.get("a521owner") || ""; }
  function deviceId() { var d = LS.get("a521dev"); if (!d) { d = hex(crypto.getRandomValues(new Uint8Array(12))); LS.set("a521dev", d); } return d; }
  function teamCode() { try { return ((JSON.parse(LS.get("pos521")) || {}).cfg || {}).teamCode || ""; } catch (e) { return ""; } }
  function err(code, text) { var e = new Error(code); e.code = code; if (text) e.text = text; return e; }

  /* ---------- Ambil versi Kabar/menu terbaru dari server ---------- */
  var pendingReload = false;
  function idle() {
    try { return !document.querySelector("#m:not([hidden]),#chat:not([hidden])") && !(typeof lines === "function" && lines().length); } catch (e) { return true; }
  }
  function maybeReload() {
    if (!pendingReload || !idle()) return;
    /* pengaman: jangan memuat ulang dua kali untuk versi yang sama (cegah loop) */
    var g = "a521rl", done = null; try { done = sessionStorage.getItem(g); } catch (e) {}
    if (done === String(KREV)) return;
    try { sessionStorage.setItem(g, String(KREV)); } catch (e) {}
    location.reload();
  }
  function pullK(quiet) {
    if (!SRV) return Promise.resolve(false);
    return fetch(SRV + "/k?since=" + KREV, { cache: "no-store" }).then(function (r) {
      if (r.status === 204 || !r.ok) return false;
      return r.json().then(function (o) {
        if (!o || !o.k || !(o.rev > KREV)) return false;
        var body = "window.__KREV=" + (+o.rev) + ";window.__K=" + JSON.stringify(o.k).replace(/</g, "\\u003c") + ";";
        if (!N) return false; /* tanpa Android: tidak ada tempat menyimpan, pakai data bawaan */
        return call("kStore", { text: body }).then(function () { KREV = o.rev; pendingReload = true; if (!quiet) maybeReload(); return true; });
      });
    }).catch(function () { return false; });
  }
  var bootAt = Date.now();
  /* beri tahu Android peran HP ini & minta cek kabar/promo terbaru di latar belakang */
  setTimeout(function () { try { A.syncRole(); if (N && SRV) call("kabarSync", {}).catch(function () {}); } catch (e) {} }, 2500);
  if (SRV) {
    pullK(true).then(function (got) { if (got && Date.now() - bootAt < 4000 && !window.__a521touched) maybeReload(); });
    ["pointerdown", "keydown", "input"].forEach(function (t) { addEventListener(t, function () { window.__a521touched = 1; }, { once: true, capture: true }); });
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "visible") { if (pendingReload) maybeReload(); else pullK(false); }
    });
    setInterval(function () { if (document.visibilityState === "visible") pullK(true).then(function () { maybeReload(); }); }, 5 * 60 * 1000);
  }

  /* ---------- Implementasi claude.use(...) ---------- */
  var uploaded = {};
  try { uploaded = JSON.parse(LS.get("a521media")) || {}; } catch (e) {}
  function externalize(k) {
    /* Foto data:URL di Kabar → file media di server (sekali unggah per foto), supaya data Kabar tetap kecil */
    var jobs = [];
    function walk(o) {
      if (Array.isArray(o)) { for (var i = 0; i < o.length; i++) visit(o, i); }
      else if (o && typeof o === "object") { for (var key in o) if (Object.prototype.hasOwnProperty.call(o, key)) visit(o, key); }
    }
    function visit(o, key) {
      var v = o[key];
      if (typeof v === "string" && /^media\/[a-f0-9]{32}\.(jpg|png|webp|gif|avif)$/.test(v) && !uploaded[v.slice(6)]) {
        /* foto bawaan aplikasi: pastikan server juga punya (untuk HP dengan versi aplikasi berbeda) */
        jobs.push(fetch(v).then(function (r) { if (!r.ok) return; var t = r.headers.get("Content-Type") || "image/jpeg";
          return r.arrayBuffer().then(function (b) {
            return fetch(SRV + "/" + v, { method: "PUT", headers: { Authorization: "Bearer " + ownerKey(), "Content-Type": t }, body: b })
              .then(function (x) { if (x.ok) { uploaded[v.slice(6)] = 1; LS.set("a521media", JSON.stringify(uploaded)); } });
          }); }).catch(function () {}));
      } else if (typeof v === "string" && v.indexOf("data:image/") === 0) {
        var d0 = dataUrlBytes(v); if (!d0) return;
        jobs.push(crypto.subtle.digest("SHA-256", d0.bytes).then(hex).then(function (h) {
          var d = d0;
          var name = h.slice(0, 32) + "." + d.ext;
          var up = uploaded[name] ? Promise.resolve() :
            fetch(SRV + "/media/" + name, { method: "PUT", headers: { Authorization: "Bearer " + ownerKey(), "Content-Type": d.type }, body: d.bytes })
              .then(function (r) { if (!r.ok) throw err(r.status === 401 || r.status === 403 ? "not_writer" : "upload_failed"); uploaded[name] = 1; LS.set("a521media", JSON.stringify(uploaded)); });
          return up.then(function () { o[key] = "media/" + name; });
        }));
      } else if (v && typeof v === "object") walk(v);
    }
    walk(k);
    return Promise.all(jobs).then(function () { return k; });
  }
  var ARTIFACT = {
    publish: function (doc) {
      if (!SRV) return Promise.reject(err("not_granted"));
      if (!ownerKey()) return Promise.reject(err("not_writer"));
      var m = /<script type="application\/json" id="kdata">([\s\S]*?)<\/script>/.exec(String(doc || ""));
      if (!m) return Promise.reject(err("bad_doc"));
      var k; try { k = JSON.parse(m[1]); } catch (e) { return Promise.reject(err("bad_doc")); }
      var sent = null;
      return externalize(k).then(function (k2) {
        sent = k2;
        return fetch(SRV + "/k", { method: "PUT", headers: { Authorization: "Bearer " + ownerKey(), "Content-Type": "application/json" }, body: JSON.stringify({ base: KREV, k: k2 }) });
      }).then(function (r) {
        if (r.status === 409) { pullK(true).then(function () { pendingReload = true; setTimeout(maybeReload, 1500); }); throw err("conflict"); }
        if (r.status === 401 || r.status === 403) throw err("not_writer");
        if (!r.ok) throw err("publish_failed");
        return r.json();
      }).then(function (o) {
        var body = "window.__KREV=" + (+o.rev) + ";window.__K=" + JSON.stringify(sent).replace(/</g, "\\u003c") + ";";
        KREV = +o.rev;
        return (N ? call("kStore", { text: body }) : Promise.resolve()).then(function () { return { ok: true }; }, function () { return { ok: true }; });
      });
    }
  };
  var USER = {
    canEdit: function () {
      var key = ownerKey(); if (!key || !SRV) return Promise.resolve(false);
      /* cek ulang di latar belakang; bila kunci sudah diganti di server, HP ini berhenti jadi HP Owner */
      fetch(SRV + "/auth", { method: "POST", headers: { Authorization: "Bearer " + key } })
        .then(function (r) { if (r.status === 401 || r.status === 403) { LS.del("a521owner"); LS.del("a521ownerOk"); } }).catch(function () {});
      return Promise.resolve(LS.get("a521ownerOk") === "1");
    }
  };

  /* Ruang realtime (WebSocket) per tim: id ruang = hash kode tim, isi pesan tetap terenkripsi kode tim oleh aplikasi */
  function Room() {
    var ws = null, myId = "", pres = null, evH = {}, peerH = [], peers = {}, q = [], tries = 0, code = "", timer = 0;
    function peerObj(p) { return { id: p.id, isMe: p.id === myId, presence: p.presence || null }; }
    function fire(ch) { peerH.forEach(function (f) { try { f(ch); } catch (e) {} }); }
    function connect() {
      code = teamCode(); if (!code || !SRV) { timer = setTimeout(connect, 5000); return; }
      sha("521room|" + code.toUpperCase()).then(function (rid) {
        var u = SRV.replace(/^http/, "ws") + "/room/" + rid.slice(0, 40) + "?dev=" + deviceId();
        try { ws = new WebSocket(u); } catch (e) { return retry(); }
        ws.onopen = function () { tries = 0; if (pres) send({ t: "presence", data: pres }); while (q.length) send(q.shift()); };
        ws.onmessage = function (ev) {
          var m; try { m = JSON.parse(ev.data); } catch (e) { return; }
          if (m.t === "hello") { myId = m.you; return; }
          if (m.t === "peers") {
            var all = (m.peers || []).map(peerObj), by = {};
            all.forEach(function (p) { by[p.id] = p; });
            var joined = (m.joined || []).map(function (id) { return by[id]; }).filter(Boolean);
            var updated = (m.updated || []).map(function (id) { return by[id]; }).filter(Boolean);
            var left = (m.left || []).map(function (id) { return peers[id] || { id: id, isMe: false, presence: null }; });
            peers = by; fire({ peers: all, joined: joined, updated: updated, left: left });
          } else if (m.t === "ev" && evH[m.event]) {
            evH[m.event].forEach(function (f) { try { f({ event: m.event, data: m.data, from: m.from }); } catch (e) {} });
          }
        };
        ws.onclose = function () { ws = null; retry(); };
        ws.onerror = function () { try { ws.close(); } catch (e) {} };
      });
    }
    function retry() { clearTimeout(timer); tries++; timer = setTimeout(connect, Math.min(30000, 1000 * Math.pow(2, Math.min(tries, 5)))); }
    function send(o) { if (ws && ws.readyState === 1) { ws.send(JSON.stringify(o)); return true; } return false; }
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "visible" && !ws) { clearTimeout(timer); tries = 0; connect(); }
    });
    setInterval(function () { if (ws && teamCode() !== code) { try { ws.close(); } catch (e) {} } }, 5000);
    connect();
    return {
      presence: function (data) { pres = data; send({ t: "presence", data: data }); return Promise.resolve(); },
      onPeers: function (f) { peerH.push(f); return function () { peerH = peerH.filter(function (x) { return x !== f; }); }; },
      on: function (event, f) { (evH[event] = evH[event] || []).push(f); return function () { evH[event] = evH[event].filter(function (x) { return x !== f; }); }; },
      emit: function (event, data) { var o = { t: "emit", event: event, data: data }; if (!send(o)) { q.push(o); if (q.length > 20) q.shift(); } return Promise.resolve(); }
    };
  }

  /* Chat 521 lewat server (kunci Claude API ada di server, bukan di aplikasi) */
  function sample(messages, opt) {
    opt = opt || {};
    var acc = "";
    return fetch(SRV + "/chat", {
      method: "POST", signal: opt.signal,
      headers: { "Content-Type": "application/json", "X-A521-Dev": deviceId() },
      body: JSON.stringify({ messages: messages })
    }).then(function (r) {
      if (r.status === 429) throw err("rate_limited", "Chat 521 lagi ramai sekali. Coba lagi sebentar ya 🙏☕");
      if (r.status === 503) throw err("sampling_disabled");
      if (!r.ok || !r.body) throw err("failed");
      var rd = r.body.getReader(), dec = new TextDecoder();
      function pump() {
        return rd.read().then(function (x) {
          if (x.done) return { text: acc };
          acc += dec.decode(x.value, { stream: true });
          if (opt.onText) try { opt.onText({ text: acc }); } catch (e) {}
          return pump();
        });
      }
      return pump();
    }).catch(function (e) {
      if (e && e.name === "AbortError") throw err("cancelled", acc);
      if (e && e.code) { if (!e.text && acc) e.text = acc; throw e; }
      throw err("failed", acc || "");
    });
  }

  var DOWNLOADS = {
    save: function (o) {
      o = o || {};
      var name = String(o.filename || "521coffee.txt");
      var mime = /\.json$/i.test(name) ? "application/json" : /\.csv$/i.test(name) ? "text/csv" : "text/plain";
      return call("save", { name: name, data: String(o.data == null ? "" : o.data), mime: mime });
    }
  };

  var caps = {};
  if (N) caps.downloads = DOWNLOADS;
  if (SRV) { caps.artifact = ARTIFACT; caps.user = USER; caps.sample = sample; }
  var roomInst = null;
  window.claude = {
    use: function (name) {
      if (name === "room") { if (!SRV) return Promise.reject(err("not_declared")); roomInst = roomInst || Room(); return Promise.resolve(roomInst); }
      if (caps[name]) return Promise.resolve(caps[name]);
      return Promise.reject(err("not_declared"));
    }
  };
})();
