import os
import base64
import tempfile
import json
import logging
from openai import AzureOpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

env_path = Path(__file__).resolve(strict=True).parent / ".env"
load_dotenv(dotenv_path=env_path)

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME]):
    logger.error("Variáveis de ambiente do Azure OpenAI não configuradas corretamente")
else:
    logger.info("Variáveis de ambiente carregadas com sucesso")

app = FastAPI(
    title="STRIDE Threat Modeling API",
    description="API para análise de ameaças em diagramas de arquitetura usando Azure OpenAI e metodologia STRIDE",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("FastAPI inicializado com CORS habilitado")

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint= AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME)

logger.info(f"Cliente Azure OpenAI configurado - Endpoint: {AZURE_OPENAI_ENDPOINT}")
logger.info(f"Deployment: {AZURE_OPENAI_DEPLOYMENT_NAME}")

class HealthResponse(BaseModel):
    status: str
    message: str

class ThreatAnalysisResponse(BaseModel):
    threat_model: list
    improvement_suggestions: list
    summary: Optional[dict] = None

def criar_prompt_modelo_ameacas(tipo_aplicacao, autenticacao, acesso_internet, dados_sensiveis, descricao_aplicacao):
    prompt = f"""Aja como um especialista em cibersegurança com mais de 20 anos de experiência 
    utilizando a metodologia de modelagem de ameaças STRIDE para produzir modelos de ameaças 
    abrangentes para uma ampla gama de aplicações. Sua tarefa é analisar o resumo do código, 
    o conteúdo do README e a descrição da aplicação fornecidos para produzir uma lista de 
    ameaças específicas para essa aplicação.

    Presta atenção na descrição da aplicação e nos detalhes técnicos fornecidos.

    Para cada uma das categorias do STRIDE (Falsificação de Identidade - Spoofing, 
    Violação de Integridade - Tampering, 
    Repúdio - Repudiation, 
    Divulgação de Informações - Information Disclosure, 
    Negação de Serviço - Denial of Service, e 
    Elevação de Privilégio - Elevation of Privilege), liste múltiplas (3 ou 4) ameaças reais, 
    se aplicável. Cada cenário de ameaça deve apresentar uma situação plausível em que a ameaça 
    poderia ocorrer no contexto da aplicação.

    A lista de ameaças deve ser apresentada em formato de tabela, 
    com as seguintes colunas:Ao fornecer o modelo de ameaças, utilize uma resposta formatada em JSON 
    com as chaves "threat_model" e "improvement_suggestions". Em "threat_model", inclua um array de 
    objetos com as chaves "Threat Type" (Tipo de Ameaça), "Scenario" (Cenário), e 
    "Potential Impact" (Impacto Potencial).    

    Ao fornecer o modelo de ameaças, utilize uma resposta formatada em JSON com as chaves 
    "threat_model" e "improvement_suggestions". 
    Em "threat_model", inclua um array de objetos com as chaves "Threat Type" (Tipo de Ameaça), 
    "Scenario" (Cenário), e "Potential Impact" (Impacto Potencial).

    Em "improvement_suggestions", inclua um array de strings que sugerem quais informações adicionais 
    poderiam ser fornecidas para tornar o modelo de ameaças mais completo e preciso na próxima iteração. 
    Foque em identificar lacunas na descrição da aplicação que, se preenchidas, permitiriam uma 
    análise mais detalhada e precisa, como por exemplo:
    - Detalhes arquiteturais ausentes que ajudariam a identificar ameaças mais específicas
    - Fluxos de autenticação pouco claros que precisam de mais detalhes
    - Descrição incompleta dos fluxos de dados
    - Informações técnicas da stack não informadas
    - Fronteiras ou zonas de confiança do sistema não especificadas
    - Descrição incompleta do tratamento de dados sensíveis
    - Detalhes sobre
    Não forneça recomendações de segurança genéricas — foque apenas no que ajudaria a criar um
    modelo de ameaças mais eficiente.

    TIPO DE APLICAÇÃO: {tipo_aplicacao}
    MÉTODOS DE AUTENTICAÇÃO: {autenticacao}
    EXPOSTA NA INTERNET: {acesso_internet}
    DADOS SENSÍVEIS: {dados_sensiveis}
    RESUMO DE CÓDIGO, CONTEÚDO DO README E DESCRIÇÃO DA APLICAÇÃO: {descricao_aplicacao}

    Exemplo de formato esperado em JSON:

    {{
      "threat_model": [
        {{
          "Threat Type": "Spoofing",
          "Scenario": "Cenário de exemplo 1",
          "Potential Impact": "Impacto potencial de exemplo 1"
        }},
        {{
          "Threat Type": "Spoofing",
          "Scenario": "Cenário de exemplo 2",
          "Potential Impact": "Impacto potencial de exemplo 2"
        }}
        // ... mais ameaças
      ],
      "improvement_suggestions": [
        "Por favor, forneça mais detalhes sobre o fluxo de autenticação entre os componentes para permitir uma análise melhor de possíveis falhas de autenticação.",
        "Considere adicionar informações sobre como os dados sensíveis são armazenados e transmitidos para permitir uma análise mais precisa de exposição de dados.",
        // ... mais sugestões para melhorar o modelo de ameaças
      ]
    }}"""

    return prompt

@app.get("/", response_model=HealthResponse)
async def root():
    logger.info("Endpoint raiz acessado")
    return {
        "status": "online",
        "message": "API de Análise de Ameaças STRIDE está funcionando! Visite /docs para ver a documentação completa."
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    logger.info("Health check solicitado")
    try:
        if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME]):
            logger.warning("Health check falhou - Variáveis de ambiente não configuradas")
            return {
                "status": "unhealthy",
                "message": "Variáveis de ambiente não configuradas corretamente"
            }
        logger.info("Health check passou - API está saudável")
        return {
            "status": "healthy",
            "message": "API configurada e pronta para uso"
        }
    except Exception as e:
        logger.error(f"Health check falhou com exceção: {str(e)}")
        return {
            "status": "unhealthy",
            "message": f"Erro: {str(e)}"
        }

@app.post("/analisar_ameacas")
async def analisar_ameacas(
    imagem: UploadFile = File(..., description="Imagem do diagrama de arquitetura"),
    tipo_aplicacao: str = Form(..., description="Tipo da aplicação (ex: Web App, API, Mobile)"),
    autenticacao: str = Form(..., description="Métodos de autenticação utilizados"),
    acesso_internet: str = Form(..., description="Se a aplicação está exposta na internet (Sim/Não)"),
    dados_sensiveis: str = Form(..., description="Tipos de dados sensíveis manipulados"),
    descricao_aplicacao: str = Form(..., description="Descrição detalhada da aplicação")
):
    """Análise de ameaças STRIDE em diagramas de arquitetura"""
    try:
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
        if imagem.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de arquivo não suportado. Use: {', '.join(allowed_types)}"
            )
        
        logger.info(f"Analisando imagem: {imagem.filename}")
        logger.info(f"Tipo de aplicação: {tipo_aplicacao}")
        
        prompt = criar_prompt_modelo_ameacas(
            tipo_aplicacao, autenticacao, acesso_internet, dados_sensiveis, descricao_aplicacao
        )
        
        content = await imagem.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(imagem.filename).suffix) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        with open(temp_file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('ascii')

        # Adicionar a imagem codificada ao prompt
        chat_prompt = [
            {
                "role": "system", 
                "content": "Você é uma IA especialista em cibersegurança, que analisa desenhos de arquitetura e aplica a metodologia STRIDE para identificar ameaças."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{encoded_string}"}
                    },
                    {
                        "type": "text", 
                        "text": "Por favor, analise a imagem do diagrama de arquitetura e o texto acima e forneça um modelo de ameaças detalhado em formato JSON conforme especificado."
                    }
                ]
            }
        ]
        
        # Chamar o modelo OpenAI
        logger.info("Enviando requisição para Azure OpenAI...")
        response = client.chat.completions.create(
            messages=chat_prompt,
            temperature=0.7,
            max_tokens=2000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False,
            model=AZURE_OPENAI_DEPLOYMENT_NAME
        )
        
        logger.info("Resposta recebida do Azure OpenAI")
        
        os.remove(temp_file_path)
        logger.debug(f"Arquivo temporário removido: {temp_file_path}")
        
        response_content = response.choices[0].message.content
        
        try:
            if "```json" in response_content:
                response_content = response_content.split("```json")[1].split("```")[0].strip()
            elif "```" in response_content:
                response_content = response_content.split("```")[1].split("```")[0].strip()
            
            threat_data = json.loads(response_content)
            
            threat_count = len(threat_data.get("threat_model", []))
            threat_types = {}
            for threat in threat_data.get("threat_model", []):
                threat_type = threat.get("Threat Type", "Unknown")
                threat_types[threat_type] = threat_types.get(threat_type, 0) + 1
            
            threat_data["summary"] = {
                "total_threats": threat_count,
                "threats_by_type": threat_types,
                "application_type": tipo_aplicacao,
                "has_internet_access": acesso_internet,
                "authentication_method": autenticacao
            }
            
            logger.info(f"Análise concluída com sucesso. Total de ameaças identificadas: {threat_count}")
            return JSONResponse(content=threat_data, status_code=200)
            
        except json.JSONDecodeError as je:
            logger.warning(f"Erro ao fazer parse do JSON da resposta: {str(je)}")
            return JSONResponse(
                content={
                    "raw_response": response_content,
                    "warning": "Não foi possível fazer parse automático do JSON. Resposta bruta incluída."
                },
                status_code=200
            )

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Erro durante análise: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao processar análise: {str(e)}")