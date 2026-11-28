
from model.clientes import Cliente
from conexion.mongo_queries import MongoQueries
from utils import config


class Controller_Cliente:
    def __init__(self):
        self.mongo = MongoQueries()

    def solicitar_cpf(self, mensagem: str) -> str:
        while True:
            cpf = input(mensagem).strip()
            if cpf == "0":
                return None
            if cpf:
                return cpf
            print("O CPF não pode ser vazio.")

    def inserir_cliente(self) -> Cliente:
        cpf = self.solicitar_cpf("CPF (Novo, 0 para voltar): ")
        if cpf is None:
            return None

        self.mongo.connect()
        if self.mongo.db["clientes"].find_one({"cpf": cpf}) is not None:
            self.mongo.close()
            print(f"O CPF {cpf} já está cadastrado.")
            return None

        nome = input("Nome (Novo): ").strip()
        telefone = input("Telefone (Novo): ").strip()
        documento = {"cpf": cpf, "nome": nome, "telefone": telefone, "ativo": "S"}
        self.mongo.db["clientes"].insert_one(documento)
        self.mongo.close()
        novo = Cliente(cpf, nome, telefone, "S")
        print(novo.to_string())
        return novo

    def atualizar_cliente(self) -> Cliente:
        cpf = self.solicitar_cpf("CPF do cliente que deseja alterar (0 para voltar): ")
        if cpf is None:
            return None

        self.mongo.connect()
        documento = self.mongo.db["clientes"].find_one({"cpf": cpf})
        if documento is None:
            self.mongo.close()
            print(f"O CPF {cpf} não existe.")
            return None

        novo_nome = input("Nome (Novo): ").strip()
        novo_telefone = input("Telefone (Novo): ").strip()
        ativo = input("Cliente ativo? [S/N]: ").strip().upper()
        while ativo not in ("S", "N"):
            ativo = input("Opção inválida. Informe S ou N: ").strip().upper()

        self.mongo.db["clientes"].update_one(
            {"cpf": cpf},
            {"$set": {"nome": novo_nome, "telefone": novo_telefone, "ativo": ativo}},
        )
        self.mongo.close()
        atualizado = Cliente(cpf, novo_nome, novo_telefone, ativo)
        print(atualizado.to_string())
        return atualizado

    def excluir_cliente(self):
        self.mongo.connect()
        clientes = list(self.mongo.db["clientes"].find({}, {"cpf": 1, "nome": 1}).sort("nome", 1))
        if not clientes:
            self.mongo.close()
            print("Não há clientes cadastrados para excluir.")
            return

        print("\nClientes:")
        for indice, cliente in enumerate(clientes, start=1):
            print(f"[{indice}] CPF: {cliente['cpf']} | Nome: {cliente['nome']}")

        opcoes = ("0",) + tuple(str(indice) for indice in range(1, len(clientes) + 1))
        opcao = config.solicitar_opcao("Selecione o cliente que deseja excluir (0 para cancelar): ", opcoes)
        if opcao == "0":
            self.mongo.close()
            return

        cpf = clientes[int(opcao) - 1]["cpf"]
        confirmar = config.solicitar_opcao(f"Confirma a exclusão permanente do cliente {cpf}? [S/N]: ", ("S", "N"))
        if confirmar != "S":
            self.mongo.close()
            print("Exclusão cancelada.")
            return

        locacoes = list(self.mongo.db["locacao"].find({"cpf": cpf}, {"codigo_locacao": 1}))
        if locacoes:
            confirmar_locacoes = config.solicitar_opcao(
                f"Este cliente possui {len(locacoes)} locação(ões). Deseja excluir também essas locações? [S/N]: ",
                ("S", "N"),
            )
            if confirmar_locacoes != "S":
                self.mongo.close()
                print("O cliente não pode ser excluído enquanto houver locações vinculadas.")
                return
            self.mongo.db["locacao"].delete_many({"cpf": cpf})

        self.mongo.db["clientes"].delete_one({"cpf": cpf})
        self.mongo.close()
        print(f"Cliente {cpf} excluído com sucesso.")
