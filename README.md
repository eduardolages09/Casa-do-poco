# Casa do Poço — site e dossiê

Casa do Poço, na aldeia da Felgueira (Arões, Vale de Cambra), Serra da Freita. AL 178025/AL, Moradia. Fica na mesma aldeia que a Casa da Gueira.

## Pastas

- `dossie/` — dossiê da casa (skill al-dossier). Entrada: `dossie/resumo.md`. O que o site pode dizer: `dossie/site-pronto.md`.
- `site/` — site estático, sem build. Abre com duplo clique no `index.html`.
  - `index.html`, `styles.css`, `main.js`, `creditos.html` (créditos das fotos da região).
  - `assets/img/` — o original de cada foto (copiado sem recompressão) e tamanhos menores (Lanczos, JPEG 90, 4:4:4).
- `scripts/imagens.py` — gera `site/assets/img/` a partir do dossiê e do Wikimedia Commons (`py -I scripts/imagens.py`). As fotos da região ficam em cache em `scripts/_regiao/`.
- `arquivo/v1-2026-10-13/` — a v1, só o HTML, o CSS e o JS (a v1 usava fotos comprimidas, que já não existem).

## Qualidade das fotos

As fotos do Airbnb vinham comprimidas: o dossiê tinha a versão por defeito, de ~130 KB, e a v1 ainda as recomprimia a 82. Foram trocadas pela versão de alta qualidade (`?im_w=2560&im_q=highq`, 0,6 a 1,8 MB cada). As verticais ficam na largura nativa de 1920. O site usa o original intacto e, nos tamanhos menores, JPEG 90 com a cor completa (4:4:4). Nenhuma foto é ampliada além do original e não há zoom ao passar o rato. A vista aérea da piscina começa a 1,16× e nessa altura usa o ficheiro de 2560 px.

## Versão base

### Ronda 6 (2026-10-15)

- **Cantos retos em todas as fotos:** saiu o raio das molduras do exterior e do interior (`.presa__moldura`), da foto dos quartos, da abertura da piscina (o `clip-path` deixou de ter `round`), da entrada das fotos ligada ao scroll e do visor. As animações ficam iguais. Os cartões das comodidades, que não têm foto, mantêm os cantos suaves.
- **Scroll fluido** (o Eduardo achou-o «meio travado» noutro PC). A causa principal: quando uma galeria presa (exterior, piscina, interior, região, quartos) encolhe depois da primeira descida, o salto de compensação era imediato e matava o embalo da roda; o scroll parava a seco em cada secção. Agora o salto guarda o resto do embalo e a página continua a deslizar. Além disso, as animações correm no mesmo frame do Lenis (antes ficavam um frame atrás), cada frame mede tudo antes de escrever (sem layouts forçados), as galerias que não mudam não são redesenhadas e as fotos descodificam-se antes de entrar no ecrã. Experimentou-se pôr as molduras em camadas próprias (`will-change`), mas as fotos perdiam nitidez, por isso o CSS ficou como estava. Conferido: fotos iguais ao pixel à versão anterior, sem erros, no PC, no telemóvel ao alto e deitado.

### Ronda 5 (2026-10-14)

A v4 está em `arquivo/v4-2026-10-14/`. O corpo da página passa a ser gerado por `scripts/monta_v5.py` (`py -I scripts/monta_v5.py`); o `monta_v4.py` fica só como histórico.

- **Hero:** o nome passou de Cinzel a Della Respira, uma romana clássica de caixa mista, com mais presença (7,6vw no PC).
- **Abertura → Exterior:** muito menos espaço por baixo da frase (o vazio caiu para cerca de metade).
- **Fotos:** todas as molduras (exterior, interior, quartos, região) entram a abrir-se e a subir e saem a recuar e a esvair-se, ligadas ao scroll (`main.js`, «ENTRADA E SAÍDA DAS FOTOS»). A piscina só tem a saída (a entrada já é a abertura da vista aérea). A foto do fecho entra com um zoom que assenta. A do hero não mexe.
- **Quartos:** refeitos a partir do 145 Townhouse, em versão simples: um painel preso com a coluna verde estreita («Quartos» no topo, o nome do quarto em duas linhas que sobem, os separadores 01–04 com a barra que se enche) e a foto 3:2 à direita, que se esvai e assenta a cada passo. Cada quarto mostra a sua foto e depois a da sua casa de banho, identificada («Casa de banho privativa»); as fotos ao alto ficam inteiras, ao centro. Sem ficha, botões nem notas. Depois da primeira descida solta-se e funciona com os separadores, as setas ou o dedo.
- **Comodidades:** a fita do Solar Antigo: o título ao centro com um filete e uma fila de 16 cartões (ícone de traço + nome) que anda sozinha para a esquerda, devagar e sem fim; pára com o rato por cima e arrasta-se.
- **Correção:** `overflow-anchor: none` no `html`. O browser já compensava sozinho o scroll quando uma secção presa encolhia, o `main.js` compensava outra vez, e a página saltava (com scroll rápido chegava a saltar os quartos inteiros). Já acontecia na v4.

### Ronda 4 (2026-10-13)

A v3 está em `arquivo/v3-2026-10-13/`. O corpo da página (do hero à região) é gerado por `scripts/monta_v4.py`, a partir de listas de fotos e legendas; para mudar uma legenda, editar lá e correr `py -I scripts/monta_v4.py`.

- **Hero:** o nome passou a Cinzel, uma romana de inscrição: as minúsculas saem em versaletes, como letra gravada no granito. Está maior (7,4vw no PC, 11,2vw no telemóvel, onde o hero 3:2 só tem ~260 px de altura).
- **Abertura:** cada palavra sai de um desfoque, em onda, ligada ao scroll (névoa). Substitui as palavras que subiam de uma máscara e ficavam cortadas a meio.
- **Exterior:** ficou só a casa, o pátio e a churrasqueira. Depois vem uma frase de quebra («Acima do jardim, a piscina olha a serra.») antes da animação da piscina.
- **A piscina:** a vista aérea abre-se até ao ecrã inteiro e segue, com o scroll, para as outras fotos da piscina, todas a ecrã inteiro e com uma frase cada: a serra, o relvado, através do vidro, as casas da aldeia e a vista aérea da casa. A piscina-02 é o hero e a piscina-01 é o fecho, por isso aparecem as 8 fotos da piscina. No telemóvel, a moldura abre-se até 6:5 à largura do ecrã e o texto fica por baixo.
- **Interior:** moldura 3:2 alta (a foto inteira) com o texto à direita, sem caixa. São as 3 fotos que existem das zonas comuns (sala, mesa, cozinha); o Airbnb não tem mais.
- **Quartos:** secção presa. Cada quarto mostra a sua foto (3:2) e, por cima, um cartão com a foto da sua casa de banho, no formato dela. Saiu a fila de miniaturas. O visor de cada quarto abre o quarto e a casa de banho dele. **A ligação de cada casa de banho a cada quarto segue a numeração da visita do Airbnb (Quarto 1 ↔ Casa de banho 1), que não diz a que quarto pertencem: confirmar com o dono.**
- **Comodidades:** quatro colunas (Exterior, Cozinha, Conforto, A casa), com 4 tópicos cada, só do que o Airbnb confirma.
- **Região:** secção presa; os lugares e as fotos avançam com o scroll. Depois da primeira descida, os nomes funcionam como separadores.
- **Sem caixas de vidro:** saíram da piscina, do interior e do fecho. O texto vai direto sobre a foto, com uma sombra difusa sem contorno.

### Ronda 3 (2026-10-13)

- **Hero:** o ficheiro original (2560×1707, igual byte a byte ao do dossiê), sem srcset reduzido, sem corte e sem nenhuma transformação. O hero tem a proporção da foto (3:2): a 1440 px de largura são 960 px de altura. Quando a foto é mais alta do que o ecrã, o nome sobe para ficar no primeiro ecrã. No telemóvel a foto também fica inteira em 3:2, à largura do ecrã.
- **Letra:** Bellefair, uma serifada fina e simples. O nome vai em caixa mista ("Casa do / Poço"); títulos, menu e etiquetas vão em maiúsculas espaçadas. As frases continuam em Petrona 300.
- **Marca:** saiu o símbolo do poço: fica só "Casa do Poço" na letra do site (o dono pode ter a sua marca).
- **Topo sobre o hero:** sem pílulas de vidro. Menu em texto fino com uma sombra difusa, uma sombra leve só na faixa do menu, e "Ver disponibilidade" só com contorno, que se enche ao passar o rato.
- **Localização:** saiu o cartão. Fica por baixo do nome, em maiúsculas pequenas ("Aldeia da Felgueira · Serra da Freita, Vale de Cambra"), sobre a terra e a pedra, a parte menos interessante da foto.

### Ronda 2 (2026-10-13)

O Eduardo pediu um site moderno e requintado que valorize a qualidade das fotos, sem ar de "spam" de fotos.

- **Hero:** a piscina elevada com a casa e a aldeia atrás (piscina-02). Nome em Tenor Sans, localização num cartão de vidro e menu em pílulas de vidro (tudo substituído na ronda 3).
- **Exterior:** galeria presa. À esquerda ficam o título, a legenda de cada foto e o contador; à direita, uma moldura 3:2 com a foto inteira, sem cortes. Cada foto sobe como uma cortina por cima da anterior. As fotos são a casa, o pátio, a piscina com a serra, o jardim e a churrasqueira.
- **A piscina:** a vista aérea que abre até ao ecrã inteiro (mantida a pedido).
- **Interior:** galeria presa como portas de correr: a sala, a mesa e a cozinha. Cada uma entra da direita e a imagem desliza a metade da velocidade. A legenda vai num cartão de vidro.
- **As duas galerias soltam-se depois da primeira descida:** a secção encolhe para um ecrã e passa a ter setas (regra da skill: não obrigar a re-percorrer).
- **Quartos:** uma foto por quarto (a única que existe), em grelha 2×2.
- **Casas de banho:** não ficam numa secção própria. O anúncio diz "4 quartos, todos com casa de banho privativa". O Airbnb mostra 4 casas de banho completas e 1 de serviço, e as fotos abrem para divisões de soalho, como os quartos. Não se sabe qual é de que quarto, por isso as 4 dos quartos aparecem numa linha discreta no fim de Quartos, sem emparelhar. A de serviço fica de fora.
- **Saíram:** a colagem do exterior, a quebra com a vista (a espreguiçadeira desfocada) e a fila de casas de banho a deslizar.
- **Ficaram:** comodidades, região (índice de 4 lugares), fecho com cartão de vidro e rodapé.

### Ronda 1 (2026-10-13)

O nome em Archivo expandido no céu da foto piscina-04, por trás da serra (máscara do céu). Cartões de vidro e pílulas vindos da referência ALVARA. Colagem do exterior e quartos em colunas desfasadas. Está em `arquivo/v1-2026-10-13/`.

## Ficou de fora de propósito

- avaliações e citações;
- preços, regras e horários;
- o mel e a receção em pessoa;
- piscina aquecida, de água salgada ou infinita (só o Booking o diz);
- animais;
- o telefone (não confirmado);
- redes sociais (não há).

## Confirmar com o dono antes de publicar

- Autorização para usar as fotos (são as do Airbnb e do Booking).
- Telefone e email para o site, e se quer o NIF no rodapé (vem do RNT).
- Qual casa de banho é de cada quarto (o site emparelha-as pela numeração do Airbnb).
- Lista completa em `dossie/resumo.md` › "Por confirmar".
