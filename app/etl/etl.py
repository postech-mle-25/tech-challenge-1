import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

urls = {
    "Producao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02",
    "Processamento": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03",
    "Comercializacao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04",
    "Importação": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05",
    "Exportacao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06"
}

base_url = "http://vitibrasil.cnpuv.embrapa.br/"

def extract_csv(url, base_url, max_retentativas=10, tempo_espera=5):
    tentativas = 0
    while tentativas < max_retentativas:
        try:
            # Fazendo a requisição HTTP
            response = requests.get(url)
            
            # Verificando o status da resposta
            if response.status_code == 200:
                print(f"Conexão bem-sucedida: {url}")
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Encontrar o link para download do CSV
                link_element = soup.find("a", class_="footer_content", href=True)
                if link_element:
                    csv_url = base_url + link_element['href']
                    print(f"Lendo diretamente: {csv_url}")
                    
                    # Carregar o CSV diretamente no DataFrame
                    df = pd.read_csv(csv_url, sep=";")
                    return df
                else:
                    print(f"Link para download não encontrado em {url}")
                    return None
            else:
                print(f"Erro: Status {response.status_code}. Tentando novamente...")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar {url}: {e}. Tentando novamente...")
        
        # Incrementa o número de tentativas e espera antes de tentar novamente
        tentativas += 1
        time.sleep(tempo_espera)
    
    print(f"Falha ao acessar {url} após {max_retentativas} tentativas.")
    return None

def normalize_production(df):
    """
    Normaliza o DataFrame de produção, transformando colunas de anos em linhas e preenchendo valores nulos.
    """
    if df is None or df.empty:
        print("DataFrame vazio ou inválido. Normalização não realizada.")
        return None
    df = (
        df.melt(id_vars=["id", "control", "produto"], var_name="ano", value_name="valor")
        .rename(columns={"id": "id_control"})
    )
    df["valor"] = df["valor"].fillna(0)  # Preencher valores nulos com zero
    return df

# Testando rota isolada
# @app.get("/extract_production")
# def extract_data():
#     try:
#         df = extract_csv(urls["Producao"], base_url)
#         if df is not None:
#             normalized_df = normalize_production(df)
#             if normalized_df is not None:
#                 return JSONResponse(content=normalized_df.head().to_dict(orient="records"))
#             else:
#                 return JSONResponse(content={"error": "Falha ao normalizar os dados de produção"}, status_code=500)
#         else:
#             return JSONResponse(content={"error": "Falha ao extrair dados de produção"}, status_code=500)
#     except Exception as e:
#         return JSONResponse(content={"error": f"Erro inesperado: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    # Extraindo os dados de cada URL e normalizando
    df = extract_csv(urls["Producao"], base_url)  
    if df is not None:
        df = normalize_production(df)
        if df is not None:
            print(df.head())  
        else:
            print("Falha ao normalizar os dados de produção.")
    else:
        print("Falha ao extrair dados de produção.")