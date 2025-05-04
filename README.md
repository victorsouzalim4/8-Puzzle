
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
Puzzle-8Pe-as/
│
├── BFS.py           # Implementação da busca em largura
├── State.py         # Classe que representa o estado do tabuleiro
├── main.py          # Ponto de entrada do programa
├── utils/           # Funções auxiliares
├── venv/            # Ambiente virtual (não versionado)
└── README.md        # Este arquivo
```

## 📌 Observações

- Não execute `main.py` diretamente com `main.py`, use `python main.py`.
- Se mudar de máquina, sempre recrie o `venv`.

## Integrantes

- André Luiz Rocha Cabral
- Douglas Nícolas Silva Gomes 
- João Paulo Dias Estevão 
- Victor Souza Lima
