/* Nettsiden 2.1.0 (20. okt 2026). Kilde: fodmapp-kode dsl/r80_data/nettside/r210/r210.js (kopieres av
   lag_nettside_210.py). Lastes etter js/i18n.js på index.html og manual.html.
   1) Sveipekaruseller på mobil (.karusell): piler og prikker under raden, bare når raden er bredere enn skjermen.
   2) Bryteren i kamerafanen (.kam-valg): viser matrett-, meny- eller kjøleskapstelefonen.
   3) Anmeldelser: «Oversatt fra …» vises bare når sitatet står på et annet språk enn originalen (data-orig).
   4) aria-label fra data-i18n-aria (applyLang i i18n.js setter bare innerHTML). */
(function(){
  'use strict';
  // currentLang er en global let i i18n.js (ikke en egenskap på window)
  function lang(){try{if(typeof currentLang!=='undefined'&&currentLang)return currentLang}catch(e){}
    try{return localStorage.getItem('fodmapp-lang')||'en'}catch(e){return 'en'}}
  function tekst(k,reserve){try{var t=T[lang()]||T.en;return (t&&t[k])||(T.en&&T.en[k])||reserve}catch(e){return reserve}}
  var PIL='<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 3L5 8l5 5"/></svg>';
  var PIL_H='<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3l5 5-5 5"/></svg>';

  /* 1) Karuseller */
  var karuseller=[];
  function synlige(k){return Array.prototype.filter.call(k.children,function(c){return c.offsetParent!==null||c.getClientRects().length})}
  function aktiv(k){var r=k.getBoundingClientRect(),midt=r.left+r.width/2,best=0,bd=1e9;
    synlige(k).forEach(function(c,i){var cr=c.getBoundingClientRect(),d=Math.abs(cr.left+cr.width/2-midt);if(d<bd){bd=d;best=i}});return best}
  function gaaTil(k,i){var barn=synlige(k);if(!barn.length)return;i=Math.max(0,Math.min(barn.length-1,i));
    var r=k.getBoundingClientRect(),cr=barn[i].getBoundingClientRect();
    k.scrollBy({left:(cr.left+cr.width/2)-(r.left+r.width/2),top:0,behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'})}
  function bygg(k){
    var nav=document.createElement('div');nav.className='karusell-nav';nav.hidden=true;
    nav.innerHTML='<button type="button" class="karusell-pil forrige">'+PIL+'</button><div class="karusell-prikker"></div><button type="button" class="karusell-pil neste">'+PIL_H+'</button>';
    k.parentNode.insertBefore(nav,k.nextSibling);
    var o={k:k,nav:nav,prikker:nav.querySelector('.karusell-prikker'),forrige:nav.querySelector('.forrige'),neste:nav.querySelector('.neste'),n:-1};
    o.forrige.addEventListener('click',function(){gaaTil(k,aktiv(k)-1)});
    o.neste.addEventListener('click',function(){gaaTil(k,aktiv(k)+1)});
    var plan=false;k.addEventListener('scroll',function(){if(plan)return;plan=true;requestAnimationFrame(function(){plan=false;merk(o)})},{passive:true});
    karuseller.push(o);return o}
  function merk(o){var i=aktiv(o.k),p=o.prikker.children;
    for(var j=0;j<p.length;j++){if(j===i)p[j].setAttribute('aria-current','true');else p[j].removeAttribute('aria-current')}
    o.forrige.disabled=i<=0;o.neste.disabled=i>=p.length-1}
  function oppdater(o){
    var mobil=matchMedia('(max-width:760px)').matches,barn=synlige(o.k),over=mobil&&o.k.scrollWidth>o.k.clientWidth+4&&barn.length>1;
    o.nav.hidden=!over;if(!over)return;
    if(o.n!==barn.length){o.prikker.innerHTML='';
      barn.forEach(function(c,i){var b=document.createElement('button');b.type='button';b.className='karusell-prikk';
        b.addEventListener('click',function(){gaaTil(o.k,i)});o.prikker.appendChild(b)});o.n=barn.length}
    var kort=tekst('web_f210_karusell_kort','Kort');
    Array.prototype.forEach.call(o.prikker.children,function(b,i){b.setAttribute('aria-label',kort+' '+(i+1))});
    o.forrige.setAttribute('aria-label',tekst('web_f210_karusell_forrige','Forrige'));
    o.neste.setAttribute('aria-label',tekst('web_f210_karusell_neste','Neste'));
    merk(o)}
  function alle(){karuseller.forEach(oppdater)}

  /* 2) Kamerafanen */
  function kamera(){
    document.querySelectorAll('.kam-valg').forEach(function(v){
      var scene=v.parentNode&&v.parentNode.querySelector('.fane-scene');if(!scene)return;   // bryteren står over panelet
      v.querySelectorAll('button[data-vis]').forEach(function(b){b.addEventListener('click',function(){
        var navn=b.getAttribute('data-vis');
        v.querySelectorAll('button[data-vis]').forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});
        scene.querySelectorAll('figure.stlf').forEach(function(f){f.hidden=f.getAttribute('data-tlf')!==navn});
        window.dispatchEvent(new Event('resize'))})})})}

  /* 3) Anmeldelser + 4) aria */
  function spraakting(){
    var l=lang();
    document.querySelectorAll('[data-orig]').forEach(function(kort){var ovs=kort.querySelector('.review-ovs');if(ovs)ovs.hidden=(kort.getAttribute('data-orig')===l)});
    var t=(typeof T!=='undefined'&&(T[l]||T.en))||{};
    document.querySelectorAll('[data-i18n-aria]').forEach(function(el){var a=t[el.getAttribute('data-i18n-aria')];if(a)el.setAttribute('aria-label',a)});
    alle()}

  function start(){
    document.querySelectorAll('.karusell').forEach(bygg);
    kamera();spraakting();
    if(typeof window.applyLang==='function'&&!window.applyLang._r210){var f=window.applyLang;
      window.applyLang=function(){var r=f.apply(this,arguments);spraakting();return r};window.applyLang._r210=true}
    var plan=false;function snart(){if(plan)return;plan=true;requestAnimationFrame(function(){plan=false;alle()})}
    window.addEventListener('resize',snart);window.addEventListener('load',snart);
    if('ResizeObserver' in window){var ro=new ResizeObserver(snart);karuseller.forEach(function(o){ro.observe(o.k)})}
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(snart)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();
