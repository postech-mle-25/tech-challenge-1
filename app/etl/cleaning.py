import pandas as pd
from collections import defaultdict
from app.etl.scraping import obter_links_csv
import csv
import requests
from io import StringIO
import re

def detectar_separador(url):
    """Identifica o separador usado em cada CSV."""
    response = requests.get(url)
    content = response.content.decode('utf-8')
    sample = "\n".join(content.splitlines()[:5])
    sniffer = csv.Sniffer()
    try:
        dialect = sniffer.sniff(sample)
        return dialect.delimiter
    except csv.Error:
        return ','

def read_and_transform(url, categoria):
    """Lê CSV da URL e transforma em formato longo."""
    sep = detectar_separador(url)
    df = pd.read_csv(url, sep=sep, encoding='utf-8', engine='python')

    # Converte todos os nomes das colunas para minúsculo
    df.columns = df.columns.str.lower()

    df['arquivo'] = categoria.split('/')[-1] + ".csv"
    df['pasta'] = categoria.split('/')[0]

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

    return df_long.reset_index(drop=True)

def remover_linhas_maiusculas(df):
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

    file_info = obter_links_csv(verbose = True)
    # Dicionário para guardar os dataframes por pasta
    dfs_por_pasta = defaultdict(list)

    # Loop pelos arquivos
    for categoria, url in file_info.items():
        pasta = categoria.split('/')[0]
        df = read_and_transform(url, categoria)
        dfs_por_pasta[pasta].append(df)

    # Junta todos os arquivos de cada pasta
    dfs_finais = {pasta: pd.concat(dfs, ignore_index=True) for pasta, dfs in dfs_por_pasta.items()}

    df_comercializacao = remover_linhas_maiusculas(dfs_finais['comercializacao'].drop(columns = 'produto'))
    df_exportacao = remover_linhas_maiusculas(dfs_finais['exportacao'])
    df_importacao = remover_linhas_maiusculas(dfs_finais['importacao'])
    df_processamento = remover_linhas_maiusculas(dfs_finais['processamento'].drop(columns = 'cultivar'))
    df_producao = remover_linhas_maiusculas(dfs_finais['producao'].drop(columns = 'produto'))

    dfs = [df_comercializacao, df_exportacao, df_importacao, df_processamento, df_producao]

    for i in range(len(dfs)):
        df = dfs[i]

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