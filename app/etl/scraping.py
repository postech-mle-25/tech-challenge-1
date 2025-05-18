import requests
from bs4 import BeautifulSoup
import time

# --- Configurações ---
BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
MAX_TENTATIVAS = 10
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

# --- Funções utilitárias ---

def get_response(url, max_tentativas=MAX_TENTATIVAS, espera=ESPERA_SEGUNDOS, verbose=False):
    """Tenta fazer uma requisição até obter resposta 200 ou atingir o limite de tentativas."""
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
    """Extrai o link do CSV a partir do HTML da página."""
    soup = BeautifulSoup(html, "html.parser")
    link_tag = soup.find("span", class_="spn_small", text="DOWNLOAD")
    if link_tag and link_tag.parent.name == "a":
        return BASE_URL + link_tag.parent.get("href", "")
    return None

def obter_links_csv(mapa_categorias=URLS_CATEGORIAS, verbose=False):
    """Percorre todas as categorias e retorna os links CSV encontrados."""
    resultado = {}
    for grupo, categorias in mapa_categorias.items():
        for nome, caminho in categorias.items():
            url_completa = BASE_URL + caminho
            resposta = get_response(url_completa, verbose=verbose)
            if not resposta:
                if verbose:
                    print(f"Erro ao acessar: {url_completa}")
                continue
            link_csv = extrair_link_csv(resposta.text)
            if link_csv:
                resultado[f"{grupo}/{nome}"] = link_csv
                if verbose:
                    print(f"✔ {grupo}/{nome}: {link_csv}")
            else:
                if verbose:
                    print(f"✘ CSV não encontrado em: {grupo}/{nome}")
    return resultado

# --- Execução direta (ex: para testes) ---
if __name__ == "__main__":
    links = obter_links_csv(verbose=True)
    print("\n--- Links CSV encontrados ---")
    for categoria, link in links.items():
        print(f"{categoria}: {link}")

