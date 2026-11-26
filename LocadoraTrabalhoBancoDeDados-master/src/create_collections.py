###########################################################################
# Script de criação das coleções no MongoDB e carga dos documentos.
#
# Atende ao item 4 do edital:
#   I.   Conectar ao banco de dados relacional Oracle
#   II.  Consultar cada uma das tabelas existentes do projeto da C2
#   III. Conectar ao banco de dados não relacional MongoDB
#   IV.  Criar uma coleção com o mesmo nome de cada tabela
#   V.   Criar os documentos a partir dos registros pré-cadastrados
#
# Execute a partir da pasta src:  python create_collections.py
###########################################################################
import json
import logging

from pandas import to_datetime

from conexion.mongo_queries import MongoQueries
from conexion.oracle_queries import OracleQueries

# Uma coleção para cada tabela do diagrama relacional.
LIST_OF_COLLECTIONS = ["clientes", "carros", "locacao"]

# O MongoDB não possui o tipo DATE do Oracle, então as datas são gravadas
# como texto no formato dd/mm/aaaa. DATA_FIM_LOCACAO aceita nulo.
DATE_COLUMNS = {
    "locacao": [
        "data_inicio_locacao",
        "data_previsao_locacao",
        "data_fim_locacao",
    ],
}
DATE_FORMAT = "%d/%m/%Y"

logger = logging.getLogger(name="Locadora_CRUD_MongoDB")
logger.setLevel(level=logging.WARNING)

mongo = MongoQueries()


def createCollections(drop_if_exists: bool = False):
    """
    Lista as coleções existentes e verifica se as coleções do projeto estão
    entre elas.
        - Se existir e drop_if_exists for True: apaga a coleção e recria.
        - Se existir e drop_if_exists for False: não faz nada.
        - Se não existir: cria a coleção.
    """
    mongo.connect()
    existing_collections = mongo.db.list_collection_names()

    for collection in LIST_OF_COLLECTIONS:
        if collection in existing_collections:
            if drop_if_exists:
                mongo.db.drop_collection(collection)
                logger.warning(f"{collection} droped!")
                mongo.db.create_collection(collection)
                logger.warning(f"{collection} created!")
        else:
            mongo.db.create_collection(collection)
            logger.warning(f"{collection} created!")

    mongo.close()


def normalize_dates(df, collection: str):
    """
    Converte as colunas de data do Oracle para texto no formato dd/mm/aaaa.
    Datas nulas (DATA_FIM_LOCACAO de locações em aberto) viram None.
    """
    for column in DATE_COLUMNS.get(collection, []):
        if column in df.columns:
            convertido = to_datetime(df[column], errors="coerce")
            df[column] = convertido.dt.strftime(DATE_FORMAT)
            df[column] = df[column].where(df[column].notna(), None)

    return df


def insert_many(data, collection: str):
    """Insere a lista de documentos na coleção informada."""
    mongo.connect()
    mongo.db[collection].insert_many(data)
    mongo.close()


def extract_and_insert():
    """
    Extrai os registros de cada tabela do Oracle e os grava como documentos
    na coleção de mesmo nome no MongoDB.
    """
    oracle = OracleQueries()
    oracle.connect()
    sql = "select * from labdatabase.{table}"

    for collection in LIST_OF_COLLECTIONS:
        df = oracle.sqlToDataFrame(sql.format(table=collection))
        logger.warning(
            f"data extracted from database Oracle labdatabase.{collection}"
        )

        if df.empty:
            logger.warning(f"{collection} has no records to migrate")
            continue

        df = normalize_dates(df, collection)
        records = list(json.loads(df.T.to_json()).values())
        logger.warning("data converted to json")

        insert_many(data=records, collection=collection)
        logger.warning(f"documents generated at {collection} collection")

    oracle.close()


if __name__ == "__main__":
    logging.warning("Starting")
    createCollections(drop_if_exists=True)
    extract_and_insert()
    logging.warning("End")
