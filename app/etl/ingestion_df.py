from app.etl.cleaning import load_all_data
from app.db import engine, get_session
from app.model.tables import Exporta, Importa, Producao, Comercio, Processamento
from sqlmodel import Session
from app.etl import constants

#TODO: remover imports desnecessários

def db_ingestion():
    dfs = load_all_data()
    for df, modelo in zip(dfs, ["Comercio", "Exporta", "Importa", "Processamento", "Producao"]):
        print(f"{modelo}: {df.shape}")
    modelos = [Comercio, Exporta, Importa, Processamento, Producao]

    with Session(engine) as session:
        for df, Modelo in zip(dfs, modelos):
            model_name = Modelo.__name__
            index_columns = constants.DB.INDEX_COLUMNS_MAP[model_name]

            df = df.where(df.notnull(), None)

            for coluna in index_columns:
                if coluna in df.columns:
                    df = df[df[coluna].notnull()]
                    df = df[df[coluna].astype(str).str.strip() != '']
                    df = df[df[coluna].astype(str).str.lower() != 'none']

            registros = []
            for row in df.to_dict(orient="records"):
                missing = [col for col in index_columns if col not in row or row[col] is None]
                if not missing:
                    registros.append(Modelo(**row))

            print(f"Inserindo {len(registros)} registros na tabela {Modelo.__tablename__}")
            session.add_all(registros)

        session.commit()

if __name__ == '__main__':
    db_ingestion()