// Navigation (mobil)
(function () {
  var btn = document.querySelector('.nav-toggle'), nav = document.getElementById('nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
})();

// Umschalter für Diagramme (Aktie/EBIT, Umsatz/EBIT)
document.querySelectorAll('.seg-toggle').forEach(function (group) {
  var buttons = group.querySelectorAll('button');
  var head = group.closest('.chart-head');
  var title = head ? head.querySelector('h3') : null;
  buttons.forEach(function (b) {
    b.addEventListener('click', function () {
      buttons.forEach(function (o) {
        o.setAttribute('aria-pressed', o === b ? 'true' : 'false');
        var el = document.getElementById(o.dataset.show);
        if (el) el.hidden = o !== b;
      });
      if (title) title.textContent = b.dataset.title;
    });
  });
});

// Kontaktformular: Thema aus URL übernehmen, Nachricht als E-Mail vorbereiten
(function () {
  var form = document.getElementById('contact');
  if (!form) return;
  var params = new URLSearchParams(location.search);
  var sel = form.querySelector('#thema');
  if (params.get('thema')) {
    Array.prototype.forEach.call(sel.options, function (o) { if (o.text === params.get('thema')) sel.value = o.text; });
  }
  if (params.get('modell')) form.querySelector('#msg').value = 'Ich interessiere mich für eine Probefahrt mit dem ' + params.get('modell') + '.';
  var to = { 'Investor Relations': 'ir', 'Presse': 'presse' };
  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var notice = document.getElementById('notice');
    if (!form.checkValidity()) { notice.textContent = 'Bitte Name, gültige E-Mail und Nachricht angeben.'; return; }
    var box = (to[sel.value] || 'info') + '@tangerine-motors.example';
    var body = form.msg.value + '\n\n' + form.name.value + ' <' + form.mail.value + '>';
    location.href = 'mailto:' + box + '?subject=' + encodeURIComponent(sel.value + ' – Anfrage') + '&body=' + encodeURIComponent(body);
    notice.textContent = 'Ihr E-Mail-Programm wird geöffnet.';
  });
})();
