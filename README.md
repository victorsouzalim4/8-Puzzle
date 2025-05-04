
# 🧩 8-Puzzle

Este projeto implementa a resolução do clássico **8 Puzzle** usando algoritmos como BFS (Busca em Largura).

## ✅ Pré-requisitos

- Python 3.10+ instalado
- Git (opcional, caso vá clonar o repositório)
- Acesso ao terminal (PowerShell, CMD ou Bash)

## 🚀 Como rodar o projeto

### 1. Clone o repositório (opcional)

Se estiver usando Git:
```bash
git clone https://github.com/seu-usuario/Puzzle-8Pe-as.git
cd Puzzle-8Pe-as
```

Ou apenas **copie os arquivos para sua máquina**.

### 2. Crie um ambiente virtual

Abra o terminal na pasta do projeto e execute:

```bash
python -m venv venv
```

> Se estiver no Linux/Mac e `python` não funcionar, tente `python3`.

### 3. Ative o ambiente virtual

- **Windows (PowerShell):**
  ```bash
  .\venv\Scripts\Activate.ps1
  ```

- **Windows (CMD):**
  ```bash
  .\venv\Scripts\activate.bat
  ```

- **Linux/Mac:**
  ```bash
  source venv/bin/activate
  ```

### 4. Instale as dependências (se houver)

Caso o projeto use bibliotecas externas, instale com:

```bash
pip install -r requirements.txt
```

### 5. Execute o programa

Com o ambiente ativado, execute o arquivo principal:

```bash
python main.py
```

### 6. Comando para geração do executavel

```bash
pyinstaller --onefile --noconsole --name Puzzle interface.py
```

## 🛠️ Estrutura do Projeto

```
8-Puzzle/
├── algorithms/
│   ├── astar_search.py            # Algoritmo de busca A*
│   ├── breadth_first_search.py    # Algoritmo de Busca em Largura (BFS)
│   ├── greedy_search.py           # Algoritmo de busca Gulosa
│   └── __init__.py                # Inicialização do pacote algorithms
│
├── benchmark/
│   └── benchmark.py               # Script para execução e análise de benchmarks
│   └── data/                      # Provável pasta de entrada/saída de dados
│
├── build/Puzzle/
│   └── Puzzle.exe                 # Executável gerado pela aplicação (via PyInstaller)
│
├── dist/
│   └── Puzzle.exe                 # Versão empacotada do executável
│
├── interface/
│   ├── board_tab.py              # Lógica da interface do tabuleiro
│   ├── controls.py               # Controle dos botões e ações da interface
│   ├── styles.py                 # Estilos visuais da interface (cores, fontes, etc.)
│   ├── textures.py               # Texturas usadas na GUI
│   ├── ui_setup.py               # Configuração inicial da interface
│   └── __init__.py               # Inicialização do pacote interface
│
├── utils/
│   ├── priority_queue.py         # Implementação de fila de prioridade (provavelmente usada em A*)
│   └── state.py                  # Representação dos estados do jogo
│
├── venv/                         # Ambiente virtual do Python
│
├── build_exe.py                  # Script de build usando PyInstaller
├── icon.ico                      # Ícone do executável
├── interface.py                  # Provavelmente ponto de entrada com interface GUI
├── main.py                       # Entrada principal (pode iniciar interface ou lógica)
├── Puzzle.spec                   # Arquivo de configuração do PyInstaller
├── puzzle8.spec                  # Outra configuração possível de build
├── README.md                     # Documentação do projeto
├── Relatorio8Puzzle-InteligênciaArtificial.pdf  # Relatório detalhado do projeto
├── requirements.txt              # Dependências do projeto

```

## 📌 Observações

- Não execute `main.py` diretamente com `main.py`, use `python main.py`.
- Se mudar de máquina, sempre recrie o `venv`.

## Integrantes

- André Luiz Rocha Cabral
- Douglas Nícolas Silva Gomes 
- João Paulo Dias Estevão 
- Victor Souza Lima
