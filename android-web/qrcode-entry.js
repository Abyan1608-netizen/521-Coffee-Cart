/* Pengganti qrcodejs (CDN) yang dibundel lokal: API sama — new QRCode(el,{text,width,height,colorDark,colorLight,correctLevel}).
   Inti generator: "QRCode for JavaScript" (c) 2009 Kazuhiko Arase, lisensi MIT. */
var Model = require("./vendor/qrcode/index.js");
var ECL = require("./vendor/qrcode/QRErrorCorrectLevel.js");

function QRCode(el, o) {
  if (typeof o === "string") o = { text: o };
  o = Object.assign({ width: 256, height: 256, colorDark: "#000000", colorLight: "#ffffff", correctLevel: ECL.M }, o || {});
  var text = unescape(encodeURIComponent(String(o.text || "")));
  var qr = new Model(-1, o.correctLevel);
  qr.addData(text);
  qr.make();
  var n = qr.getModuleCount(), quiet = 4, total = n + quiet * 2;
  var cv = document.createElement("canvas");
  cv.width = o.width; cv.height = o.height;
  var x = cv.getContext("2d"), s = Math.min(o.width, o.height) / total;
  x.fillStyle = o.colorLight; x.fillRect(0, 0, cv.width, cv.height);
  x.fillStyle = o.colorDark;
  for (var r = 0; r < n; r++) for (var c = 0; c < n; c++) {
    if (qr.isDark(r, c)) {
      var x0 = Math.round((c + quiet) * s), y0 = Math.round((r + quiet) * s);
      x.fillRect(x0, y0, Math.round((c + quiet + 1) * s) - x0, Math.round((r + quiet + 1) * s) - y0);
    }
  }
  cv.setAttribute("role", "img");
  cv.setAttribute("aria-label", "Kode QR");
  cv.style.maxWidth = "100%"; cv.style.height = "auto";
  if (el) { el.innerHTML = ""; el.appendChild(cv); }
  this._el = cv;
}
QRCode.CorrectLevel = { L: ECL.L, M: ECL.M, Q: ECL.Q, H: ECL.H };
window.QRCode = QRCode;
