# 🎬 Gerenciador de Catálogos Netflix - Projeto Cloud Completo

## 📝 Descrição

Projeto completo de portfólio cloud para gerenciamento de catálogos Netflix, utilizando:
- **Infraestrutura como Código (IaC):** Terraform para provisionamento Azure
- **Backend Serverless:** Azure Functions com Python
- **Frontend:** Streamlit para interface web interativa
- **Banco de Dados:** Azure Cosmos DB
- **Armazenamento:** Azure Blob Storage

## 📁 Estrutura do Projeto

```
gerenciador-netflix/
├── infra/                      # Infraestrutura Terraform
│   ├── main.tf               # Configuração principal Azure
│   ├── variables.tf          # Variáveis do Terraform
│   └── outputs.tf            # Outputs da infraestrutura
├── functions/                  # Azure Functions
│   ├── upload_file/          # Função de upload
│   │   ├── __init__.py
│   │   ├── function.json
│   │   └── requirements.txt
│   ├── salvar_catalogo/      # Função de salvamento
│   │   ├── __init__.py
│   │   ├── function.json
│   │   └── requirements.txt
│   ├── listar_catalogos/     # Função de listagem
│   │   ├── __init__.py
│   │   ├── function.json
│   │   └── requirements.txt
│   └── buscar_catalogo/      # Função de busca
│       ├── __init__.py
│       ├── function.json
│       └── requirements.txt
└── frontend/                   # Interface Streamlit
    └── app.py                 # Aplicação principal
```

## 🚀 Como Usar

### 1️⃣ Pré-requisitos

- Azure CLI instalado e configurado
- Terraform >= 1.0
- Python >= 3.9
- Conta Azure ativa

### 2️⃣ Provisionar Infraestrutura

```bash
cd infra/
terraform init
terraform plan
terraform apply
```

Este comando criará:
- Resource Group
- Storage Account
- App Service Plan
- Function App
- Cosmos DB (configure manualmente ou adicione ao Terraform)

### 3️⃣ Configurar Azure Functions

```bash
# Instalar Azure Functions Core Tools
npm install -g azure-functions-core-tools@4

# Deploy das funções
cd functions/
func azure functionapp publish <FUNCTION_APP_NAME>
```

### 4️⃣ Configurar Variáveis de Ambiente

No Azure Portal, configure as seguintes variáveis no Function App:

- `COSMOS_ENDPOINT`: Endpoint do Cosmos DB
- `COSMOS_KEY`: Chave de acesso do Cosmos DB
- `COSMOS_DATABASE`: Nome do banco (padrão: NetflixDB)
- `COSMOS_CONTAINER`: Nome do container (padrão: catalogs)
- `AzureWebJobsStorage`: String de conexão do Storage

### 5️⃣ Executar Frontend

```bash
cd frontend/
pip install streamlit requests
streamlit run app.py
```

Crie `.streamlit/secrets.toml` com:

```toml
FUNCTION_BASE_URL = "https://func-netflix-catalog.azurewebsites.net/api"
```

## 📚 Funcionalidades

### 📤 Upload de Arquivos
- Upload de catálogos em formato CSV, JSON ou TXT
- Armazenamento no Azure Blob Storage

### 💾 Salvar Catálogo
- Persistência de catálogos no Cosmos DB
- Validação de dados

### 📋 Listar Catálogos
- Listagem de todos os catálogos cadastrados
- Visualização em formato JSON

### 🔍 Buscar Catálogo
- Busca por ID específico
- Retorno detalhado do catálogo

## 🛠️ Tecnologias

- **Infraestrutura:** Terraform, Azure
- **Backend:** Python 3.9, Azure Functions
- **Frontend:** Streamlit
- **Banco de Dados:** Azure Cosmos DB
- **Armazenamento:** Azure Blob Storage
- **CI/CD:** GitHub Actions (opcional)

## 📝 Licença

Este projeto é um projeto de portfólio educacional.

## ✍️ Autor

Desenvolvido como projeto de demonstração de habilidades em Cloud Computing e Desenvolvimento Serverless.
