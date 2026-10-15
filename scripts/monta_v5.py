"""Monta o corpo da v5 do index.html (hero → região) a partir de listas.

Só para não escrever à mão dezenas de srcset. Substitui o bloco entre o
comentário do HERO e o do FECHO. Correr a partir da pasta da casa:
    py -I scripts/monta_v5.py
"""
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(AQUI), 'site')
IMG = os.path.join(SITE, 'assets', 'img')


def srcset(nome):
    """Todos os tamanhos que existem de uma foto, mais o original."""
    from PIL import Image
    larg = sorted(int(m.group(1)) for f in os.listdir(IMG)
                  for m in [re.fullmatch(re.escape(nome) + r'-(\d+)\.jpg', f)] if m)
    w, h = Image.open(os.path.join(IMG, nome + '.jpg')).size
    partes = [f'assets/img/{nome}-{lw}.jpg {lw}w' for lw in larg] + [f'assets/img/{nome}.jpg {w}w']
    meio = [lw for lw in larg if lw >= 1400] or [w]
    src = f'assets/img/{nome}-{meio[0]}.jpg' if larg and meio[0] != w else f'assets/img/{nome}.jpg'
    return src, ', '.join(partes), w, h


def img(nome, alt, sizes, extra=''):
    src, ss, w, h = srcset(nome)
    return (f'<img src="{src}" srcset="{ss}" sizes="{sizes}" alt="{alt}" '
            f'width="{w}" height="{h}" loading="lazy" decoding="async"{extra}>')


SETAS = '''<div class="presa__setas" hidden>
            <button type="button" data-ant aria-label="Anterior"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
            <button type="button" data-seg aria-label="Seguinte"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
          </div>'''


def conta(n):
    return f'<p class="presa__conta"><span data-conta>01</span><i></i><span>{n:02d}</span></p>'


# ---------------------------------------------------------------- exterior
EXTERIOR = [
    ('ext-fachada', 'A casa', 'Granito à vista e uma varanda sobre o pátio.',
     'A fachada de granito com o telhado novo, a varanda e as escadas sobre o pátio'),
    ('ext-patio', 'O pátio', 'Escadas de pedra entre a rocha da serra.',
     'O pátio de calçada, as escadas de granito, as rochas e os ciprestes'),
    ('ext-churrasco', 'A churrasqueira', 'Bancada de granito para as refeições lá fora.',
     'A bancada de granito com lava-loiça e o grelhador de inox'),
]

# ---------------------------------------------------------------- piscina
# a primeira é a vista aérea que se abre; as outras seguem-na, uma de cada vez
PISCINA = [
    ('aerea', 'Só para a casa, com espreguiçadeiras e guarda-sóis.',
     'A piscina vista de cima, com alguém a nadar, o telhado de telha, as espreguiçadeiras e os guarda-sóis'),
    ('ext-serra', 'A serra inteira à frente.',
     'A borda da piscina com espreguiçadeiras e um guarda-sol, os socalcos e a Serra da Freita ao fundo'),
    ('ext-jardim', 'O relvado à volta da água.',
     'O relvado e a piscina com espreguiçadeiras, um guarda-sol e um pufe'),
    ('pool-vidro', 'Através do vidro, o verde e a água.',
     'O relvado, uma laranjeira e a piscina vistos através de um vidro, com a serra ao fundo'),
    ('pool-vista', 'Da água, as casas da aldeia.',
     'Da piscina, as casas de granito da aldeia e a encosta em socalcos'),
    ('aerea-2', 'A casa e o jardim, vistos do céu.',
     'Vista aérea dos telhados da casa, do jardim e da piscina'),
]

# ---------------------------------------------------------------- interior
INTERIOR = [
    ('sala', 'A sala', 'Granito à vista e uma porta de vidro para o jardim.',
     'A sala: sofá verde, parede de granito com a televisão e luz indireta, e a porta de vidro para o jardim'),
    ('mesa', 'A mesa', 'Para as refeições todos juntos.',
     'A mesa de madeira, o sofá verde ao fundo, a parede de granito e a janela para o jardim'),
    ('cozinha', 'A cozinha', 'Totalmente equipada.',
     'A cozinha branca com forno e micro-ondas embutidos e um candeeiro linear sobre a mesa'),
]

# ---------------------------------------------------------------- quartos
# Cada quarto tem casa de banho privativa (AF-WC). A ligação de cada casa de
# banho a cada quarto segue a numeração da visita por fotos do Airbnb
# ("Quarto 1" ↔ "Casa de banho completa 1"): confirmar com o dono.
QUARTOS = [
    (1, 'cama de casal', 'quarto-1', 'wc-1', '1086 / 1448',
     'Quarto 1: cama de casal com cabeceira verde e parede de granito com janela',
     'Casa de banho do quarto 1: duche, lavatório de pousar, espelho redondo e mosaico hidráulico'),
    (2, 'cama de casal', 'quarto-2', 'wc-2', '1920 / 2560',
     'Quarto 2: a janela funda na parede de granito, com a aldeia lá fora, e a cama em primeiro plano',
     'Casa de banho do quarto 2: duche, sanita e parede de granito com um nicho antigo'),
    (3, 'cama de casal', 'quarto-3', 'wc-3', '',
     'Quarto 3: cama de casal, cabeceira verde e mesa de cabeceira de tronco',
     'Casa de banho do quarto 3: lavatório, duche com porta de vidro e janela'),
    (4, 'duas camas de solteiro', 'quarto-4', 'wc-4', '1920 / 2879',
     'Quarto 4: duas camas de solteiro com cabeceira verde e uma mesa de tronco entre elas',
     'Casa de banho do quarto 4: lavatório e sanita, com chão de mosaico hidráulico'),
]

# ------------------------------------------------------------ comodidades
# Só o que o Airbnb confirma. Ícones de traço fino, todos no mesmo desenho.
COMODIDADES = [
    ('Piscina privada', '<path d="M2 18.5c2 0 2.5-1.5 5-1.5s3 1.5 5 1.5 2.5-1.5 5-1.5 3 1.5 5 1.5"/><path d="M8 14.5V6a2.5 2.5 0 0 1 5 0M14 14.5V6a2.5 2.5 0 0 1 5 0M8 9.5h6"/>'),
    ('Espreguiçadeiras e guarda-sóis', '<path d="M3 11.5a9 9 0 0 1 18 0Z"/><path d="M12 11.5v7.5a2 2 0 0 0 4 0M12 2.5v.01"/>'),
    ('Churrasqueira', '<path d="M4 10h16a8 8 0 0 1-16 0Z"/><path d="M8.5 17l-2 4M15.5 17l2 4M12 18v3"/><path d="M9 3.5c-.8.8-.8 1.7 0 2.5M12.5 3.5c-.8.8-.8 1.7 0 2.5"/>'),
    ('Pátio e varanda', '<path d="M3 9h18M3 20h18M6 9v11M10 9v11M14 9v11M18 9v11"/>'),
    ('Cozinha equipada', '<path d="M4 9.4h16v4.8a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V9.4Z"/><path d="M4 9.4H2M20 9.4h2"/><path d="M9 6.4V4M12 6.4V4M15 6.4V4"/>'),
    ('Forno, placa e micro-ondas', '<rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M4 8h16M8 5.5h.01M12 5.5h.01M16 5.5h.01"/><rect x="7.5" y="11" width="9" height="7" rx=".8"/>'),
    ('Máquina de lavar loiça', '<rect x="4.2" y="2.8" width="15.6" height="18.4" rx="2"/><circle cx="12" cy="14" r="4"/><path d="M8 7h.01M11 7h.01"/>'),
    ('Máquina de café', '<path d="M4 9h12v5a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4V9Z"/><path d="M16 10.5h1.4a2.6 2.6 0 0 1 0 5.2H16"/><path d="M7.2 3v2.6M11 3v2.6"/>'),
    ('Ar condicionado', '<path d="M12 3v18M4.2 7.5l15.6 9M19.8 7.5l-15.6 9"/><path d="M9.6 4.9 12 7.3l2.4-2.4M9.6 19.1 12 16.7l2.4 2.4"/>'),
    ('Casa de banho em cada quarto', '<path d="M7 9h10l-1.7-3.4a2 2 0 0 0-1.8-1.1h-3a2 2 0 0 0-1.8 1.1L7 9Z"/><path d="M12 4.5V2.8"/><path d="M9.2 12.6h.01M12 12.6h.01M14.8 12.6h.01M10.6 16.2h.01M13.4 16.2h.01M12 19.8h.01"/>'),
    ('Roupa de cama de algodão', '<path d="M2.8 19.4V7"/><path d="M2.8 13.6h15.6a2.6 2.6 0 0 1 2.6 2.6v3.2"/><path d="M2.8 16.8h18.2"/><path d="M6.4 13.6v-2.4a1 1 0 0 1 1-1h3.6a1 1 0 0 1 1 1v2.4"/>'),
    ('Secador de cabelo', '<path d="M4 9a5 5 0 0 1 5-5h10v10H9a5 5 0 0 1-5-5Z"/><circle cx="9" cy="9" r="1.6"/><path d="M11 14l-1.2 7h3.2l1.2-7"/>'),
    ('Wi-Fi', '<path d="M2.5 9.3a15 15 0 0 1 19 0"/><path d="M5.6 13a10.4 10.4 0 0 1 12.8 0"/><path d="M8.7 16.6a6 6 0 0 1 6.6 0"/><path d="M12 20.2h.01"/>'),
    ('Televisão e livros', '<rect x="2.6" y="4" width="18.8" height="12.4" rx="2"/><path d="M8 20.4h8"/><path d="M12 16.4v4"/>'),
    ('Entrada privada', '<circle cx="7.4" cy="12" r="4.3"/><circle cx="7.4" cy="12" r="1.5"/><path d="M11.7 12h9.5"/><path d="M17.4 12v3.4M20.6 12v2.8"/>'),
    ('Estacionamento gratuito', '<rect x="3.5" y="3.5" width="17" height="17" rx="3"/><path d="M10 17V7h3.5a3 3 0 0 1 0 6H10"/>'),
]

REGIAO = [
    ('regiao-freita', 'Serra da Freita', 'Planalto, urze e vales em socalcos.',
     'A Serra da Freita com urze em flor e, ao fundo, um vale com uma aldeia em socalcos', ''),
    ('regiao-frecha', 'Frecha da Mizarela', 'Uma das quedas de água mais altas do país.',
     'A garganta da serra com a queda de água da Frecha da Mizarela', ' style="object-position:66% 50%"'),
    ('regiao-drave', 'Aldeia de Drave', 'Casas de xisto no fundo de um vale.',
     'As casas de xisto da aldeia de Drave, com a encosta coberta de urze', ''),
    ('regiao-paiva', 'Passadiços do Paiva', 'Ao longo do rio Paiva, entre rochas.',
     'Os Passadiços do Paiva a subir a encosta entre rochas', ''),
]


def corpo():
    o = []
    o.append('''  <!-- ============ HERO ============
       A piscina elevada com a casa e a aldeia atrás (piscina-02): o ficheiro
       original (2560×1707, sem recompressão nem srcset), inteiro, na sua
       proporção 3:2 e sem nenhuma transformação. O nome em Della Respira, uma
       romana clássica de caixa mista, em baixo à esquerda. -->
  <section class="hero" id="inicio" aria-labelledby="hero-titulo">
    <img class="hero__foto" src="assets/img/hero.jpg" alt="A piscina elevada de borda branca, o relvado com espreguiçadeiras e a casa de granito, com as casas da aldeia atrás" width="2560" height="1707" fetchpriority="high" decoding="async">
    <div class="hero__texto">
      <h1 class="hero__nome" id="hero-titulo"><span class="hero__linha"><span>Casa do</span></span><span class="hero__linha"><span>Poço</span></span></h1>
      <p class="hero__onde"><span>Aldeia da Felgueira</span><span>Serra da Freita, Vale de Cambra</span></p>
    </div>
  </section>

  <!-- ============ ABERTURA ============
       As palavras saem de uma névoa (desfoque que se dissipa), ligadas ao
       scroll (main.js, "NÉVOA"). -->
  <section class="abertura" id="abertura" aria-label="A casa">
    <p class="abertura__frase" data-nevoa>Na aldeia da Felgueira, no coração da Serra da Freita, há uma casa de granito com piscina, feita para dias longos com quem mais gosta, ao ritmo da aldeia.</p>
  </section>
''')

    # exterior
    o.append('''  <!-- ============ EXTERIOR ============
       Galeria presa: à esquerda o título e a legenda; à direita a moldura 3:2
       onde cada foto sobe por cima da anterior com o scroll (main.js,
       "SECÇÕES PRESAS", tipo cortina). Factos: AF-CHURRASQUEIRA. -->
  <section class="presa exterior" id="exterior" aria-labelledby="exterior-titulo" data-presa="cortina">
    <div class="presa__palco">
      <div class="presa__lado">
        <h2 class="titulo" id="exterior-titulo">Exterior</h2>
        <div class="presa__legendas" aria-live="polite">''')
    for i, (n, t, f, a) in enumerate(EXTERIOR):
        o.append(f'          <div class="legenda{" is-ativa" if i == 0 else ""}"><b>{t}</b><span>{f}</span></div>')
    o.append(f'''        </div>
        <div class="presa__pe">
          {conta(len(EXTERIOR))}
          {SETAS}
        </div>
      </div>
      <div class="presa__moldura exterior__moldura">''')
    for i, (n, t, f, a) in enumerate(EXTERIOR):
        o.append(f'        <figure class="presa__foto">{img(n, a, "(max-width: 760px) 100vw, 70vw")}</figure>')
    o.append('''      </div>
    </div>
  </section>

  <!-- ============ QUEBRA ============ -->
  <section class="quebra" aria-hidden="true">
    <p class="quebra__frase" data-nevoa>Acima do jardim, a piscina olha a serra.</p>
  </section>
''')

    # piscina
    o.append(f'''  <!-- ============ A PISCINA ============
       Secção presa. A vista aérea começa numa moldura arredondada e abre-se até
       ao ecrã inteiro; depois as outras fotos da piscina seguem-na, uma de cada
       vez, com o scroll (main.js, tipo piscina). Texto direto sobre a foto, sem
       caixa. No telemóvel a moldura abre-se até à largura do ecrã (6:5) e o
       texto fica por baixo. Nunca «aquecida», «salgada» nem «infinita». -->
  <section class="presa piscina" id="piscina" aria-labelledby="piscina-titulo" data-presa="piscina">
    <div class="presa__palco">
      <div class="piscina__moldura" data-abre>''')
    for i, (n, f, a) in enumerate(PISCINA):
        o.append(f'        <figure class="presa__foto">{img(n, a, "(max-width: 760px) 100vw, 100vw")}</figure>')
    o.append('''      </div>
      <div class="piscina__texto" data-abre-texto>
        <h2 class="piscina__titulo" id="piscina-titulo">A piscina</h2>
        <div class="presa__legendas" aria-live="polite">''')
    for i, (n, f, a) in enumerate(PISCINA):
        o.append(f'          <div class="legenda{" is-ativa" if i == 0 else ""}"><span>{f}</span></div>')
    o.append(f'''        </div>
        <div class="presa__pe">
          {conta(len(PISCINA))}
          {SETAS}
        </div>
      </div>
    </div>
  </section>
''')

    # interior
    o.append('''  <!-- ============ INTERIOR ============
       Galeria presa como portas de correr, numa moldura alta na proporção das
       fotos (3:2, nada cortado); o texto fica ao lado, sem caixa. São as três
       fotos que a casa tem das zonas comuns: a sala, a mesa e a cozinha.
       Factos: AF-COZINHA. -->
  <section class="presa interior" id="interior" aria-labelledby="interior-titulo" data-presa="portas">
    <div class="presa__palco">
      <div class="presa__moldura interior__moldura">''')
    for i, (n, t, f, a) in enumerate(INTERIOR):
        o.append(f'        <figure class="presa__foto">{img(n, a, "(max-width: 760px) 100vw, 75vw")}</figure>')
    o.append('''      </div>
      <div class="presa__lado">
        <h2 class="titulo" id="interior-titulo">Interior</h2>
        <div class="presa__legendas" aria-live="polite">''')
    for i, (n, t, f, a) in enumerate(INTERIOR):
        o.append(f'          <div class="legenda{" is-ativa" if i == 0 else ""}"><b>{t}</b><span>{f}</span></div>')
    o.append(f'''        </div>
        <div class="presa__pe">
          {conta(len(INTERIOR))}
          {SETAS}
        </div>
      </div>
    </div>
  </section>
''')

    # quartos
    o.append('''  <!-- ============ QUARTOS ============
       Um painel preso do tamanho do ecrã, no verde do sofá, adaptado do 145
       Townhouse mas mais simples (main.js, «QUARTOS»): à esquerda, numa
       coluna estreita, «Quartos» grande no topo (marca a mudança de secção),
       o nome do quarto em duas linhas que sobem e, em baixo, os separadores
       com a barra que se enche com o scroll (o quarto que se está a ver). À direita, a foto no formato original
       (3:2; as casas de banho ao alto ficam inteiras, ao centro), que se
       esvai e assenta a cada passo: o quarto e, a seguir, a sua casa de banho,
       identificada. Casa de banho de cada quarto pela numeração do Airbnb:
       confirmar com o dono. Factos: AF-CAMAS, AF-WC. -->
  <section class="quartos" id="quartos" aria-labelledby="quartos-titulo" data-quartos>
    <div class="quartos__pista">
    <div class="quartos__palco">
      <div class="quartos__lado">
        <h2 class="quartos__titulo" id="quartos-titulo">Quartos</h2>
        <div class="quartos__textos" aria-live="polite">''')
    for i, (k, camas, q, w, r, aq, aw) in enumerate(QUARTOS):
        o.append(f'          <div class="qtexto{" is-atual" if i == 0 else ""}" data-q="{i}"><h3 class="qtexto__nome"><span class="qlinha"><span>Quarto {k}</span></span> <span class="qlinha"><em>{camas}</em></span></h3></div>')
    o.append('''        </div>
        <ol class="quartos__abas" aria-label="Quartos">''')
    for i, (k, camas, q, w, r, aq, aw) in enumerate(QUARTOS):
        o.append(f'          <li><button type="button" data-qir="{i}" aria-pressed="{"true" if i == 0 else "false"}" aria-label="Quarto {k}"><span class="quartos__seg" aria-hidden="true"><span></span></span><b>{k:02d}</b></button></li>')
    o.append('''        </ol>
      </div>
      <div class="quartos__foto">
        <button type="button" class="quartos__abre" data-serie="quarto1" data-foto="0" aria-label="Ver o quarto em grande">''')
    for i, (k, camas, q, w, r, aq, aw) in enumerate(QUARTOS):
        o.append(f'          <span class="qfoto{" is-atual" if i == 0 else ""}" data-q="{i}" data-serie-f="quarto{k}" data-f="0">{img(q, aq, "(max-width: 760px) 100vw, 74vw")}</span>')
        alto = f' qfoto--alto" style="--r: {r}' if r else ''
        o.append(f'          <span class="qfoto{alto}" data-q="{i}" data-serie-f="quarto{k}" data-f="1">{img(w, aw, "(max-width: 760px) 70vw, 40vw" if r else "(max-width: 760px) 100vw, 74vw")}<span class="qfoto__nota">Casa de banho privativa</span></span>')
    o.append('''        </button>
        <div class="quartos__setas">
          <button type="button" data-qpasso="-1" aria-label="Fotografia anterior"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
          <button type="button" data-qpasso="1" aria-label="Fotografia seguinte"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
        </div>
      </div>
    </div>
    </div>
  </section>
''')

    # comodidades
    o.append('''  <!-- ============ COMODIDADES ============
       Como no Solar Antigo: uma faixa com cartões que anda sozinha, devagar,
       para a esquerda e não acaba (a lista está duplicada; main.js volta ao
       princípio a meio do percurso, onde a emenda não se vê). Arrasta-se com
       o rato ou o dedo, e pára enquanto o rato está por cima. Só o que a casa
       confirma (factos.md, lista do Airbnb). -->
  <section class="comodidades" id="comodidades" aria-labelledby="comodidades-titulo">
    <h2 class="titulo comodidades__titulo" id="comodidades-titulo">Comodidades</h2>
    <div class="comod-pista" data-comod-pista tabindex="0" role="group" aria-label="Comodidades, lista horizontal">
      <ul class="comod-lista" data-comod-lista>''')
    for vez in range(2):
        for nome, icone in COMODIDADES:
            esc = ' aria-hidden="true"' if vez else ''
            o.append(f'        <li class="comod"{esc}><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{icone}</svg><b>{nome}</b></li>')
    o.append('''      </ul>
    </div>
  </section>
''')

    # região
    o.append('''  <!-- ============ REGIÃO ============
       Secção presa: os quatro lugares avançam com o scroll, a foto entra da
       direita por cima da anterior (tipo regiao). Depois da primeira descida
       solta-se e os nomes passam a ser separadores. Fotos do Wikimedia
       Commons; créditos em creditos.html (rodapé). -->
  <section class="presa regiao" id="regiao" aria-labelledby="regiao-titulo" data-presa="regiao">
    <div class="presa__palco">
      <div class="presa__lado">
        <h2 class="titulo" id="regiao-titulo">Região</h2>
        <p class="frase">A Serra da Freita à porta: trilhos, cascatas e aldeias de pedra.</p>
        <ol class="regiao__lista" role="tablist" aria-label="Lugares da região">''')
    for i, (n, nome, linha, a, ex) in enumerate(REGIAO):
        o.append(f'          <li class="legenda{" is-ativa" if i == 0 else ""}"><button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" aria-controls="regiao-foto" data-ir="{i}"><span class="regiao__nome">{nome}</span><span class="regiao__linha">{linha}</span></button></li>')
    o.append('''        </ol>
      </div>
      <div class="presa__moldura regiao__moldura" id="regiao-foto" role="tabpanel">''')
    for i, (n, nome, linha, a, ex) in enumerate(REGIAO):
        o.append(f'        <figure class="presa__foto">{img(n, a, "(max-width: 760px) 100vw, 56vw", ex)}</figure>')
    o.append('''      </div>
    </div>
  </section>

''')
    return '\n'.join(o)


if __name__ == '__main__':
    p = os.path.join(SITE, 'index.html')
    s = open(p, encoding='utf-8').read()
    a = s.index('  <!-- ============ HERO ============')
    b = s.index('  <!-- ============ RESERVAR (FECHO) ============ -->')
    s = s[:a] + corpo() + s[b:]
    open(p, 'w', encoding='utf-8', newline='\n').write(s)
    print('ok', len(s))
