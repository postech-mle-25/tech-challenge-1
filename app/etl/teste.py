import pandas as pd

CSV_BASE_PATH = r"C:\Pos-Fiap\Tech1\tech-challenge-1\app\etl\downloads"

CSV_CATEGORIAS = {
    "producao": {
        "producao": f"{CSV_BASE_PATH}\\producao\\producao.csv",
    },
    "processamento": {
        "pro_viniferas": f"{CSV_BASE_PATH}\\processamento\\pro_viniferas.csv",
        "pro_americanas_hibridas": f"{CSV_BASE_PATH}\\processamento\\pro_americanas_hibridas.csv",
        "pro_uvas_de_mesa": f"{CSV_BASE_PATH}\\processamento\\pro_uvas_de_mesa.csv",
        "pro_sem_classificacao": f"{CSV_BASE_PATH}\\processamento\\pro_sem_classificacao.csv",
    },
    "comercializacao": {
        "comercializacao": f"{CSV_BASE_PATH}\\comercializacao\\comercializacao.csv",
    },
    "importacao": {
        "imp_vinho_de_mesa": f"{CSV_BASE_PATH}\\importacao\\imp_vinho_de_mesa.csv",
        "imp_espumantes": f"{CSV_BASE_PATH}\\importacao\\imp_espumantes.csv",
        "imp_uvas_frescas": f"{CSV_BASE_PATH}\\importacao\\imp_uvas_frescas.csv",
        "imp_uvas_passas": f"{CSV_BASE_PATH}\\importacao\\imp_uvas_passas.csv",
        "imp_suco_de_uva": f"{CSV_BASE_PATH}\\importacao\\imp_suco_de_uva.csv",
    },
    "exportacao": {
        "exp_vinhos_de_mesa": f"{CSV_BASE_PATH}\\exportacao\\exp_vinhos_de_mesa.csv",
        "exp_espumantes": f"{CSV_BASE_PATH}\\exportacao\\exp_espumantes.csv",
        "exp_uvas_frescas": f"{CSV_BASE_PATH}\\exportacao\\exp_uvas_frescas.csv",
        "exp_uvas_passas": f"{CSV_BASE_PATH}\\exportacao\\exp_uvas_passas.csv",
        "exp_suco_de_uva": f"{CSV_BASE_PATH}\\exportacao\\exp_suco_de_uva.csv",
    },
}


if __name__ == "__main__":
    for categoria, arquivos in CSV_CATEGORIAS.items():
        for nome, caminho in arquivos.items():
            try:
                df = pd.read_csv(caminho)
                print(f"[OK] {categoria}/{nome}: {len(df)} registros")
            except Exception as e:
                print(f"[ERRO] {categoria}/{nome}: {e}")

    