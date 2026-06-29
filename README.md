# ⚽ Desafio do Dribble Infinito 🥅

1.📖 Sinopse:
Chegou a hora de calçar as chuteiras e entrar em campo! Prepare-se para ajudar nosso craque Neymar Jr. nessa corrida frenética rumo ao hexa! Aviso: Cuidado com os carrinhos dos zagueiros adversários e com o apito do juiz... eles farão de tudo para te expulsar de campo. Mostre que você tem ginga, desvie das faltas, colete os bônus e prove que nosso camisa 10 é merecedor da Bola de Ouro e da Taça da Copa!

2.🚹 Participantes:
    - Daniel Cavalcanti Monteiro
    - Fernando Corrêa Gambôa Pereira dos Santos
    - Leonardo Quintella Mendes Remigio
    - Saulo Fabianne de Melo Ferreira Filho
    - Theo Bessa da Costa
    - Tiago Almeida Rolim Cruz

3.🧱 Arquitetura do Projeto:
O jogo foi desenvolvido com a biblioteca Pygame e estruturado de forma modular (sem o uso de subpastas complexas) para melhor organização e facilidade de importação. A estrutura conta com uma pasta assets/ para imagens e áudios, e os seguintes arquivos na raiz:
    - main.py: Controla o loop principal do jogo, gerencia a tela, atualiza os grupos de sprites e calcula as colisões.
    - coletaveis.py: Define os itens de vantagem (Bola de Ouro, Isotônico/Gatorade e Caneleira), cada um aplicando um bônus único ao jogador.
    - obstaculos.py: Define a física e o comportamento de diferentes obstáculos (zagueiro, cones e cartões amarelos e vermelhos) com diferentes níveis de dano ao jogador em sua colisão.
    - jogador.py: Define a classe do jogador, programando sua movimentação, status de invencibilidade e sistema de vidas.
    - menu_inicial.py: Gera a tela de abertura do jogo, preparando o jogador para a partida.
    - game_over.py: Gera o plano de fundo da tela "Game Over" para ser mostrado assim que o jogador perde suas vidas.

4.📸 Capturas de Tela:

5.🛠 Ferramentas, bibliotecas e frameworks utilizados:
    - Python 3.12+.
    - Biblioteca Pygame: Biblioteca principal usada para renderização, eventos e lógica física do jogo. O Pygame facilitou o gerenciamento de Hitboxes (caixas de colisão) separadas dos Rects visuais, além de gerenciar grupos de sprites e o loop contínuo de quadros por segundo (FPS).
    - Random: Biblioteca usada para gerar aleatoriedade principalmente para os obstáculos e coletáveis do jogo.
    - GitHub: Usado para versionamento de código, criação de branches e Pull Requests para manter o código seguro durante o trabalho em equipe.

6.📝 Divisão de trabalho: 
    - Daniel Cavalcanti Monteiro: responsável pela lógica dos coletáveis em coletaveis.py.
    - Fernando Corrêa Gambôa Pereira dos Santos: responsável pela lógica envolvendo o jogador (vidas, efeitos, movimentação...) em jogador.py.
    - Leonardo Quintella Mendes Remigio: responsável pelas imagens e sons do jogo na pasta assets.
    - Saulo Fabianne de Melo Ferreira Filho: responsável pela lógica dos obstáculos em obstaculos.py e pelo README.
    - Theo Bessa da Costa: responsável pela interface em menu_inicial.py e game_over.py.
    - Tiago Almeida Rolim Cruz: responsável pela lógica de funcionamento do jogo em main.py.

7.📚 Conceitos de Programação utilizados: 
    - Programação Orientada a Objetos (POO): Uso massivo de Classes (class), herança (pygame.sprite.Sprite) e métodos específicos (update, __init__) para dar vida e independência a cada elemento do jogo.
    - Estruturas de Controle de Fluxo e Dados: Uso de arrays em conjunto com a biblioteca random para armazenar os tipos de obstáculos e coletáveis e também para sortear qual deles vai aparecer na tela, além do uso de operadores lógicos e condicionais aliados a laços de repetição para controlar o desenrolar do jogo.
    - Matemática Aplicada: Manipulação de eixos X e Y para compor as lógicas do jogador, coletáveis e obstáculos.
    - Modularização: Separação das lógicas em arquivos individuais para facilitar a criação do jogo.

8.📈 Aprendizados e Desafios:
    - Dificuldade com o uso do GitHub: foi um desafio usar essa poderosa ferramenta para programação no início do projeto, porém quanto mais produziamos e desenvolviamos o projeto nós nos familiarizamos com a ferramenta e conseguimos aprender como usar ela.
    - Construção do código em equipe: Para desenvolver o jogo em equipe nós desenvolvemos nossas habilidades de comunicação durante o projeto, a partir de feedbacks, do alinhando dos nossos objetivos e da divisão de tarefas entre nós mesmos.
    - Lógica de versionamento no GitHub: Evoluímos na prática de criar Pull Requests, revisar código (merge) e lidar com conflitos de arquivos enquanto toda a equipe desenvolvia o jogo simultaneamente.

9.🎮 Como jogar:
Requisitos:
    - Python 3.x instalado.
    - Pygame instalado (rode pip install pygame no terminal).
Instruções:
    - Clone ou baixe nosso código no repositório oficial: https://github.com/sfmff/Projeto-IP-grupo-01
    - Rode o arquivo main.py.
    - Use as setas do teclado para movimentar o jogador.
    - Desvie dos zagueiros e cartões, colete as Bolas de Ouro e os Isotônicos para chegar à maior pontuação possível!

BOM JOGO E RUMO AO HEXA! 🏆
