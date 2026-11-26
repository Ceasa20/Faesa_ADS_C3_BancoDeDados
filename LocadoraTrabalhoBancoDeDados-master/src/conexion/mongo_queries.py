
###########################################################################
# Essa classe auxilia na conexão com o Banco de Dados não relacional MongoDB
#
# Segue a mesma estrutura de OracleQueries: as credenciais ficam em
# conexion/passphrase/authentication.mongo e o caminho é resolvido a partir
# da localização deste módulo, para que funcione independente do diretório
# de onde a aplicação for executada.
###########################################################################
from pathlib import Path
from urllib.parse import quote_plus

import pymongo


class MongoQueries:

    def __init__(self):
        self.host = "localhost"
        self.port = 27017
        self.database_name = "labdatabase"

        # Inicializa os atributos para evitar erros se a conexão falhar.
        self.mongo_client = None
        self.db = None

        credentials_path = (
            Path(__file__).resolve().parent
            / "passphrase"
            / "authentication.mongo"
        )

        with credentials_path.open(encoding="utf-8") as f:
            self.user, self.passwd = f.read().strip().split(",", 1)

        self.user = self.user.strip()
        self.passwd = self.passwd.strip()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    def connectionString(self) -> str:
        """
        Monta a URI de conexão com o MongoDB.
        quote_plus escapa caracteres especiais de usuário e senha.
        """
        return (
            f"mongodb://{quote_plus(self.user)}:{quote_plus(self.passwd)}"
            f"@{self.host}:{self.port}/"
        )

    def connect(self):
        """
        Abre a conexão e seleciona o banco de dados. Retorna o objeto de
        banco, para que o chamador possa acessar as coleções diretamente.
        """
        self.mongo_client = pymongo.MongoClient(self.connectionString())
        self.db = self.mongo_client[self.database_name]
        return self.db

    def count_documents(self, collection: str, query: dict = None) -> int:
        """
        Conta os documentos de uma coleção, com filtro opcional.
        Usado pela Splash Screen para informar o total de cada coleção.
        """
        return self.db[collection].count_documents(query or {})

    def close(self):
        if self.mongo_client is not None:
            self.mongo_client.close()
            self.mongo_client = None
            self.db = None
