# TASK_IC



### Pré-requisitos
- Python 3.x
- Docker (para implantação em contêiner)

## Instalação

Clone este repositório:
```bash
git clone https://github.com/jonathannrocha/TASK_IC.git
```
Acesse o diretório do projeto:
```
cd TASK_IC
```

Acesse o diretório do projeto:
```
python -m venv venv
```

No Windows:
```
venv\Scripts\activate
```

No macOS/Linux:
```
source venv/bin/activate
```
Instale as dependências:
```
pip install -r requirements.txt
```

Para configurar o ambiente com Docker :
```
docker-compose up
```
## Executando a Aplicação
```
python main.py
```