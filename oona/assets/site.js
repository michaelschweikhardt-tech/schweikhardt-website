(function(){
  // Slideshows (Autoplay wie im Original, pausiert außerhalb des Viewports / bei reduzierter Bewegung)
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.slideshow').forEach(function(s){
    var slides = s.querySelectorAll('.slide'), i = 0, visible = false, delay = +s.dataset.delay || 3000;
    if (slides.length < 2 || reduce) return;
    // Bilder der Slideshow vorladen, sobald sie in die Nähe kommt
    var io = new IntersectionObserver(function(e){
      visible = e[0].isIntersecting;
      if (visible) slides.forEach(function(sl){ var im = sl.querySelector('img'); if (im) im.loading = 'eager'; });
    }, {rootMargin: '400px'});
    io.observe(s);
    setInterval(function(){
      if (!visible || document.hidden) return;
      slides[i].classList.remove('on'); i = (i + 1) % slides.length; slides[i].classList.add('on');
    }, delay);
  });

  // Lightbox für zoombare Bilder
  var items = Array.prototype.slice.call(document.querySelectorAll('figure.zoom'));
  if (!items.length) return;
  var lb, img, cur = 0;
  function show(n){ cur = (n + items.length) % items.length; var f = items[cur]; img.src = f.dataset.full; img.alt = (f.querySelector('img')||{}).alt || ''; }
  function close(){ if (lb){ lb.remove(); lb = null; document.removeEventListener('keydown', key); } }
  function key(e){ if (e.key === 'Escape') close(); else if (e.key === 'ArrowRight') show(cur + 1); else if (e.key === 'ArrowLeft') show(cur - 1); }
  function open(n){
    lb = document.createElement('div'); lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true');
    img = document.createElement('img'); lb.appendChild(img);
    if (items.length > 1){
      [['prev','‹',-1],['next','›',1]].forEach(function(b){
        var bt = document.createElement('button'); bt.className = b[0]; bt.textContent = b[1]; bt.setAttribute('aria-label', b[0] === 'prev' ? 'Vorheriges Bild' : 'Nächstes Bild');
        bt.onclick = function(e){ e.stopPropagation(); show(cur + b[2]); }; lb.appendChild(bt);
      });
    }
    var x = document.createElement('button'); x.className = 'x'; x.textContent = '×'; x.setAttribute('aria-label', 'Schließen'); lb.appendChild(x);
    lb.onclick = close; document.body.appendChild(lb); document.addEventListener('keydown', key); show(n);
  }
  items.forEach(function(f, n){ f.addEventListener('click', function(e){ e.preventDefault(); open(n); }); });
})();
