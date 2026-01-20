<!--START_SECTION:header-->
<div align="center">
  <p align="center">
    <img 
      alt="DIO Education" 
      src="./.github/assets/logo.webp" 
      width="100px" 
    />
    <h1>Análise de Ameaças STRIDE com Azure OpenAI</h1>
    <p>API REST + GPT-4 Vision para análise automática de segurança em arquiteturas de software</p>
  </p>
</div>
<!--END_SECTION:header-->

<p align="center">
  <img src="https://img.shields.io/static/v1?label=DIO&message=Education&color=E94D5F&labelColor=202024" alt="DIO Project" />
  <a href="LICENSE"><img  src="https://img.shields.io/static/v1?label=License&message=MIT&color=E94D5F&labelColor=202024" alt="License"></a>
  <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python" alt="Python Version" />
  <img src="https://img.shields.io/badge/FastAPI-0.104+-green?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Azure-OpenAI-orange?logo=microsoft-azure" alt="Azure OpenAI" />
</p>

---

## Índice

- [Início Rápido](#início-rápido)
- [Sobre o Projeto](#sobre-o-projeto)
- [Configuração do Azure OpenAI](#configuração-do-azure-openai)
- [Como Usar a API](#como-usar-a-api)
  - [Via Swagger UI](#1-via-swagger-ui-recomendado)
  - [Via Frontend Web](#2-via-frontend-web)
  - [Via cURL](#3-via-curl)
  - [Via Python](#4-via-python)
- [Endpoints da API](#endpoints-da-api)
- [Testes](#testes)
- [Troubleshooting](#troubleshooting)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Autor](#autor)

---

## Início Rápido

### Pré-requisitos
- Python 3.8+
- Credenciais do Azure OpenAI (veja [Configuração Azure](#configuração-do-azure-openai))

### Setup Rápido

```powershell
# 1. Clone e acesse o diretório
git clone https://github.com/tezougo/STRIDE-Threat-Analysis-with-Azure-OpenAI
cd Stride-demo-main-Agents-de-IA/module-1/01-introducao-backend

# 2. Crie ambiente virtual e instale dependências
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Configure credenciais
cp .env.example .env
notepad .env  # Cole suas credenciais do Azure

# 4. Inicie o servidor
uvicorn main:app --reload

# 5. Acesse a documentação
# http://localhost:8000/docs
```

**Pronto!** A API está rodando. Teste no endpoint `/health` ou use a interface Swagger em `/docs`.

---

## Sobre o Projeto

**Desafio da Formação Agents de IA - DIO Education**

API REST que analisa diagramas de arquitetura e identifica ameaças de segurança usando a metodologia **STRIDE** (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) com suporte de GPT-4 Vision/GPT-4o.

### Funcionalidades

- **Upload de imagens**: Suporta PNG, JPG, JPEG, GIF, WEBP
- **Análise automatizada**: 3-4 ameaças por categoria STRIDE
- **Relatórios JSON**: Estruturados com cenários e impactos
- **Sugestões de melhoria**: Feedback contextual para análises mais precisas
- **API documentada**: Swagger UI automático
- **Logging profissional**: Sistema de logs com níveis apropriados

### Metodologia STRIDE

| Categoria | Descrição | Exemplo |
|-----------|-----------|---------|
| **S**poofing | Falsificação de identidade | Roubo de tokens JWT |
| **T**ampering | Violação de integridade | SQL Injection |
| **R**epudiation | Negação de ações | Falta de logs de auditoria |
| **I**nformation Disclosure | Exposição de dados | Vazamento de informações |
| **D**enial of Service | Negação de serviço | DDoS, esgotamento de recursos |
| **E**levation of Privilege | Escalada de privilégios | Exploração de vulnerabilidades |

---

## Configuração do Azure OpenAI

### Passo 1: Criar Recurso

1. Acesse [Portal Azure](https://portal.azure.com)
2. Crie recurso **Azure OpenAI**
3. Configure:
   - **Região**: East US, West Europe ou Sweden Central (GPT-4 Vision disponível)
   - **Nome**: único globalmente (ex: `stride-openai-resource`)
   - **Tier**: Standard S0

  ### Rede e Firewall (Portal Azure)

  Ao criar o recurso pelo Portal (blade "Criar o OpenAI do Azure") você encontrará a aba "Rede" onde pode escolher como o serviço será acessado. Algumas orientações práticas:

  - Tipo de acesso:
    - "Todas as redes": permite acesso público (útil para testes locais). Não recomendado em produção.
    - "Redes selecionadas": bloqueia o acesso público e exige configurar uma Virtual Network / Subnet ou endpoints privados. Use em produção quando quiser isolar o serviço.
    - "Quando o recurso estiver desabilitado": recurso inacessível até que redes/endereços sejam configurados.

  - Virtual Network / Subnet: se optar por redes selecionadas, crie ou vincule uma VNet e subnet (por exemplo `vnet01` / `subnet-1`). Note que o serviço pode criar endpoints privados; isso exige configuração adicional para acessar a API a partir da sua rede on-premises ou máquina local (bastion/jumpbox ou VPN/ExpressRoute).

  - Firewall / Intervalo de endereços: você pode adicionar intervalos de IP públicos para permitir acesso (por exemplo, o IP público do seu laptop/CI). Em geral, para testes locais adicionar seu IP público é suficiente.

  - Observação sobre assinatura (Azure for Students): algumas assinaturas exigem registro do provedor de recursos (ex.: `Microsoft.CognitiveServices`) ou aprovação para criar instâncias. Se ocorrer erro ao criar o recurso, verifique se o seu subscription permite Azure OpenAI e registre os providers necessários.

  - Região e nome: selecione a região que suporta o modelo desejado (ex.: `Brazil South` para proximidade do Brasil) e escolha um nome único (ex.: `openai-STRIDE-instancia`).

  Imagens anexadas a este repositório mostram as opções de criação e a aba de Rede (Virtual network / Subnets). Para testes rápidos, use "Todas as redes" e depois endureça as regras quando tudo estiver funcionando.

  Se você bloquear o acesso via VNet/Private Endpoint, lembre-se de que as chaves e endpoint retornados no portal só funcionarão de dentro da rede configurada (ouvia conexão privada). Para desenvolvimentos locais, prefira habilitar acesso via firewall para o seu IP ou usar uma instância de jumpbox na mesma VNet.

  - Formato aceito (dica prática):
    - O portal aceita endereços em CIDR (ex.: `178.76.112.106/32`) e, em muitos casos, também aceita apenas o IP puro (`178.76.112.106`).
    - Se o portal rejeitar a entrada com `/32`, tente colar apenas o IP (sem espaços): `178.76.112.106`.
    - Evite incluir espaços em branco no começo/fim quando colar — frequentemente esse é o motivo da validação falhar.
    - Para um único host use `/32` ou o IP simples; para uma faixa use CIDR (ex.: `198.51.100.0/24`).



### Passo 2: Deploy do Modelo (Azure OpenAI Studio)

1. Acesse https://oai.azure.com/ e selecione seu recurso `openai-STRIDE-instancia`
2. No menu lateral, vá em **Recursos compartilhados** → **Implantações** (ou **Deployments**)
3. Clique em **+ Implantar o modelo** (ou **Create deployment**) e configure:
   - **Modelo**: `gpt-4o` (recomendado) ou `gpt-4-vision-preview`
   - **Nome do deployment**: `gpt-4o-stride` (anote este nome)
   - **Versão do modelo**: latest
   - **TPM**: 10K (ou conforme disponibilidade)

**Troubleshooting**: Se não encontrar a opção, verifique diretório/assinatura corretos (canto superior). Assinaturas de estudante podem requerer aprovação adicional.

### Passo 3: Obter Credenciais

1. No Portal Azure, acesse seu recurso
2. Menu **Keys and Endpoint**
3. Copie: **KEY 1**, **Endpoint**, **Deployment Name**

### Passo 4: Configurar .env

```env
AZURE_OPENAI_API_KEY=sua_chave_api_aqui
AZURE_OPENAI_ENDPOINT=https://seu-recurso.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-stride
```

**Importante**: Nunca faça commit do arquivo `.env`

### Passo 5: Testar Integração (Opcional)

Após criar o deployment, teste a conexão com este código simples:

```python
from openai import AzureOpenAI
import os

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

response = client.chat.completions.create(
    model="gpt-4o-stride",  # seu deployment name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, Azure OpenAI!"}
    ]
)
print(response.choices[0].message.content)
```

**Exemplos avançados**: Stream de resposta, conversas multi-turno e mais na [documentação oficial](https://learn.microsoft.com/azure/ai-services/openai/how-to/chatgpt).

### Custos (Aproximados)

- **GPT-4o**: ~$2.50/1M tokens input, ~$10/1M output
- **Crédito gratuito**: $200 nos primeiros 30 dias

**Dica**: Configure alertas de custo no Azure (Cost Management → Cost alerts)

---

## Como Usar a API

### 1. Via Swagger UI (Recomendado)

1. Acesse: http://localhost:8000/docs
2. Expanda **POST /analisar_ameacas**
3. Clique em **Try it out**
4. Faça upload da imagem do diagrama
5. Preencha os campos:
   ```
   tipo_aplicacao: "Aplicação Web"
   autenticacao: "OAuth 2.0 + JWT"
   acesso_internet: "Sim"
   dados_sensiveis: "Dados pessoais, emails"
   descricao_aplicacao: "Web app com autenticação OAuth, armazena dados em PostgreSQL"
   ```
6. Execute e aguarde ~10-30 segundos

### 2. Via Frontend Web

O projeto inclui uma interface web com visualização gráfica (Cytoscape.js) das ameaças:

1. Com a API rodando (porta 8000), abra o frontend:
   ```powershell
   # No diretório raiz do projeto
   cd module-1/02-front-end
   # Abra o index.html no navegador (duplo clique ou):
   start index.html
   ```

2. Na interface web:
   - Faça upload da imagem do diagrama
   - Preencha todos os campos do formulário
   - Clique em **Analisar**
   - Visualize o resultado em texto + grafo interativo de ameaças

**Recursos do Frontend**:
- Visualização gráfica das ameaças com Cytoscape.js
- Botão para imprimir o grafo de ameaças
- Interface Bootstrap responsiva
- Conexão automática com a API em http://localhost:8000

> **Nota**: Se você alterou a porta da API no uvicorn (ex: `--port 8001`), edite a linha 72 do `index.html` para refletir a nova porta.

### 3. Via cURL

```bash
curl -X POST "http://localhost:8000/analisar_ameacas" \
  -F "imagem=@diagrama.png" \
  -F "tipo_aplicacao=Web Application" \
  -F "autenticacao=OAuth 2.0 + JWT" \
  -F "acesso_internet=Sim" \
  -F "dados_sensiveis=Dados pessoais" \
  -F "descricao_aplicacao=Aplicação web com autenticação"
```

### 4. Via Python

```python
import requests

url = "http://localhost:8000/analisar_ameacas"
files = {"imagem": open("diagrama.png", "rb")}
data = {
    "tipo_aplicacao": "Web Application",
    "autenticacao": "OAuth 2.0 + JWT",
    "acesso_internet": "Sim",
    "dados_sensiveis": "Dados pessoais",
    "descricao_aplicacao": "App web com autenticação OAuth 2.0"
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

### Resposta Esperada

```json
{
  "threat_model": [
    {
      "Threat Type": "Spoofing",
      "Scenario": "Atacante pode interceptar tokens JWT se HTTPS não estiver configurado",
      "Potential Impact": "Acesso não autorizado a contas de usuário"
    }
    // ... mais 15-20 ameaças
  ],
  "improvement_suggestions": [
    "Forneça detalhes sobre rotação de tokens JWT",
    "Descreva estratégia de logging implementada"
  ],
  "summary": {
    "total_threats": 18,
    "threats_by_type": {
      "Spoofing": 3,
      "Tampering": 3,
      // ...
    }
  }
}
```

---

## Endpoints da API

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Status da API |
| `/health` | GET | Health check |
| `/analisar_ameacas` | POST | Análise STRIDE de imagem |
| `/docs` | GET | Documentação Swagger |

### Parâmetros do endpoint `/analisar_ameacas`

- `imagem` (file): Imagem do diagrama (PNG, JPG, JPEG, GIF, WEBP)
- `tipo_aplicacao` (string): Tipo da aplicação (ex: "Web Application")
- `autenticacao` (string): Métodos de autenticação (ex: "OAuth 2.0, JWT")
- `acesso_internet` (string): Indica se a aplicação está exposta à internet ("Sim" / "Não")
- `dados_sensiveis` (string): Tipos de dados sensíveis (ex: "Dados pessoais, emails")
- `descricao_aplicacao` (string): Descrição detalhada do fluxo e componentes da aplicação
---

## Testes

### Testar Health Check

```powershell
Invoke-RestMethod -Uri http://localhost:8000/health
```

### Executar Testes Automatizados

```powershell
python test_api.py
```

### Teste com imagem (PowerShell - multipart/form-data)

Se você usa PowerShell e precisa enviar um formulário multipart manualmente (útil em scripts ou quando o cliente não facilita upload de arquivos), este exemplo monta o corpo com boundary e envia os campos necessários:

```powershell
$boundary = [System.Guid]::NewGuid().ToString()
$LF = "`r`n"

$bodyLines = (
  "--$boundary",
  "Content-Disposition: form-data; name=`"tipo_aplicacao`"$LF",
  "Web Application",
  "--$boundary",
  "Content-Disposition: form-data; name=`"autenticacao`"$LF",
  "OAuth 2.0",
  "--$boundary",
  "Content-Disposition: form-data; name=`"acesso_internet`"$LF",
  "Sim",
  "--$boundary",
  "Content-Disposition: form-data; name=`"dados_sensiveis`"$LF",
  "Dados pessoais",
  "--$boundary",
  "Content-Disposition: form-data; name=`"descricao_aplicacao`"$LF",
  "Aplicação web",
  "--$boundary--$LF"
) -join $LF

Invoke-RestMethod -Uri http://localhost:8000/analisar_ameacas -Method Post -ContentType "multipart/form-data; boundary=$boundary" -Body $bodyLines
```

> Observação: este exemplo constrói apenas os campos de texto. Para incluir o arquivo da imagem via PowerShell é mais simples usar `Invoke-RestMethod` com `-Form` e um objeto que contenha o stream do arquivo, por exemplo: `-Form @{ imagem = Get-Item .\diagrama.png; tipo_aplicacao = 'Web Application'; ... }`.

---

## Troubleshooting

### "Connection error" ou "getaddrinfo failed"

**Causa**: O deployment do modelo não foi criado ou o endpoint está incorreto.

**Solução**:
```powershell
# 1. Verifique se o deployment existe no Azure
# Acesse https://ai.azure.com/ → selecione seu recurso → Implantações

# 2. Se não houver deployment, crie um:
# - Clique em "+ Implantar o modelo"
# - Modelo: gpt-4o
# - Nome: gpt-4o-stride
# - Versão: latest

# 3. Atualize o .env com o endpoint correto:
# AZURE_OPENAI_ENDPOINT=https://SEU-RECURSO.services.ai.azure.com/models
# AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-stride

# 4. Reinicie o servidor
# Ctrl+C no terminal do uvicorn, depois:
uvicorn main:app --reload
```

### "Não foi possível resolver a importação"
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "401 Unauthorized"
- Verifique a chave API no `.env`
- Confirme o endpoint com `https://` e `/` final

### "Model not found"
- Acesse Azure OpenAI Studio
- Copie o nome EXATO do deployment
- Atualize `AZURE_OPENAI_DEPLOYMENT_NAME`

### Servidor não inicia (porta ocupada)
```powershell
uvicorn main:app --reload --port 8001
```

### "Model does not support vision"

- Use `gpt-4o` ou `gpt-4-vision-preview`
- Recrie o deployment com modelo correto

---

## Tecnologias Utilizadas

- **Python 3.8+** - Linguagem de programação
- **FastAPI** - Framework web moderno e de alta performance
- **Azure OpenAI** - GPT-4 Vision / GPT-4o para análise de imagens
- **Uvicorn** - Servidor ASGI
- **Pydantic** - Validação de dados
- **Cytoscape.js** - Visualização de grafos de ameaças

---

## Estrutura do Projeto

```
stride-demo-main-agents-de-ia/
│
├── .github/                       # Assets do GitHub
├── .vscode/                       # Configurações do VS Code
│
├── module-1/
│   ├── 01-introducao-backend/
│   │   ├── main.py                # API FastAPI principal
│   │   ├── requirements.txt       # Dependências Python
│   │   ├── .env.example          # Template de variáveis de ambiente
│   │   └── .env                  # Suas credenciais (não commitado)
│   │
│   └── 02-front-end/
│       └── index.html            # Interface web com Cytoscape.js
│
├── examples/
│   ├── diagrams/                 # Diagramas de exemplo (vazio)
│   └── results/
│       └── web-app-example-result.json  # Exemplo de análise
│
├── test_api.py                   # Script de testes automatizados
├── .gitignore                    # Arquivos ignorados pelo Git
└── readme.md                     # Este arquivo
```

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---


<div align="center">
  <a href="https://www.linkedin.com/in/wagner-rodrigues-rosa/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>
</div>

### Sobre

Engenheiro de Controle e Automação com formação técnica em Mecatrônica, atuando como **Desenvolvedor Pleno** há mais de 4 anos. Experiência em desenvolvimento de aplicações web e mobile para os setores de **saúde, financeiro e entretenimento**, com forte domínio em **Python** (uso diário) e desenvolvimento de modelos de **IA e Machine Learning**.

### Stack Técnica

**Linguagens**: Python, Dart, TypeScript, Java, JavaScript, C++  
**Frontend**: Angular, Flutter, HTML, CSS, Bootstrap  
**Backend**: Spring Boot, FastAPI, Hibernate, Maven  
**Databases**: PostgreSQL, MySQL, MongoDB, SQL Server  
**Mobile**: Flutter/Dart (2 apps publicados na Play Store)  
**Versionamento**: Git, SVN, GitHub

### Experiência com Testes

Adoto uma abordagem de **tripla validação** para garantir estabilidade e qualidade:

1. **Testes Unitários**: Toda implementação de backend inclui testes unitários para blindar a lógica de negócios e prevenir regressões
2. **Testes de Integração**: Validação de persistência e consistência de dados em ambiente controlado
3. **Testes Funcionais**: Integração frontend/backend simulando comportamento do usuário final antes da entrega para QA

### Projetos Destacados

- **Apps Mobile**: Desenvolvimento e publicação de aplicações Android como desenvolvedor independente

---

<p align="center">
Wagner Rodrigues Rosa

Desenvolvido como parte do desafio da Formação Agents de IA da [DIO Education](https://www.dio.me/).
</p>

<p align="center">
  <a href="https://www.dio.me/" target="_blank">
    <img align="center" src="./.github/assets/footer.png" alt="banner"/>
  </a>
</p> 