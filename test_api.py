"""
Script de Teste Automatizado para a API de Análise de Ameaças STRIDE

Este script testa todos os endpoints da API e valida as respostas.
"""

import requests
import sys
import json
from pathlib import Path

# Configurações
API_BASE_URL = "http://localhost:8000"
TIMEOUT = 60  # segundos

# Cores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_colored(text, color):
    """Imprime texto colorido"""
    print(f"{color}{text}{RESET}")

def test_health_check():
    """Testa o endpoint de health check"""
    print_colored("\nTestando Health Check...", BLUE)
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print_colored("[OK] Health Check: PASSOU", GREEN)
                return True
            else:
                print_colored(f"[FALHA] Health Check: FALHOU - Status: {data.get('status')}", RED)
                return False
        else:
            print_colored(f"[FALHA] Health Check: FALHOU - Status Code: {response.status_code}", RED)
            return False
    except Exception as e:
        print_colored(f"[ERRO] Health Check: ERRO - {str(e)}", RED)
        return False

def test_root_endpoint():
    """Testa o endpoint raiz"""
    print_colored("\nTestando Endpoint Raiz...", BLUE)
    
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if "status" in data and "message" in data:
                print_colored("[OK] Endpoint Raiz: PASSOU", GREEN)
                return True
            else:
                print_colored("[FALHA] Endpoint Raiz: FALHOU - Estrutura inválida", RED)
                return False
        else:
            print_colored(f"[FALHA] Endpoint Raiz: FALHOU - Status Code: {response.status_code}", RED)
            return False
    except Exception as e:
        print_colored(f"[ERRO] Endpoint Raiz: ERRO - {str(e)}", RED)
        return False

def test_swagger_docs():
    """Testa se a documentação Swagger está acessível"""
    print_colored("\nTestando Documentação Swagger...", BLUE)
    
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=5)
        
        if response.status_code == 200:
            print_colored("[OK] Swagger Docs: PASSOU", GREEN)
            print_colored(f"   Acesse em: {API_BASE_URL}/docs", YELLOW)
            return True
        else:
            print_colored(f"[FALHA] Swagger Docs: FALHOU - Status Code: {response.status_code}", RED)
            return False
    except Exception as e:
        print_colored(f"[ERRO] Swagger Docs: ERRO - {str(e)}", RED)
        return False

def test_openapi_schema():
    """Testa se o schema OpenAPI está disponível"""
    print_colored("\nTestando Schema OpenAPI...", BLUE)
    
    try:
        response = requests.get(f"{API_BASE_URL}/openapi.json", timeout=5)
        
        if response.status_code == 200:
            schema = response.json()
            if "openapi" in schema and "paths" in schema:
                print_colored("[OK] OpenAPI Schema: PASSOU", GREEN)
                print_colored(f"   Versão OpenAPI: {schema.get('openapi')}", YELLOW)
                print_colored(f"   Endpoints disponíveis: {len(schema.get('paths', {}))} ", YELLOW)
                return True
            else:
                print_colored("[FALHA] OpenAPI Schema: FALHOU - Estrutura inválida", RED)
                return False
        else:
            print_colored(f"[FALHA] OpenAPI Schema: FALHOU - Status Code: {response.status_code}", RED)
            return False
    except Exception as e:
        print_colored(f"[ERRO] OpenAPI Schema: ERRO - {str(e)}", RED)
        return False

def create_test_image():
    """Cria uma imagem de teste simples"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Criar uma imagem simples de diagrama
        img = Image.new('RGB', (800, 600), color='white')
        draw = ImageDraw.Draw(img)
        
        # Desenhar retângulos representando componentes
        # Frontend
        draw.rectangle([50, 50, 200, 150], outline='blue', width=3)
        draw.text((80, 90), "Frontend", fill='blue')
        
        # Backend
        draw.rectangle([300, 50, 450, 150], outline='green', width=3)
        draw.text((330, 90), "Backend API", fill='green')
        
        # Database
        draw.rectangle([550, 50, 700, 150], outline='red', width=3)
        draw.text((580, 90), "Database", fill='red')
        
        # Setas
        draw.line([200, 100, 300, 100], fill='black', width=2)
        draw.line([450, 100, 550, 100], fill='black', width=2)
        
        # Salvar
        test_image_path = Path("test_diagram.png")
        img.save(test_image_path)
        
        print_colored("[OK] Imagem de teste criada: test_diagram.png", GREEN)
        return test_image_path
        
    except ImportError:
        print_colored("[AVISO] Pillow não instalado. Pulando criação de imagem.", YELLOW)
        print_colored("   Instale com: pip install Pillow", YELLOW)
        return None

def test_threat_analysis_with_mock():
    """Testa o endpoint de análise de ameaças com dados mock"""
    print_colored("\nTestando Análise de Ameaças (Mock)...", BLUE)
    print_colored("[AVISO] Este teste requer uma imagem. Use uma imagem real para teste completo.", YELLOW)
    
    # Tentar criar imagem de teste
    image_path = create_test_image()
    
    if not image_path or not image_path.exists():
        print_colored("[AVISO] Pulando teste de análise - sem imagem disponível", YELLOW)
        print_colored("   Para testar manualmente:", YELLOW)
        print_colored(f"   1. Acesse: {API_BASE_URL}/docs", YELLOW)
        print_colored("   2. Use o endpoint POST /analisar_ameacas", YELLOW)
        return None
    
    try:
        files = {
            'imagem': open(image_path, 'rb')
        }
        data = {
            'tipo_aplicacao': 'Aplicação Web de Teste',
            'autenticacao': 'OAuth 2.0 + JWT',
            'acesso_internet': 'Sim',
            'dados_sensiveis': 'Dados de teste',
            'descricao_aplicacao': 'Aplicação de teste para validação da API'
        }
        
        print_colored("   Enviando requisição (pode levar 30-60 segundos)...", YELLOW)
        response = requests.post(
            f"{API_BASE_URL}/analisar_ameacas",
            files=files,
            data=data,
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Validar estrutura da resposta
            if "threat_model" in result:
                threat_count = len(result.get("threat_model", []))
                print_colored("[OK] Análise de Ameaças: PASSOU", GREEN)
                print_colored(f"   Ameaças identificadas: {threat_count}", YELLOW)
                
                if "summary" in result:
                    summary = result["summary"]
                    print_colored(f"   Total de ameaças: {summary.get('total_threats', 0)}", YELLOW)
                
                # Salvar resultado
                with open("test_result.json", "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print_colored("   Resultado salvo em: test_result.json", YELLOW)
                
                return True
            else:
                print_colored("[FALHA] Análise de Ameaças: FALHOU - Estrutura inválida", RED)
                print_colored(f"   Resposta: {json.dumps(result, indent=2)}", RED)
                return False
        else:
            print_colored(f"[FALHA] Análise de Ameaças: FALHOU - Status Code: {response.status_code}", RED)
            try:
                error = response.json()
                print_colored(f"   Erro: {error.get('detail', 'Sem detalhes')}", RED)
            except:
                print_colored(f"   Resposta: {response.text}", RED)
            return False
            
    except Exception as e:
        print_colored(f"[ERRO] Análise de Ameaças: ERRO - {str(e)}", RED)
        return False
    finally:
        # Limpar arquivo de teste
        if image_path and image_path.exists():
            image_path.unlink()

def check_server_running():
    """Verifica se o servidor está rodando"""
    print_colored("\nVerificando se o servidor está rodando...", BLUE)
    
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        print_colored(f"[OK] Servidor está rodando em {API_BASE_URL}", GREEN)
        return True
    except requests.exceptions.ConnectionError:
        print_colored(f"[ERRO] Servidor NÃO está rodando em {API_BASE_URL}", RED)
        print_colored("\n[INFO] Para iniciar o servidor:", YELLOW)
        print_colored("   cd module-1/01-introducao-backend", YELLOW)
        print_colored("   uvicorn main:app --reload", YELLOW)
        return False
    except Exception as e:
        print_colored(f"[ERRO] Erro ao conectar: {str(e)}", RED)
        return False

def main():
    """Função principal"""
    print_colored("=" * 60, BLUE)
    print_colored("  Teste Automatizado - API de Análise STRIDE", BLUE)
    print_colored("=" * 60, BLUE)
    
    # Verificar se servidor está rodando
    if not check_server_running():
        print_colored("\n[AVISO] Testes abortados - Servidor não está rodando", RED)
        sys.exit(1)
    
    # Executar testes
    results = []
    
    results.append(("Health Check", test_health_check()))
    results.append(("Endpoint Raiz", test_root_endpoint()))
    results.append(("Swagger Docs", test_swagger_docs()))
    results.append(("OpenAPI Schema", test_openapi_schema()))
    results.append(("Análise de Ameaças", test_threat_analysis_with_mock()))
    
    # Resumo
    print_colored("\n" + "=" * 60, BLUE)
    print_colored("  RESUMO DOS TESTES", BLUE)
    print_colored("=" * 60, BLUE)
    
    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)
    skipped = sum(1 for _, result in results if result is None)
    total = len(results)
    
    for name, result in results:
        if result is True:
            print_colored(f"[OK] {name}: PASSOU", GREEN)
        elif result is False:
            print_colored(f"[FALHA] {name}: FALHOU", RED)
        else:
            print_colored(f"[AVISO] {name}: PULADO", YELLOW)
    
    print_colored("\n" + "-" * 60, BLUE)
    print_colored(f"Total: {total} | Passou: {passed} | Falhou: {failed} | Pulado: {skipped}", BLUE)
    
    if failed == 0 and passed > 0:
        print_colored("\n[SUCESSO] TODOS OS TESTES PASSARAM!", GREEN)
        sys.exit(0)
    elif failed > 0:
        print_colored(f"\n[AVISO] {failed} TESTE(S) FALHARAM", RED)
        sys.exit(1)
    else:
        print_colored("\n[AVISO] NENHUM TESTE EXECUTADO COMPLETAMENTE", YELLOW)
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n[AVISO] Testes interrompidos pelo usuário", YELLOW)
        sys.exit(1)
