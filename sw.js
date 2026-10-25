// HistoKHB — service worker: la app abre sin conexión con lo ya visto.
const V='hk-v286';
const SHELL=['./','index.html','manifest.json','datos/indice.json','img/icono-192.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=='GET'||u.origin!==location.origin)return;
  // audios y láminas animadas: directos de la red, sin guardarlos en el móvil
  if(u.pathname.includes('/audio/')||u.pathname.includes('/img/vivas/'))return;
  // red primero (para ver siempre lo último), caché si no hay conexión
  // siempre pregunta al servidor si hay versión nueva (no usar la copia de 10 min del navegador)
  e.respondWith(fetch(e.request,{cache:'no-cache'}).then(r=>{const c=r.clone();caches.open(V).then(ca=>ca.put(e.request,c));return r;}).catch(()=>caches.match(e.request).then(r=>r||caches.match('index.html'))));
});
