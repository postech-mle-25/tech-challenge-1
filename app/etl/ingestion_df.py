from app.etl.cleaning import load_all_data
from app.db import engine, get_session
from app.model.tables import Exporta, Importa, Producao, Comercio, Processamento
from sqlmodel import Session
from app.etl import constants

#TODO: remover imports desnecessários

def db_ingestion():
    dfs = load_all_data()
    modelos = [Comercio, Exporta, Importa, Processamento, Producao]

    with Session(engine) as session:
        for df, Modelo in zip(dfs, modelos):
            # Limpa valores nulos do DataFrame, se necessário
            df = df.where(df.notnull(), None)

            for coluna in constants.DB.INDEX_COLUMNS:
                if coluna in df.columns:
                    df = df[df[coluna].notnull()]
                    df = df[df[coluna].astype(str).str.strip() != '']
                    df = df[df[coluna].astype(str).str.lower() != 'none']

            # Transforma cada linha em um objeto da classe Modelo
            registros = [
                Modelo(**row)
                for row in df.to_dict(orient="records")
                if all(row.get(col) is not None for col in constants.DB.INDEX_COLUMNS)
            ]

            # Insere no banco
            session.add_all(registros)

        session.commit()

if __name__ == '__main__':
    db_ingestion()