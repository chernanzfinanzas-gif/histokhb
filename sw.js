// HistoKHB — service worker: la app abre sin conexión con lo ya visto.
const V='hk-v381'
const SHELL=['./','index.html','manifest.json','datos/indice.json','img/ammo-icono-192.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=='GET'||u.origin!==location.origin)return;
  // audios, láminas animadas y Viajes: directos de la red, sin guardarlos en el móvil
  if(u.pathname.includes('/viajes/'))return;
  if(u.pathname.endsWith('.pdf'))return;
  if(u.pathname.includes('/biblioteca/')||u.pathname.includes('/api/'))return; // Biblioteca y servidor: siempre de la red (la vista previa depende de la sesión) // los PDF de la Biblioteca, directos de la red
  if(u.pathname.includes('/audio/')||u.pathname.includes('/img/vivas/')||u.pathname.includes('/sonidos/'))return;
  // red primero (para ver siempre lo último), caché si no hay conexión
  // siempre pregunta al servidor si hay versión nueva (no usar la copia de 10 min del navegador)
  e.respondWith(fetch(e.request,{cache:'no-cache'}).then(r=>{const c=r.clone();caches.open(V).then(ca=>ca.put(e.request,c));return r;}).catch(()=>caches.match(e.request).then(r=>r||caches.match('index.html'))));
});
