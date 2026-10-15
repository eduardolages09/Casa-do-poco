/* Casa do Poço — versão base (v5). A foto do hero nunca é transformada. Sem dependências além do Lenis (scroll suave). */
(function () {
  'use strict';

  var reduzido = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var raiz = document.documentElement;
  var topo = document.getElementById('topo');
  var hero = document.querySelector('.hero');
  var vh = window.innerHeight;
  var vw = window.innerWidth;

  function limitar(v, a, b) { return Math.min(b, Math.max(a, v)); }
  function suave(t) { return t * t * (3 - 2 * t); }
  function sai(t) { return 1 - Math.pow(1 - t, 3); }
  function dois(n) { return (n < 10 ? '0' : '') + n; }
  function lista(sel, dentro) { return Array.prototype.slice.call((dentro || document).querySelectorAll(sel)); }
  function estreito() { return vw <= 760; }

  /* ============ SCROLL SUAVE ============ */
  var lenis = null;
  if (!reduzido && window.Lenis) {
    lenis = new window.Lenis({ lerp: 0.085, smoothWheel: true });
    raiz.classList.add('lenis');
    var correr = function (t) { lenis.raf(t); requestAnimationFrame(correr); };
    requestAnimationFrame(correr);
  }
  function scrollY() { return window.scrollY || window.pageYOffset; }
  function irParaY(y, dur) {
    if (lenis) lenis.scrollTo(y, { duration: dur || 1.4 });
    else window.scrollTo({ top: y, behavior: reduzido ? 'auto' : 'smooth' });
  }
  function saltarPara(y) {
    if (lenis) { lenis.resize(); lenis.scrollTo(y, { immediate: true, force: true }); }
    else window.scrollTo(0, y);
  }

  /* ============ NÉVOA ============
     A frase de abertura (e a da quebra) sai de uma nuvem: cada palavra passa
     de desfocada e transparente a nítida, em onda, ligada diretamente ao
     scroll (sem transições que fiquem para trás). */
  var nevoas = lista('[data-nevoa]').map(function (el) {
    var palavras = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    var spans = palavras.map(function (p, i) {
      var s = document.createElement('span');
      s.className = 'nv';
      s.textContent = p;
      el.appendChild(s);
      if (i < palavras.length - 1) el.appendChild(document.createTextNode(' '));
      return s;
    });
    return { el: el, spans: spans };
  });
  function nevoa() {
    nevoas.forEach(function (n) {
      var r = n.el.getBoundingClientRect();
      var ini = vh * 0.95, fim = vh * (estreito() ? 0.38 : 0.45);
      var p = reduzido ? 1 : limitar((ini - r.top) / (ini - fim), 0, 1);
      var N = n.spans.length, janela = 0.42;
      n.spans.forEach(function (s, i) {
        var q = sai(limitar((p - (i / Math.max(1, N - 1)) * (1 - janela)) / janela, 0, 1));
        if (q !== s._q) { s._q = q; s.style.setProperty('--p', q.toFixed(3)); }
      });
    });
  }

  /* ============ HERO ============ */
  var heroFoto = document.querySelector('.hero__foto');
  function pronto() { requestAnimationFrame(function () { raiz.classList.add('is-pronto'); }); }
  if (heroFoto.complete) pronto();
  else { heroFoto.addEventListener('load', pronto); heroFoto.addEventListener('error', pronto); setTimeout(pronto, 1800); }

  /* ============ SECÇÕES PRESAS ============
     Avançam com o scroll, foto a foto, só na primeira descida; depois de
     passar a secção, ela encolhe para um ecrã e passa a ter setas.
       cortina  (exterior)  cada foto sobe por cima da anterior
       piscina              a vista aérea abre-se; as outras esvaem-se por cima
       portas   (interior)  a foto seguinte entra da direita, a imagem a metade da velocidade
       regiao               a foto entra da direita por cima da anterior */
  var presas = lista('[data-presa]').map(function (sec) {
    var g = {
      sec: sec,
      tipo: sec.getAttribute('data-presa'),
      fotos: lista('.presa__foto', sec),
      legendas: lista('.legenda', sec),
      botoes: lista('[data-ir]', sec),
      conta: sec.querySelector('[data-conta]'),
      setas: sec.querySelector('.presa__setas'),
      abre: sec.querySelector('[data-abre]'),
      abreTexto: sec.querySelector('[data-abre-texto]'),
      solta: false, t: 0, a: 1, ativa: -1, anim: null
    };
    g.n = g.fotos.length;
    g.intro = g.tipo === 'piscina' ? 110 : 0;   // em svh: o curso da moldura a abrir-se
    if (g.tipo === 'piscina') g.a = 0;
    sec.style.setProperty('--n', g.n);
    sec.style.setProperty('--intro', g.intro);
    return g;
  });

  // as fotos de cada secção descarregam todas quando ela se aproxima
  (function () {
    var carregar = function (sec) { lista('img', sec).forEach(function (i) { i.loading = 'eager'; }); };
    if (!('IntersectionObserver' in window)) { presas.forEach(function (g) { carregar(g.sec); }); return; }
    var perto = new IntersectionObserver(function (en) {
      en.forEach(function (e) { if (e.isIntersecting) { carregar(e.target); perto.unobserve(e.target); } });
    }, { rootMargin: '1200px 0px' });
    presas.forEach(function (g) { perto.observe(g.sec); });
  })();

  function abrir_moldura(g, a) {
    g.a = a;
    if (!g.abre) return;
    var e = sai(a);
    if (estreito()) {
      g.abre.style.setProperty('--in-x', ((1 - e) * 9).toFixed(2) + '%');
      g.abre.style.setProperty('--in-y', ((1 - e) * 11).toFixed(2) + '%');
    } else {
      g.abre.style.setProperty('--in-x', ((1 - e) * 16).toFixed(2) + 'vw');
      g.abre.style.setProperty('--in-y', ((1 - e) * 14).toFixed(2) + 'vh');
    }
    // a vista aérea começa a 1,16× e assenta a 1× (usa o ficheiro de 2560 px)
    g.fotos[0].firstElementChild.style.transform = 'scale(' + (1.16 - 0.16 * e).toFixed(4) + ')';
    if (g.abreTexto) g.abreTexto.style.setProperty('--txt', limitar((a - 0.55) / 0.4, 0, 1).toFixed(3));
  }

  function desenhar(g, t) {
    g.t = t;
    for (var k = 1; k < g.n; k++) {
      var f = g.fotos[k], el = f.firstElementChild;
      var r = limitar(t - (k - 1), 0, 1);
      if (g.tipo === 'cortina') {
        f.style.clipPath = 'inset(' + ((1 - r) * 100).toFixed(2) + '% 0 0 0)';
        el.style.transform = 'translate3d(0,' + ((1 - r) * 14).toFixed(2) + '%,0)';
      } else if (g.tipo === 'portas') {
        f.style.transform = 'translate3d(' + ((1 - r) * 100).toFixed(2) + '%,0,0)';
        el.style.transform = 'translate3d(' + (-(1 - r) * 50).toFixed(2) + '%,0,0)';
      } else if (g.tipo === 'piscina') {
        f.style.opacity = r.toFixed(3);
        el.style.transform = 'scale(' + (1.08 - 0.08 * r).toFixed(4) + ')';
      } else {   // regiao
        f.style.clipPath = 'inset(0 0 0 ' + ((1 - r) * 100).toFixed(2) + '%)';
        el.style.transform = 'scale(' + (1.1 - 0.1 * r).toFixed(4) + ')';
        el.style.transformOrigin = '0 50%';
      }
      f.style.visibility = r > 0 ? 'visible' : 'hidden';
    }
    var a = Math.round(t);
    if (a !== g.ativa) {
      g.ativa = a;
      g.legendas.forEach(function (l, i) { l.classList.toggle('is-ativa', i === a); });
      g.botoes.forEach(function (b, i) { b.setAttribute('aria-selected', i === a ? 'true' : 'false'); });
      if (g.conta) g.conta.textContent = dois(a + 1);
      if (g.setas) {
        g.setas.querySelector('[data-ant]').disabled = a === 0;
        g.setas.querySelector('[data-seg]').disabled = a === g.n - 1;
      }
    }
    g.sec.style.setProperty('--prog', g.n > 1 ? (t / (g.n - 1)).toFixed(3) : 1);
  }

  // encolhe a secção para um ecrã sem mexer no que se está a ver
  function soltar(g, compensar) {
    var antes = g.sec.offsetHeight;
    g.sec.classList.add('is-solta');
    var depois = g.sec.offsetHeight;
    g.solta = true;
    if (g.setas) g.setas.hidden = false;
    abrir_moldura(g, 1);
    return compensar ? antes - depois : 0;
  }

  function irPara_foto(g, alvo) {
    alvo = limitar(alvo, 0, g.n - 1);
    var de = g.t, ini = null, dur = reduzido ? 1 : 1100;
    if (g.anim) cancelAnimationFrame(g.anim);
    var passo = function (agora) {
      if (ini === null) ini = agora;
      var p = limitar((agora - ini) / dur, 0, 1);
      desenhar(g, de + (alvo - de) * sai(p));
      if (p < 1) g.anim = requestAnimationFrame(passo);
    };
    g.anim = requestAnimationFrame(passo);
  }

  presas.forEach(function (g) {
    if (g.setas) {
      g.setas.querySelector('[data-ant]').addEventListener('click', function () { irPara_foto(g, g.ativa - 1); });
      g.setas.querySelector('[data-seg]').addEventListener('click', function () { irPara_foto(g, g.ativa + 1); });
    }
    // região: os nomes também escolhem o lugar (no 1.º percurso levam o scroll lá)
    g.botoes.forEach(function (b, i) {
      b.addEventListener('click', function () {
        if (g.solta) { irPara_foto(g, i); return; }
        var curso = g.sec.offsetHeight - vh;
        var topoSec = g.sec.getBoundingClientRect().top + scrollY();
        irParaY(topoSec + curso * (i + 0.5) / g.n, 1);
      });
    });
  });

  function presaScroll(g) {
    if (g.solta) return;
    var r = g.sec.getBoundingClientRect();
    var curso = g.sec.offsetHeight - vh;
    var introPx = g.intro / 100 * vh;
    var px = -r.top;
    if (g.intro) abrir_moldura(g, reduzido ? 1 : limitar(px / introPx, 0, 1));
    var bruto = limitar((px - introPx) / Math.max(1, curso - introPx), 0, 1) * (g.n - 1);
    var k = Math.min(Math.floor(bruto), g.n - 2);
    var f = bruto - k;
    // cada passo: um momento parado, a troca, outro momento parado
    var t = g.n < 2 ? 0 : (reduzido ? Math.round(bruto) : k + suave(limitar((f - 0.16) / 0.68, 0, 1)));
    desenhar(g, t);
    if (r.bottom < 0) saltarPara(scrollY() - soltar(g, true));
  }

  /* ============ QUARTOS ============
     Adaptado do 145 Townhouse: primeiro a entrada (o título grande); depois a
     pista, que na 1.ª descida fica presa. O scroll percorre as fotos de cada
     quarto (o quarto e a sua casa de banho); o nome muda quando muda o quarto
     e a barra do separador enche-se com as fotos dele. Passada a secção,
     solta-se (o scroll compensa a altura que sai) e muda-se com os
     separadores, as setas ou o dedo. */
  var qsec = document.querySelector('[data-quartos]');
  var qpista = qsec.querySelector('.quartos__pista');
  var qfotos = lista('.qfoto', qsec);
  var qtextos = lista('.qtexto', qsec);
  var qabas = lista('[data-qir]', qsec);
  var qsegs = lista('.quartos__seg span', qsec);
  var qabre = qsec.querySelector('.quartos__abre');
  var qpassos = lista('[data-qpasso]', qsec);
  var NQ = qfotos.length;
  var Q = { presa: !reduzido, i: -1, q: -1, passo: 0.55 };
  var qinicio = [];   // a primeira foto de cada quarto (e o fim da última)
  qfotos.forEach(function (f, k) { var q = +f.getAttribute('data-q'); if (qinicio[q] === undefined) qinicio[q] = k; });
  qinicio.push(NQ);
  if (reduzido) qsec.classList.add('is-livre');

  function encheQuartos(p) {
    qsegs.forEach(function (sg, k) {
      var a = qinicio[k], b = qinicio[k + 1];
      sg.style.transform = 'scaleX(' + limitar((p - a) / (b - a), 0, 1).toFixed(4) + ')';
    });
  }
  function mostraFoto(i) {
    i = limitar(i, 0, NQ - 1);
    if (!Q.presa) {
      encheQuartos(i + 1);
      qpassos.forEach(function (b) { b.disabled = +b.getAttribute('data-qpasso') < 0 ? i === 0 : i === NQ - 1; });
    }
    if (i === Q.i) return;
    Q.i = i;
    var f = qfotos[i], q = +f.getAttribute('data-q');
    qfotos.forEach(function (x, k) { x.classList.toggle('is-atual', k === i); });
    qabre.setAttribute('data-serie', f.getAttribute('data-serie-f'));
    qabre.setAttribute('data-foto', f.getAttribute('data-f'));
    if (q === Q.q) return;
    Q.q = q;
    qtextos.forEach(function (t, k) { t.classList.toggle('is-atual', k === q); });
    qabas.forEach(function (b, k) { b.setAttribute('aria-pressed', k === q ? 'true' : 'false'); });
  }
  function medeQuartos() {
    qpista.style.height = Q.presa ? (vh * (1 + NQ * Q.passo)) + 'px' : '';
  }
  // encolhe a pista para um ecrã; devolve a altura que saiu
  function soltaQuartos(compensar) {
    if (!Q.presa) return 0;
    var antes = qsec.offsetHeight;
    Q.presa = false;
    qsec.classList.add('is-livre');
    medeQuartos();
    mostraFoto(Q.i < 0 ? 0 : Q.i);
    return compensar ? antes - qsec.offsetHeight : 0;
  }
  function atualizaQuartos() {
    if (!Q.presa) return;
    var r = qpista.getBoundingClientRect();
    if (r.bottom < -10) { saltarPara(scrollY() - soltaQuartos(true)); return; }
    if (r.top > vh + 50 || r.bottom < -50) return;
    var p = limitar(-r.top / Math.max(1, r.height - vh), 0, 1) * NQ;
    encheQuartos(p);
    mostraFoto(Math.min(NQ - 1, Math.floor(p)));
  }
  qabas.forEach(function (b) {
    b.addEventListener('click', function () {
      var k = +b.getAttribute('data-qir');
      if (!Q.presa) return mostraFoto(qinicio[k]);
      var y = qpista.getBoundingClientRect().top + scrollY() + (qinicio[k] + 0.05) / NQ * (qpista.offsetHeight - vh);
      irParaY(y, 1);
    });
  });
  qpassos.forEach(function (b) {
    b.addEventListener('click', function () { mostraFoto(Q.i + +b.getAttribute('data-qpasso')); });
  });
  var qx = null, qy = 0;
  qabre.addEventListener('touchstart', function (e) { qx = e.touches[0].clientX; qy = e.touches[0].clientY; }, { passive: true });
  qabre.addEventListener('touchend', function (e) {
    if (qx === null || Q.presa) return;
    var dx = e.changedTouches[0].clientX - qx, dy = e.changedTouches[0].clientY - qy;
    qx = null;
    if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.4) { e.preventDefault(); mostraFoto(Q.i + (dx < 0 ? 1 : -1)); }
  });
  // as fotos dos quartos descarregam quando a secção se aproxima
  if ('IntersectionObserver' in window) {
    var qperto = new IntersectionObserver(function (en) {
      if (en[0].isIntersecting) { lista('img', qsec).forEach(function (i) { i.loading = 'eager'; }); qperto.disconnect(); }
    }, { rootMargin: '1200px 0px' });
    qperto.observe(qsec);
  }
  medeQuartos();
  mostraFoto(0);

  /* ============ COMODIDADES ============
     Como no Solar Antigo: a faixa anda sozinha para a esquerda, devagar, e
     não acaba (a lista está duplicada; a meio do percurso volta-se ao
     princípio e a emenda cai fora do ecrã). Quem arrastar ou deslizar
     manda: o movimento pára durante o gesto e retoma a seguir. Mexe-se em
     scrollLeft, para o deslize nativo do telemóvel continuar a funcionar. */
  (function () {
    var pista = document.querySelector('[data-comod-pista]');
    var fila = document.querySelector('[data-comod-lista]');
    if (!pista || !fila || reduzido) return;
    var VELOCIDADE = 24;          // px por segundo (igual a 60 e a 120 Hz)
    var pausa = 0, sobre = false, anterior = null;
    var pos = pista.scrollLeft;   // em decimal: o scrollLeft é truncado em ecrãs 1×
    var volta = fila.scrollWidth / 2;
    var visivel = false, aCorrer = false;
    function ligar() { if (aCorrer) return; aCorrer = true; anterior = null; requestAnimationFrame(andar); }
    function andar(agora) {
      if (!visivel) { aCorrer = false; return; }
      if (anterior === null) anterior = agora;
      var ms = Math.min(agora - anterior, 100);
      anterior = agora;
      if (sobre || pausa > 0) {
        if (pausa > 0) pausa -= ms;
        pos = pista.scrollLeft;
      } else {
        pos += VELOCIDADE * ms / 1000;
        if (volta > 0) { if (pos >= volta) pos -= volta; else if (pos < 0) pos += volta; }
        pista.scrollLeft = pos;
      }
      requestAnimationFrame(andar);
    }
    window.addEventListener('resize', function () { volta = fila.scrollWidth / 2; });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) {
        visivel = e[0].isIntersecting;
        if (visivel) { volta = fila.scrollWidth / 2; ligar(); }
      }).observe(pista);
    } else { visivel = true; ligar(); }

    function suspender() { pausa = 1500; }
    pista.addEventListener('wheel', suspender, { passive: true });
    pista.addEventListener('touchstart', suspender, { passive: true });
    pista.addEventListener('touchmove', suspender, { passive: true });
    pista.addEventListener('touchend', function () { pausa = 2500; }, { passive: true });
    pista.addEventListener('mouseenter', function () { sobre = true; });
    pista.addEventListener('mouseleave', function () { sobre = false; });
    pista.addEventListener('focusin', function () { sobre = true; });
    pista.addEventListener('focusout', function () { sobre = false; });
    window.addEventListener('blur', function () { sobre = false; });

    // arrastar com o rato (no telemóvel o dedo já chega)
    var agarrado = false, partidaX = 0, partidaScroll = 0;
    pista.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'touch') return;
      agarrado = true; partidaX = e.clientX; partidaScroll = pista.scrollLeft;
      pista.classList.add('is-agarrada');
      pista.setPointerCapture(e.pointerId);
    });
    pista.addEventListener('pointermove', function (e) {
      if (!agarrado) return;
      e.preventDefault();
      pista.scrollLeft = partidaScroll - (e.clientX - partidaX);
    });
    function largar(e) {
      if (!agarrado) return;
      agarrado = false;
      pista.classList.remove('is-agarrada');
      try { pista.releasePointerCapture(e.pointerId); } catch (err) {}
    }
    pista.addEventListener('pointerup', largar);
    pista.addEventListener('pointercancel', largar);
  })();

  /* ============ ENTRADA E SAÍDA DAS FOTOS ============
     Cada moldura abre-se e sobe ao entrar no ecrã (um recorte que se alarga)
     e, ao sair por cima, recua e esvai-se. Ligado diretamente ao scroll. O
     progresso mede-se no pai (o palco), que não se mexe com a transformação.
     A foto do fecho entra com um zoom que assenta. A do hero nunca mexe. */
  var entradas = [
    ['.exterior__moldura', 'moldura'], ['.interior__moldura', 'moldura'], ['.quartos__foto', 'moldura'],
    ['.regiao__moldura', 'moldura'], ['.piscina__moldura', 'sai'], ['.fecho__foto', 'zoom']
  ].map(function (d) {
    var el = document.querySelector(d[0]);
    return el && { el: el, pai: el.parentElement, tipo: d[1], e: -1, s: -1 };
  }).filter(Boolean);
  function entraSai() {
    entradas.forEach(function (x) {
      var r = x.pai.getBoundingClientRect();
      if (r.top > vh + 20 || r.bottom < -20) return;
      var e = reduzido ? 1 : sai(limitar((vh - r.top) / (vh * 0.7), 0, 1));
      var sa = reduzido ? 0 : limitar((vh * 0.85 - r.bottom) / (vh * 0.85), 0, 1);
      if (x.tipo === 'zoom') {
        if (e === x.e) return;
        x.e = e;
        x.el.style.transform = 'scale(' + (1 + (1 - e) * 0.14).toFixed(4) + ')';
        return;
      }
      if (x.tipo === 'sai') e = 1;
      if (e === x.e && sa === x.s) return;
      x.e = e; x.s = sa;
      var a = 1 - e;
      x.el.style.clipPath = a > 0.001 ? 'inset(' + (a * 10).toFixed(2) + '% ' + (a * 8).toFixed(2) + '%)' : '';
      x.el.style.transform = (a > 0.001 || sa > 0.001)
        ? 'translate3d(0,' + (a * 80 - sa * 50).toFixed(1) + 'px,0) scale(' + (1 - sa * 0.08).toFixed(4) + ')' : '';
      x.el.style.opacity = sa > 0.001 ? (1 - sa * 0.6).toFixed(3) : '';
    });
  }


  /* ============ LIGAÇÕES DO MENU ============
     Antes de ir para uma secção, soltam-se as secções presas que ficam pelo
     caminho, para o destino não fugir durante a viagem. */
  lista('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (id.length < 2) return;
      var alvo = document.querySelector(id);
      if (!alvo) return;
      e.preventDefault();
      var y = scrollY(), desvio = 0;
      presas.forEach(function (g) {
        if (g.solta || g.sec === alvo) return;
        if (!(g.sec.compareDocumentPosition(alvo) & Node.DOCUMENT_POSITION_FOLLOWING)) return;
        var acima = g.sec.getBoundingClientRect().top + y < y;
        var d = soltar(g, true);
        desenhar(g, g.n - 1);
        if (acima) desvio += d;
      });
      if (Q.presa && alvo !== qsec && (qsec.compareDocumentPosition(alvo) & Node.DOCUMENT_POSITION_FOLLOWING)) {
        var qAcima = qsec.getBoundingClientRect().top < 0;
        var dq = soltaQuartos(true);
        mostraFoto(NQ - 1);
        if (qAcima) desvio += dq;
      }
      if (desvio) saltarPara(y - desvio);
      irParaY(alvo.getBoundingClientRect().top + scrollY());
    });
  });

  /* ============ A CADA SCROLL ============ */
  function atualizar() {
    topo.classList.toggle('is-solido', scrollY() > hero.offsetHeight - 90);
    nevoa();
    presas.forEach(presaScroll);
    atualizaQuartos();
    entraSai();
  }
  var pedido = false;
  function agendar() {
    if (pedido) return;
    pedido = true;
    requestAnimationFrame(function () { pedido = false; atualizar(); });
  }
  if (lenis) lenis.on('scroll', agendar);
  window.addEventListener('scroll', agendar, { passive: true });
  window.addEventListener('resize', function () {
    vh = window.innerHeight; vw = window.innerWidth;
    medeQuartos();
    presas.forEach(function (g) { if (g.intro) abrir_moldura(g, g.solta ? 1 : g.a); });
    agendar();
  });
  presas.forEach(function (g) { desenhar(g, 0); if (g.intro) abrir_moldura(g, 0); });
  atualizar();

  /* ============ VISOR (originais, na resolução máxima) ============
     Cada quarto abre só as suas fotos: o quarto e a casa de banho dele. */
  var IMG = 'assets/img/';
  var SERIES = {
    quarto1: { titulo: 'Quarto 1', fotos: [['quarto-1.jpg', 'Quarto 1 · cama de casal'], ['wc-1.jpg', 'Quarto 1 · casa de banho privativa']] },
    quarto2: { titulo: 'Quarto 2', fotos: [['quarto-2.jpg', 'Quarto 2 · cama de casal'], ['wc-2.jpg', 'Quarto 2 · casa de banho privativa']] },
    quarto3: { titulo: 'Quarto 3', fotos: [['quarto-3.jpg', 'Quarto 3 · cama de casal'], ['wc-3.jpg', 'Quarto 3 · casa de banho privativa']] },
    quarto4: { titulo: 'Quarto 4', fotos: [['quarto-4.jpg', 'Quarto 4 · duas camas de solteiro'], ['wc-4.jpg', 'Quarto 4 · casa de banho privativa']] }
  };

  var visor = document.getElementById('visor');
  var vImg = document.getElementById('visorImg');
  var vTitulo = document.getElementById('visorTitulo');
  var vConta = document.getElementById('visorConta');
  var vLegenda = document.getElementById('visorLegenda');
  var vAnt = document.getElementById('visorAnt');
  var vSeg = document.getElementById('visorSeg');
  var serie = null, indice = 0, origem = null;

  function mostrar() {
    var f = serie.fotos[indice];
    vImg.src = IMG + f[0];
    vImg.alt = f[1];
    vLegenda.textContent = f[1];
    vConta.textContent = serie.fotos.length > 1 ? (indice + 1) + ' / ' + serie.fotos.length : '';
    vAnt.hidden = vSeg.hidden = serie.fotos.length < 2;
  }
  function abrir(nome, i, botao) {
    serie = SERIES[nome];
    if (!serie) return;
    indice = i || 0;
    origem = botao;
    vTitulo.textContent = serie.titulo;
    mostrar();
    visor.hidden = false;
    if (lenis) lenis.stop();
    document.body.style.overflow = 'hidden';
    document.getElementById('visorFechar').focus();
  }
  function fechar() {
    visor.hidden = true;
    if (lenis) lenis.start();
    document.body.style.overflow = '';
    if (origem) origem.focus({ preventScroll: true });
  }
  function passoVisor(d) {
    indice = (indice + d + serie.fotos.length) % serie.fotos.length;
    mostrar();
  }
  lista('.abre[data-serie], .quartos__abre').forEach(function (b) {
    b.addEventListener('click', function () { abrir(b.getAttribute('data-serie'), parseInt(b.getAttribute('data-foto'), 10), b); });
  });
  document.getElementById('visorFechar').addEventListener('click', fechar);
  vAnt.addEventListener('click', function () { passoVisor(-1); });
  vSeg.addEventListener('click', function () { passoVisor(1); });
  visor.addEventListener('click', function (e) { if (e.target === visor || e.target.classList.contains('visor__palco')) fechar(); });
  document.addEventListener('keydown', function (e) {
    if (visor.hidden) return;
    if (e.key === 'Escape') fechar();
    else if (e.key === 'ArrowLeft') passoVisor(-1);
    else if (e.key === 'ArrowRight') passoVisor(1);
  });
  var toqueX = null;
  visor.addEventListener('touchstart', function (e) { toqueX = e.touches[0].clientX; }, { passive: true });
  visor.addEventListener('touchend', function (e) {
    if (toqueX === null || !serie || serie.fotos.length < 2) return;
    var dx = e.changedTouches[0].clientX - toqueX;
    if (Math.abs(dx) > 50) passoVisor(dx < 0 ? 1 : -1);
    toqueX = null;
  });

  var ano = document.getElementById('ano');
  if (ano) ano.textContent = new Date().getFullYear();
})();
