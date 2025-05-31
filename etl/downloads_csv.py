import requests
from bs4 import BeautifulSoup
import os
import time

# Configurações globais
BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/"
OUTPUT_DIR = "downloads"  # Diretório para salvar os arquivos CSV
MAX_TENTATIVAS = 10

# URLs das categorias
CATEGORIES = {
    "producao": {
        "producao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02",
    },
    "processamento": {
        "pro_viniferas": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_03",
        "pro_americanas_hibridas": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_03",
        "pro_uvas_de_mesa": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_03",
        "pro_sem_classificacao": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_03",
    },
    "comercializacao": {
        "comercializacao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04",
    },
    "importacao": {
        "imp_vinho_de_mesa": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_05",
        "imp_espumantes": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_05",
        "imp_uvas_frescas": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_05",
        "imp_uvas_passas": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_05",
        "imp_suco_de_uva": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_05&opcao=opt_05",
    },
    "exportacao": {
        "exp_vinhos_de_mesa": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_06",
        "exp_espumantes": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_06",
        "exp_uvas_frescas": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_05",
        "exp_uvas_passas": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_06",
        "exp_suco_de_uva": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_06",
    },
}

def criar_diretorio_saida():
    """Cria o diretório de saída, se não existir."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def fazer_requisicao(url):
    """Faz uma requisição HTTP com tentativas."""
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        try:
            resposta = requests.get(url)
            if resposta.status_code == 200:
                return resposta
            print(f"Status {resposta.status_code} para {url}. Tentando novamente em 3 segundos...")
        except requests.RequestException as e:
            print(f"Erro de conexão para {url}: {e}. Tentando novamente em 3 segundos...")
        time.sleep(3)
        tentativas += 1
    print(f"Não foi possível acessar o site após {MAX_TENTATIVAS} tentativas.")
    return None

def encontrar_url_csv(html):
    """Encontra a URL do arquivo CSV na página HTML."""
    soup = BeautifulSoup(html, "html.parser")
    botao_download = soup.find("span", class_="spn_small", text="DOWNLOAD")
    if botao_download and botao_download.parent and botao_download.parent.get("href"):
        return BASE_URL + botao_download.parent["href"]
    return None

def salvar_csv(category_group, category_name, csv_content):
    """Salva o conteúdo do CSV no diretório apropriado."""
    group_dir = os.path.join(OUTPUT_DIR, category_group)
    os.makedirs(group_dir, exist_ok=True)
    caminho_arquivo = os.path.join(group_dir, f"{category_name}.csv")
    with open(caminho_arquivo, "wb") as file:
        file.write(csv_content)
    print(f"Arquivo salvo em: {caminho_arquivo}")

def processar_categoria(category_group, category_name, url):
    """Processa uma categoria específica para baixar o CSV."""
    resposta = fazer_requisicao(url)
    if not resposta:
        return
    csv_url = encontrar_url_csv(resposta.text)
    if csv_url:
        print(f"Baixando CSV para {category_name}: {csv_url}")
        resposta_csv = fazer_requisicao(csv_url)
        if resposta_csv:
            salvar_csv(category_group, category_name, resposta_csv.content)
    else:
        print(f"Botão de download não encontrado para {category_name}.")

def csv_final():
    """Função principal para processar todas as categorias."""
    criar_diretorio_saida()
    for category_group, group_data in CATEGORIES.items():
        for category_name, url in group_data.items():
            processar_categoria(category_group, category_name, url)

if __name__ == "__main__":
    csv_final()