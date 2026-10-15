"""Monta o corpo da v4 do index.html (hero → região) a partir de listas.

Só para não escrever à mão dezenas de srcset. Substitui o bloco entre o
comentário do HERO e o do FECHO. Correr a partir da pasta da casa:
    py -I scripts/monta_v4.py
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
    (1, 'Cama de casal', 'quarto-1', 'wc-1', '1086 / 1448',
     'Quarto 1: cama de casal com cabeceira verde e parede de granito com janela',
     'Casa de banho do quarto 1: duche, lavatório de pousar, espelho redondo e mosaico hidráulico'),
    (2, 'Cama de casal', 'quarto-2', 'wc-2', '1920 / 2560',
     'Quarto 2: a janela funda na parede de granito, com a aldeia lá fora, e a cama em primeiro plano',
     'Casa de banho do quarto 2: duche, sanita e parede de granito com um nicho antigo'),
    (3, 'Cama de casal', 'quarto-3', 'wc-3', '2560 / 1707; --h: .5',
     'Quarto 3: cama de casal, cabeceira verde e mesa de cabeceira de tronco',
     'Casa de banho do quarto 3: lavatório, duche com porta de vidro e janela'),
    (4, 'Duas camas de solteiro', 'quarto-4', 'wc-4', '1920 / 2879',
     'Quarto 4: duas camas de solteiro com cabeceira verde e uma mesa de tronco entre elas',
     'Casa de banho do quarto 4: lavatório e sanita, com chão de mosaico hidráulico'),
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
       proporção 3:2 e sem nenhuma transformação. O nome em Cinzel, uma romana
       de inscrição, como letra gravada no granito, em baixo à esquerda. -->
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
       Cada quarto com a sua casa de banho privativa (AF-WC): a foto do quarto
       numa moldura 3:2 e, por cima, num cartão com sombra, a casa de banho, no
       formato da sua foto. Avançam com o scroll, quarto a quarto (tipo
       quartos). Casa de banho de cada quarto pela numeração do Airbnb:
       confirmar com o dono. Factos: AF-CAMAS, AF-WC. -->
  <section class="presa quartos" id="quartos" aria-labelledby="quartos-titulo" data-presa="quartos">
    <div class="presa__palco">
      <div class="presa__lado">
        <h2 class="titulo titulo--claro" id="quartos-titulo">Quartos</h2>
        <p class="frase frase--clara">Quatro quartos, cada um com a sua casa de banho.</p>
        <div class="presa__legendas" aria-live="polite">''')
    for i, (k, camas, q, w, r, aq, aw) in enumerate(QUARTOS):
        o.append(f'          <div class="legenda{" is-ativa" if i == 0 else ""}"><b>Quarto {k}</b><span>{camas}<br>Casa de banho privativa</span></div>')
    o.append(f'''        </div>
        <div class="presa__pe">
          {conta(len(QUARTOS))}
          {SETAS}
        </div>
      </div>
      <div class="quartos__comp">
        <div class="presa__moldura quartos__moldura">''')
    for i, (k, camas, q, w, r, aq, aw) in enumerate(QUARTOS):
        o.append(f'          <figure class="presa__foto"><button type="button" class="abre" data-serie="quarto{k}" data-foto="0" aria-label="Ver o quarto {k} em grande">{img(q, aq, "(max-width: 760px) 80vw, 52vw")}</button></figure>')
    o.append('        </div>')
    for i, (k, camas, q, w, r, aq, aw) in enumerate(QUARTOS):
        o.append(f'        <figure class="quartos__banho" style="--r: {r}"><button type="button" class="abre" data-serie="quarto{k}" data-foto="1" aria-label="Ver a casa de banho do quarto {k} em grande">{img(w, aw, "(max-width: 760px) 50vw, 30vw")}</button></figure>')
    o.append('''      </div>
    </div>
  </section>
''')

    # comodidades
    o.append('''  <!-- ============ COMODIDADES ============
       Uma faixa em quatro colunas, por tema; só o que a casa confirma
       (factos.md, lista do Airbnb). -->
  <section class="comodidades" id="comodidades" aria-labelledby="comodidades-titulo">
    <h2 class="titulo titulo--pequeno" id="comodidades-titulo">Comodidades</h2>
    <div class="comodidades__colunas">
      <div class="comodidades__col">
        <h3><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M2 18.5c2 0 2.5-1.5 5-1.5s3 1.5 5 1.5 2.5-1.5 5-1.5 3 1.5 5 1.5"/><path d="M8 14.5V6a2.5 2.5 0 0 1 5 0M14 14.5V6a2.5 2.5 0 0 1 5 0M8 9.5h6"/></svg>Exterior</h3>
        <ul><li>Piscina privada</li><li>Espreguiçadeiras e guarda-sóis</li><li>Churrasqueira com grelha e utensílios</li><li>Pátio e varanda</li></ul>
      </div>
      <div class="comodidades__col">
        <h3><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M4 9h16M8 6h.01M12 6h.01M16 6h.01M8 13h8v5H8z"/></svg>Cozinha</h3>
        <ul><li>Totalmente equipada</li><li>Forno, placa e micro-ondas</li><li>Máquina de lavar loiça</li><li>Máquina de café e torradeira</li></ul>
      </div>
      <div class="comodidades__col">
        <h3><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3 18v-6.5A2.5 2.5 0 0 1 5.5 9h13a2.5 2.5 0 0 1 2.5 2.5V18M3 15h18M3 18v2M21 18v2M6 9V6.5A1.5 1.5 0 0 1 7.5 5h9A1.5 1.5 0 0 1 18 6.5V9"/></svg>Conforto</h3>
        <ul><li>Ar condicionado em todas as divisões</li><li>Casa de banho privativa em cada quarto</li><li>Roupa de cama de algodão</li><li>Secador de cabelo</li></ul>
      </div>
      <div class="comodidades__col">
        <h3><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3 11l9-7 9 7M5 9.5V20h14V9.5M10 20v-5h4v5"/></svg>A casa</h3>
        <ul><li>Wi-Fi</li><li>Televisão e livros</li><li>Entrada privada</li><li>Estacionamento privado gratuito</li></ul>
      </div>
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
