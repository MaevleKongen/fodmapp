/* Språkvelgeren på fodmapp.com (runde rSpraak). Teksten står ferdig i HTML-en, per språk; js/i18n.js lastes ikke av sidene.
   Valget lagres i 'fodmapp-lang', så rotsidene (engelsk) sender deg til språket du har valgt. Lenkene virker uten JavaScript. */
(function(){
  'use strict';
  function overlay(){return document.getElementById('langOverlay')}
  window.openLangModal=function(){var o=overlay();if(o)o.classList.add('open')};
  window.closeLangModalForce=function(){var o=overlay();if(o)o.classList.remove('open')};
  window.closeLangModal=function(e){if(e&&e.target===overlay())window.closeLangModalForce()};
  var g=document.getElementById('langGrid');
  if(g)g.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[data-kode]');if(!a)return;
    try{localStorage.setItem('fodmapp-lang',a.getAttribute('data-kode'))}catch(x){}
    if(location.hash&&a.href.indexOf('#')<0)a.href+=location.hash;   // samme sted på siden i det nye språket
  });
})();
