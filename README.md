# Trabalho Final - INF420: Inteligência Artificial

## Projeto: Bot de Xadrez com Minimax

### Descrição do Projeto
Este projeto é o trabalho final da disciplina INF420 - Inteligência Artificial. O objetivo do projeto foi desenvolver um bot de xadrez utilizando o algoritmo **Minimax** para jogar contra o usuário. A interface gráfica do jogo foi implementada com **Pyglet**, e a lógica de xadrez utiliza a biblioteca **python-chess**.

### Funcionalidades
- Implementação do algoritmo Minimax para decisões do bot.
- Capacidade de jogar contra um bot que simula movimentos de xadrez.
- Interface gráfica simples usando Pyglet.
- Suporte a movimentos legais e regras de xadrez através da biblioteca python-chess.

### Tecnologias Utilizadas
- **Python**: Linguagem de programação principal do projeto.
- **Pyglet**: Biblioteca utilizada para a implementação da interface gráfica.
- **python-chess**: Biblioteca que fornece as funcionalidades relacionadas às regras do jogo de xadrez.

### Algoritmo Minimax
O bot utiliza o algoritmo Minimax com uma profundidade configurável para calcular os melhores movimentos. A versão do Minimax inclui:
- **Podas alfa-beta** para otimizar a performance e reduzir o número de movimentos avaliados.
- Heurísticas usadas para determinar a melhor jogada em cenários intermediários.

### Como Executar o Projeto
1. **Pré-requisitos**: Certifique-se de que possui Python instalado, assim como as bibliotecas necessárias:
   ```
   pip install pyglet python-chess
   ```

2. **Executar o jogo**:
   Para iniciar o jogo, basta executar o arquivo principal:
   ```
   python main.py
   ```

### Estrutura do Projeto
- `main.py`: Arquivo principal que inicializa o jogo e o loop de interação com o player.
- `minimax.py`: Contém a implementação do algoritmo Minimax e poda alfa-beta.
- `game.py`: Controla a lógica do jogo e a integração entre o player e o bot.
- `images/`: Diretório com imagens e recursos utilizados pela interface gráfica.

### Futuras Melhorias
- Implementação de um sistema de dicas para o jogador.
- Ajuste da dificuldade do bot baseado em níveis de profundidade do algoritmo Minimax.
- Ajuste de heurísticas usadas para tomada de decisão do bot.
