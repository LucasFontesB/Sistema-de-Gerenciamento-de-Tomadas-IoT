# 🏨 Sistema de Gerenciamento de Tomadas IoT

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3BABC3.svg?style=for-the-badge&logo=Flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57.svg?style=for-the-badge&logo=SQLite&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848.svg?style=for-the-badge&logo=Gunicorn&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-009639.svg?style=for-the-badge&logo=NGINX&logoColor=white)
![RaspberryPi](https://img.shields.io/badge/Raspberry%20Pi-A22846.svg?style=for-the-badge&logo=Raspberry-Pi&logoColor=white)

Sistema web desenvolvido em **Flask** para gerenciamento e monitoramento de tomadas inteligentes (Tuya) em ambiente de rede IoT.

Projetado para uso em hotelaria ou ambientes com múltiplos dispositivos, permitindo controle centralizado, seguro e escalável.

---

## 📦 Tecnologias Utilizadas

- Python 3  
- Flask  
- SQLite  
- TinyTuya  
- Gunicorn (produção)  
- Nginx (proxy reverso)  
- Raspberry Pi (servidor recomendado)  

## ⚙️ Funcionalidades

- ✅ Cadastro de dispositivos  
- ✅ Validação de IP e versão  
- ✅ Monitoramento contínuo via thread  
- ✅ Controle remoto (ligar/desligar)  
- ✅ Edição de dispositivos  
- ✅ Exclusão com confirmação  
- ✅ Persistência via SQLite  
- ✅ Configuração via `.env`  

## 🧠 Arquitetura

O sistema é projetado para rodar **dentro da rede IoT**, junto aos dispositivos, mantendo isolamento da rede administrativa.
```
Rede ADM
   ↓
(acesso HTTP permitido) Firewall / Roteador
   ↓
Rede IoT
├── Raspberry Pi (Servidor Flask)
├── Tomadas Inteligentes
└── Outros dispositivos IoT
```

A rede IoT permanece isolada, permitindo apenas acesso controlado ao servidor web.

# 🚀 Instalação (Ambiente de Desenvolvimento)

## 1️⃣ Clonar o projeto

```bash
git clone https://github.com/LucasFontesB/Sistema-de-Gerenciamento-de-Tomadas-IoT.git
cd seuprojeto
```

2️⃣ Criar ambiente virtual

```bash
python -m venv venv

Linux / Mac
source venv/bin/activate

Windows
venv\Scripts\activate
```

3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

4️⃣ Criar arquivo .env (Na raiz do projeto e não dentro da pasta app)

```bash
SECRET_KEY="sua_chave_super_secreta" (Recomendo uma senha forte gerada com letras maiusculas, minusculas, números e simbolos)
DB_PATH=dispositivos.db
STATUS_INTERVAL=5 (recomendado)
SOCKET_TIMEOUT=2 (recomendado)
```

5️⃣ Executar

```bash
python run.py
```

Acesse:
http://localhost:5000

# 🏭 Instalação em Produção (Raspberry Pi)

1️⃣ Instalar dependências do sistema

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx git -y
```

2️⃣ Rodar com Gunicorn

```bash
pip install gunicorn
gunicorn -w 2 -b 127.0.0.1:8000 run:app
```

3️⃣ Configurar Nginx como proxy reverso

```bash
Arquivo:
/etc/nginx/sites-available/iot

- Configuração:

server {
    listen 80;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

Ativar:

sudo ln -s /etc/nginx/sites-available/iot /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

# 🔐 Segurança Recomendada

- Manter servidor apenas na rede IoT

- Criar regra de firewall permitindo apenas acesso HTTP da rede ADM

- Não expor portas na internet

- Utilizar HTTPS interno se necessário

- Fazer backup periódico do banco SQLite

## 📁 Estrutura do Projeto
```
Projeto-Geral/
│
├── app/
│ ├── routes/
│ ├── services/
│ ├── templates/
│ ├── static/
│ └── config.py
│
├── run.py
├── requirements.txt
├── .env
└── .gitignore
```

# 🔧 Variáveis de Ambiente

| Variável        | Descrição                                  | Padrão |
|-----------------|--------------------------------------------|--------|
| SECRET_KEY      | Chave de segurança do Flask                | —      |
| DB_PATH         | Caminho do banco SQLite                    | dispositivos.db |
| STATUS_INTERVAL | Intervalo de monitoramento (segundos)      | 5      |
| SOCKET_TIMEOUT  | Tempo limite de conexão                    | 2      |

# 🧪 Futuras Melhorias

- Autenticação de usuários

- Histórico de ações

- Dashboard com gráficos

- Integração MQTT

- Dockerização

- Sistema de logs avançado

- Monitoramento remoto do Raspberry

# 🏁 Status do Projeto

Projeto em desenvolvimento ativo com foco em:
- 🛡️ Estabilidade
- 🔐 Segurança de rede
- 📈 Escalabilidade para múltiplos dispositivos
