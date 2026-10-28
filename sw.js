/* Service worker — ASTERID
 *
 * Berkas aplikasi yang besar TIDAK ikut precache saat install (supaya Chrome cepat menganggap situs siap dipasang);
 * ia diunduh ke cache segera setelah aktif dan pada pembukaan berikutnya.
 *
 * Strategi: "cache dulu, perbarui di latar belakang".
 *  - Setelah dibuka sekali, aplikasi berjalan offline.
 *  - Setiap kali dibuka, salinan di cache disajikan langsung, lalu diperiksa ulang ke server
 *    (permintaan bersyarat/ETag: bila tidak berubah, hampir tanpa data). Versi baru yang
 *    ditemukan dipakai pada pembukaan berikutnya.
 *
 * SAAT MENGUNGGAH VERSI BARU DENGAN NAMA BERKAS BERBEDA, ubah nama berkas di TIGA tempat:
 *   1) APP_FILE di bawah ini   2) index.html (konstanta APP_FILE)   3) tidak perlu mengubah manifest.
 * Bila nama berkas HTML tetap sama, tidak ada yang perlu diubah.
 */
const APP_FILE = 'ASTERID.html';
const CACHE = 'asterid-v1';
const CORE = [            // berkas kecil: dipasang saat install agar service worker cepat aktif
  'manifest.webmanifest',
  'icon-192.png',
  'icon-512.png',
  'maskable-512.png',
  'apple-touch-icon.png',
  'favicon.svg'
];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      return c.addAll(CORE.map(function (u) { return new Request(u, { cache: 'reload' }); }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
  precacheApp();                      // berkas aplikasi (besar) diunduh di latar belakang, tidak menahan aktivasi
});

function refresh(cache, req) {
  return fetch(req, { cache: 'no-cache' }).then(function (res) {
    if (res && res.status === 200) { return cache.put(req, res.clone()).then(function () { return res; }); }
    return res;
  });
}

var pending = null;
function precacheApp() {
  if (pending) return pending;
  pending = caches.open(CACHE).then(function (cache) {
    return cache.match(APP_FILE).then(function (hit) {
      return hit || refresh(cache, new Request(APP_FILE));
    });
  }).catch(function () {}).then(function () { pending = null; });
  return pending;
}

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  var url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  var key = req;
  if (req.mode === 'navigate' && /(\/|\/index\.html)$/.test(url.pathname)) {
    key = new Request(APP_FILE);            // "./" dan index.html langsung menyajikan aplikasi
  }
  if (url.pathname.indexOf(APP_FILE) === -1 && req.mode !== 'navigate') {
    e.waitUntil(precacheApp());             // permintaan kecil lain menjaga SW tetap hidup sampai berkas aplikasi tersimpan
  }

  e.respondWith(
    caches.open(CACHE).then(function (cache) {
      return cache.match(key).then(function (hit) {
        if (hit) {
          e.waitUntil(refresh(cache, key).catch(function () {}));
          return hit;
        }
        return refresh(cache, key);
      });
    }).catch(function () { return fetch(req); })
  );
});
