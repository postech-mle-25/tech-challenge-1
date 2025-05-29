import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path
import os
import csv

# --- Configurações ---
BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
MAX_TENTATIVAS = 3
ESPERA_SEGUNDOS = 3

# --- Mapeamento de categorias ---
URLS_CATEGORIAS = {
    "producao": {
        "producao": "index.php?opcao=opt_02",
    },
    "processamento": {
        "pro_viniferas": "index.php?subopcao=subopt_01&opcao=opt_03",
        "pro_americanas_hibridas": "index.php?subopcao=subopt_02&opcao=opt_03",
        "pro_uvas_de_mesa": "index.php?subopcao=subopt_03&opcao=opt_03",
        "pro_sem_classificacao": "index.php?subopcao=subopt_04&opcao=opt_03",
    },
    "comercializacao": {
        "comercializacao": "index.php?opcao=opt_04",
    },
    "importacao": {
        "imp_vinho_de_mesa": "index.php?subopcao=subopt_01&opcao=opt_05",
        "imp_espumantes": "index.php?subopcao=subopt_02&opcao=opt_05",
        "imp_uvas_frescas": "index.php?subopcao=subopt_03&opcao=opt_05",
        "imp_uvas_passas": "index.php?subopcao=subopt_04&opcao=opt_05",
        "imp_suco_de_uva": "index.php?subopcao=subopt_05&opcao=opt_05",
    },
    "exportacao": {
        "exp_vinhos_de_mesa": "index.php?subopcao=subopt_01&opcao=opt_06",
        "exp_espumantes": "index.php?subopcao=subopt_02&opcao=opt_06",
        "exp_uvas_frescas": "index.php?subopcao=subopt_03&opcao=opt_05",  # erro no site
        "exp_uvas_passas": "index.php?subopcao=subopt_03&opcao=opt_06",
        "exp_suco_de_uva": "index.php?subopcao=subopt_04&opcao=opt_06",
    },
}

# --- URLs dos CSVs na nuvem ---
CSV_CATEGORIAS = {
    "producao": {
        "producao": "https://fiaptech.blob.core.windows.net/downloads/producao/producao.csv",
    },
    "processamento": {
        "pro_viniferas": "https://fiaptech.blob.core.windows.net/downloads/processamento/pro_viniferas.csv",
        "pro_americanas_hibridas": "https://fiaptech.blob.core.windows.net/downloads/processamento/pro_americanas_hibridas.csv",
        "pro_uvas_de_mesa": "https://fiaptech.blob.core.windows.net/downloads/processamento/pro_uvas_de_mesa.csv",
        "pro_sem_classificacao": "https://fiaptech.blob.core.windows.net/downloads/processamento/pro_sem_classificacao.csv",
    },
    "comercializacao": {
        "comercializacao": "https://fiaptech.blob.core.windows.net/downloads/comercializacao/comercializacao.csv",
    },
    "importacao": {
        "imp_vinho_de_mesa": "https://fiaptech.blob.core.windows.net/downloads/importacao/imp_vinho_de_mesa.csv",
        "imp_espumantes": "https://fiaptech.blob.core.windows.net/downloads/importacao/imp_espumantes.csv",
        "imp_uvas_frescas": "https://fiaptech.blob.core.windows.net/downloads/importacao/imp_uvas_frescas.csv",
        "imp_uvas_passas": "https://fiaptech.blob.core.windows.net/downloads/importacao/imp_uvas_passas.csv",
        "imp_suco_de_uva": "https://fiaptech.blob.core.windows.net/downloads/importacao/imp_suco_de_uva.csv",
    },
    "exportacao": {
        "exp_vinhos_de_mesa": "https://fiaptech.blob.core.windows.net/downloads/exportacao/exp_vinhos_de_mesa.csv",
        "exp_espumantes": "https://fiaptech.blob.core.windows.net/downloads/exportacao/exp_espumantes.csv",
        "exp_uvas_frescas": "https://fiaptech.blob.core.windows.net/downloads/exportacao/exp_uvas_frescas.csv",
        "exp_uvas_passas": "https://fiaptech.blob.core.windows.net/downloads/exportacao/exp_uvas_passas.csv",
        "exp_suco_de_uva": "https://fiaptech.blob.core.windows.net/downloads/exportacao/exp_suco_de_uva.csv",
    },
}

# --- Funções utilitárias ---

def get_response(url, max_tentativas=MAX_TENTATIVAS, espera=ESPERA_SEGUNDOS, verbose=False):
    """
    Tenta fazer uma requisição HTTP GET até obter resposta 200 ou atingir o limite de tentativas.

    Parâmetros:
        url (str): URL a ser requisitada.
        max_tentativas (int): Número máximo de tentativas.
        espera (int): Tempo de espera entre tentativas (segundos).
        verbose (bool): Se True, imprime mensagens de erro e progresso.

    Retorna:
        requests.Response ou None: Resposta HTTP se sucesso, senão None.
    """
    for tentativa in range(max_tentativas):
        try:
            resposta = requests.get(url, headers=HEADERS)
            if resposta.status_code == 200:
                return resposta
            if verbose:
                print(f"[{tentativa+1}/{max_tentativas}] Falha {resposta.status_code} em {url}")
        except Exception as e:
            if verbose:
                print(f"[{tentativa+1}/{max_tentativas}] Erro: {e}")
        time.sleep(espera)
    return None

def extrair_link_csv(html):
    """
    Extrai o link do arquivo CSV a partir do HTML da página.

    Parâmetros:
        html (str): Conteúdo HTML da página.

    Retorna:
        str ou None: URL completa do CSV se encontrada, senão None.
    """
    soup = BeautifulSoup(html, "html.parser")
    link_tag = soup.find("span", class_="spn_small", text="DOWNLOAD")
    if link_tag and link_tag.parent.name == "a":
        return BASE_URL + link_tag.parent.get("href", "")
    return None

def obter_links_csv(mapa_categorias=URLS_CATEGORIAS, verbose=False):
    """
    Percorre todas as categorias e retorna os links CSV encontrados.
    Se não conseguir acessar nenhuma URL após 3 tentativas, faz fallback para as URLs dos arquivos na nuvem.

    Parâmetros:
        mapa_categorias (dict): Dicionário de categorias e caminhos relativos.
        verbose (bool): Se True, imprime mensagens de progresso e fallback.

    Retorna:
        dict: Mapeamento {categoria/nome: url_csv}
    """
    resultado = {}
    falha_global = False

    # Primeiro, tenta acessar todas as URLs
    for grupo, categorias in mapa_categorias.items():
        for nome, caminho in categorias.items():
            url_completa = BASE_URL + caminho
            resposta = get_response(url_completa, verbose=verbose)
            if not resposta:
                falha_global = True
                if verbose:
                    print(f"Falha ao acessar {url_completa}. Fallback global será ativado.")
                break
        if falha_global:
            break

    if falha_global:
        # Fallback global: retorna apenas as URLs dos arquivos na nuvem
        for grupo, categorias in CSV_CATEGORIAS.items():
            for nome, url in categorias.items():
                resultado[f"{grupo}/{nome}"] = url
                if verbose:
                    print(f"⚠ Fallback URL: {grupo}/{nome} -> {url}")
        return resultado

    # Se não houve falha global, retorna os links online normalmente
    for grupo, categorias in mapa_categorias.items():
        for nome, caminho in categorias.items():
            url_completa = BASE_URL + caminho
            resposta = get_response(url_completa, verbose=verbose)
            link_csv = extrair_link_csv(resposta.text)
            if link_csv:
                resultado[f"{grupo}/{nome}"] = link_csv
                if verbose:
                    print(f"✔ {grupo}/{nome}: {link_csv}")
            else:
                # Fallback para URL da nuvem se não encontrar o link
                url = CSV_CATEGORIAS.get(grupo, {}).get(nome)
                if url:
                    resultado[f"{grupo}/{nome}"] = url
                    if verbose:
                        print(f"⚠ Fallback URL (CSV não encontrado): {grupo}/{nome} -> {url}")
                else:
                    if verbose:
                        print(f"✘ CSV não encontrado em: {grupo}/{nome} e sem fallback disponível.")
    return resultado

# --- Execução direta (ex: para testes) ---
if __name__ == "__main__":
    """
    Executa a extração dos links CSV de todas as categorias e imprime os resultados.
    """
    try:
        links = obter_links_csv(verbose=True)
        print("\n--- Links CSV encontrados ---")
        for categoria, link in links.items():
            print(f"{categoria}: {link}")
    except RuntimeError as e:
        print(f"Processamento interrompido: {e}")