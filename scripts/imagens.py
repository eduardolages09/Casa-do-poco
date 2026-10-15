"""Copia as fotos do dossiê para o site sem perder qualidade.

- O tamanho maior é o próprio ficheiro do dossiê, copiado byte a byte (sem
  voltar a comprimir).
- Os tamanhos menores saem do original com Lanczos, JPEG qualidade 90 e cor
  sem subamostragem (4:4:4), para o granito e as arestas não borrarem.
- As fotos da região vêm do Wikimedia Commons (descarregadas de novo, a 2400 px).

Correr a partir da pasta da casa:  py -I scripts/imagens.py
"""
import os
import shutil
import subprocess
import urllib.parse
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
CASA = os.path.dirname(AQUI)
FOTOS = os.path.join(CASA, 'dossie', 'marketing', 'fotos')
SAIDA = os.path.join(CASA, 'site', 'assets', 'img')
CACHE = os.path.join(AQUI, '_regiao')

# nome no site: (origem no dossiê, larguras menores)
CASA_FOTOS = {
    'hero':          ('exterior/piscina-02.jpg', (800, 1400, 2000)),
    'ext-fachada':   ('exterior/fachada-01.jpg', (1000, 1600, 2000)),
    'ext-patio':     ('exterior/patio-01.jpg', (1000, 1600, 2000)),
    'ext-serra':     ('exterior/piscina-04.jpg', (800, 1000, 1400, 1600, 2000)),
    'ext-jardim':    ('exterior/jardim-01.jpg', (800, 1000, 1400, 1600, 2000)),
    'ext-churrasco': ('exterior/churrasqueira-01.jpg', (1000, 1600, 2000)),
    'aerea':         ('exterior/aerea-01.jpg', (800, 1400, 2000)),
    'aerea-2':       ('exterior/aerea-02.jpg', (800, 1400, 2000)),
    'pool-vidro':    ('exterior/piscina-03.jpg', (800, 1400, 2000)),
    'pool-vista':    ('exterior/vista-01.jpg', (800, 1400, 2000)),
    'fecho':         ('exterior/piscina-01.jpg', (800, 1400, 2000)),
    'sala':          ('interior/sala-01.jpg', (800, 1400, 2000)),
    'mesa':          ('interior/refeicoes-01.jpg', (800, 1400, 2000)),
    'cozinha':       ('interior/cozinha-01.jpg', (800, 1400, 2000)),
    'quarto-1':      ('interior/quarto-01.jpg', (800, 1200, 1600)),
    'quarto-2':      ('interior/quarto-02.jpg', (800, 1200, 1600)),
    'quarto-3':      ('interior/quarto-03.jpg', (800, 1200, 1600)),
    'quarto-4':      ('interior/quarto-04.jpg', (800, 1200, 1600)),
    'wc-1':          ('interior/casa-de-banho-01.jpg', (600,)),
    'wc-2':          ('interior/casa-de-banho-02.jpg', (600, 1000)),
    'wc-3':          ('interior/casa-de-banho-03.jpg', (800, 1400)),
    'wc-4':          ('interior/casa-de-banho-04.jpg', (600, 1000)),
}

# Wikimedia Commons: (ficheiro, recorte em baixo para tirar a assinatura)
REGIAO = {
    'regiao-freita': ('Serra da Freita e Arada. GeoParque Arouca 143.jpg', 0),
    'regiao-frecha': ('Frecha da Mizarela - Serra da Freira - Portugal (51621506684).jpg', 0.045),
    'regiao-drave':  ('Drave 5.jpg', 0),
    'regiao-paiva':  ('Passadiços do Paiva Paiva walkways (39681956172).jpg', 0),
}


def menores(im, nome, larguras):
    im = im.convert('RGB')
    w, h = im.size
    for lw in larguras:
        if lw >= w:
            continue
        im.resize((lw, round(h * lw / w)), Image.LANCZOS).save(
            os.path.join(SAIDA, f'{nome}-{lw}.jpg'), quality=90, subsampling=0, optimize=True, progressive=True)


def da_casa():
    for nome, (orig, larguras) in CASA_FOTOS.items():
        src = os.path.join(FOTOS, orig)
        shutil.copyfile(src, os.path.join(SAIDA, nome + '.jpg'))   # o original, intacto
        im = Image.open(src)
        menores(im, nome, larguras)
        print(nome, im.size)


def da_regiao():
    os.makedirs(CACHE, exist_ok=True)
    for nome, (ficheiro, corte) in REGIAO.items():
        dest = os.path.join(CACHE, nome + '.jpg')
        if not os.path.exists(dest):
            url = 'https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote(ficheiro) + '?width=2400'
            subprocess.run(['curl', '-sL', '-A', 'CasaDoPoco-site/1.0', '-o', dest, url], check=True)
        im = Image.open(dest).convert('RGB')
        if corte:
            w, h = im.size
            im = im.crop((0, 0, w, round(h * (1 - corte))))
        w = min(im.size[0], 2400)
        if w < im.size[0]:
            im = im.resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS)
        im.save(os.path.join(SAIDA, nome + '.jpg'), quality=90, subsampling=0, optimize=True, progressive=True)
        menores(im, nome, (800, 1400))
        print(nome, im.size)


if __name__ == '__main__':
    if os.path.isdir(SAIDA):
        shutil.rmtree(SAIDA)
    os.makedirs(SAIDA)
    da_casa()
    da_regiao()
