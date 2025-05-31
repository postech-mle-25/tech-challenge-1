import unicodedata

import pandas as pd
from collections import defaultdict
from etl.scraping import obter_links_csv, CSV_CATEGORIAS
import csv
import requests
import time
import os

def detectar_separador(url):
    """
    Identifica o separador usado em um arquivo CSV a partir de uma URL.

    Parâmetros:
        url (str): URL do arquivo CSV.

    Retorna:
        str: Delimitador detectado (ex: ',' ou ';').
    """
    response = requests.get(url)
    content = response.content.decode('utf-8')
    sample = "\n".join(content.splitlines()[:5])
    sniffer = csv.Sniffer()
    try:
        dialect = sniffer.sniff(sample)
        return dialect.delimiter
    except csv.Error:
        return ','

DOWNLOADS_ROOT = os.path.join(os.path.dirname(__file__), "downloads")

def read_and_transform(url, categoria, online=True):
    """
    Lê um arquivo CSV (online ou local) e transforma em formato longo (long format).

    Parâmetros:
        url (str): URL do arquivo CSV.
        categoria (str): Categoria/nome do arquivo para organização local.
        online (bool): Se True, tenta baixar online; senão, lê apenas localmente.

    Retorna:
        pd.DataFrame: DataFrame transformado no formato longo.

    Exceções:
        FileNotFoundError: Se o arquivo local não for encontrado.
        ValueError: Se o arquivo estiver vazio ou corrompido.
    """
    sep = None
    df = None
    erro_online = False

    # Só tenta baixar online se online=True e url for http
    if online and url.startswith("http"):
        for tentativa in range(3):
            try:
                sep = detectar_separador(url)
                df = pd.read_csv(url, sep=sep, encoding='utf-8', engine='python')
                if not df.empty:
                    break
            except Exception:
                erro_online = True
                time.sleep(2)
        else:
            erro_online = True
    else:
        # Não tenta baixar online, já vai para o local
        erro_online = True
        df = None

    # Fallback local se falhar online ou DataFrame vazio
    if erro_online or df is None or df.empty:
        # Caminho local garantido conforme estrutura
        pasta = categoria.split('/')[0]
        nome = categoria.split('/')[-1]
        local_path = os.path.join(DOWNLOADS_ROOT, pasta, f"{nome}.csv")
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {local_path}")
        # Detecta separador localmente
        with open(local_path, encoding='utf-8') as f:
            sample = "\n".join([next(f) for _ in range(5)])
            sniffer = csv.Sniffer()
            try:
                dialect = sniffer.sniff(sample)
                sep = dialect.delimiter
            except csv.Error:
                sep = ','
        df = pd.read_csv(local_path, sep=sep, encoding='utf-8', engine='python')
        if df.empty:
            raise ValueError(f"Arquivo local {local_path} está vazio ou corrompido.")

    # Normalização e transformação igual para ambos os fluxos
    df.columns = df.columns.str.lower()
    cat = categoria.split('/')[-1].split('_')
    cat = cat[0] if len(cat) == 1 else "_".join(cat[1:])
    df["tipo"] = cat

    # Detecta colunas de quantidade e valor
    cols_quantidade = [col for col in df.columns if col.isdigit()]
    cols_valor = [col for col in df.columns if col.endswith('.1') and col.replace('.1', '').isdigit()]
    id_vars = [col for col in df.columns if col not in cols_quantidade + cols_valor]

    # Transforma os dados
    quant_df = df.melt(id_vars=id_vars, value_vars=cols_quantidade, var_name='ano', value_name='quantidade')
    if cols_valor:
        valor_df = df.melt(id_vars=id_vars, value_vars=cols_valor, var_name='ano', value_name='valor')
        valor_df['ano'] = valor_df['ano'].str.replace('.1', '', regex=False)
        df_long = pd.merge(quant_df, valor_df, on=id_vars + ['ano'], how='outer')
    else:
        df_long = quant_df

    # Garante que o DataFrame final não está vazio
    if df_long.empty:
        raise ValueError(f"Transformação resultou em DataFrame vazio para {categoria} (url: {url})")

    if 'ano' in df_long.columns:
        df_long['ano'] = pd.to_numeric(df_long['ano'], errors='coerce').astype('Int64')

    return df_long.reset_index(drop=True)

def remover_linhas_maiusculas(df):
    """
    Remove linhas do DataFrame onde todas as colunas de texto estão em maiúsculas.

    Parâmetros:
        df (pd.DataFrame): DataFrame de entrada.

    Retorna:
        pd.DataFrame: DataFrame sem as linhas totalmente em maiúsculas.
    """
    # Seleciona colunas de texto
    colunas_texto = df.select_dtypes(include=['object', 'string']).columns.tolist()

    def contem_maiuscula_total(linha):
        for col in colunas_texto:
            valor = linha[col]
            if pd.notna(valor) and isinstance(valor, str) and valor.isupper():
                return True
        return False

    return df[~df.apply(contem_maiuscula_total, axis=1)].reset_index(drop=True)

def load_all_data():
    """
    Carrega todos os arquivos CSV disponíveis (online ou local), transforma e retorna uma lista de DataFrames.

    Retorna:
        list: Lista de DataFrames carregados e transformados.
    """
    file_info = {}
    online_ok = True

    # Tenta obter todos os links online de uma vez só
    try:
        file_info = obter_links_csv(verbose=True)
        # Testa se pelo menos um arquivo online está acessível
        for url in file_info.values():
            if url.startswith("http"):
                try:
                    resp = requests.head(url, timeout=5)
                    if resp.status_code != 200:
                        online_ok = False
                        print(f"[ERRO] Não foi possível acessar o arquivo online: {url} (status {resp.status_code})")
                        break
                except Exception as ex:
                    online_ok = False
                    print(f"[ERRO] Falha ao tentar acessar {url}: {ex}")
                    break
        if not online_ok:
            raise Exception("Nenhum arquivo online disponível para download.")
    except Exception as e:
        print(f"[ERRO] Falha ao obter links online ou acessar arquivos: {e}")
        # Fallback para as URLs reais da Azure Blob Storage
        file_info = {}
        for grupo, categorias in CSV_CATEGORIAS.items():
            for nome, url in categorias.items():
                file_info[f"{grupo}/{nome}"] = url
        online_ok = True

    dfs_por_pasta = defaultdict(list)

    # Loop pelos arquivos
    for categoria, url in file_info.items():
        pasta = categoria.split('/')[0]
        try:
            df = read_and_transform(url, categoria, online = online_ok)
            dfs_por_pasta[pasta].append(df)
            print(f"[OK] Carregado {categoria} ({url}) com {len(df)} linhas.")
        except FileNotFoundError as fnf:
            print(f"[ERRO] Arquivo não encontrado para {categoria}: {fnf}")
        except ValueError as ve:
            print(f"[ERRO] Erro de valor ao carregar {categoria} ({url}): {ve}")
        except Exception as e:
            print(f"[ERRO] Erro inesperado ao carregar {categoria} ({url}): {e}")

    # Junta todos os arquivos de cada pasta
    dfs_finais = {pasta: pd.concat(dfs, ignore_index=True) for pasta, dfs in dfs_por_pasta.items()}


    df_comercializacao = remover_linhas_maiusculas(dfs_finais['comercializacao'])#.drop(columns = 'produto'))
    df_exportacao = remover_linhas_maiusculas(dfs_finais['exportacao'])
    df_importacao = remover_linhas_maiusculas(dfs_finais['importacao'])
    df_processamento = remover_linhas_maiusculas(dfs_finais['processamento'])#.drop(columns = 'cultivar'))
    df_producao = remover_linhas_maiusculas(dfs_finais['producao'])#.drop(columns = 'produto'))


    dfs = [df_comercializacao, df_exportacao, df_importacao, df_processamento, df_producao]

    dfs = [df.rename(columns=lambda col: remover_acentos(col)) for df in dfs]

    for i in range(len(dfs)):
        df = dfs[i]

        #remove 'tipo' se houver apenas um
        num_tipos = len(set(df.tipo))
        if num_tipos <=1:
            df.drop(columns='tipo', inplace=True)

        # Remove coluna 'Id', se existir (ignorando capitalização)
        lower_cols = [col.lower() for col in df.columns]
        if 'id' in lower_cols:
            df.drop(columns=[col for col in df.columns if col.lower() == 'id'][0], inplace=True)

        # Remove linhas onde Quantidade e (se existir) Valor são ambos zero
        df = df[~((df['quantidade'] == 0) & (df.get('valor', 0) == 0))]

        # Remove duplicatas
        df.drop_duplicates(inplace=True)

        # Resetar índice
        df.reset_index(drop=True, inplace=True)

        # Atualiza o dataframe na lista

        dfs[i] = df
    return dfs


# Função para remover acentos
def remover_acentos(texto):
    if isinstance(texto, str):
        return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto


if __name__ == "__main__":
    """
    Executa o carregamento de todos os DataFrames e exibe informações básicas de cada um.
    """
    dfs = load_all_data()
    if dfs and len(dfs) > 0:
        for df in dfs:
            print(df.head())
            print(df.info())
    else:
        print("[AVISO] Nenhum DataFrame foi carregado.")