from model.carros import Carros
from conexion.mongo_queries import MongoQueries
from utils import config
import math


class Controller_Carro:
    def __init__(self):
        self.mongo = MongoQueries()

    def solicitar_placa(self, mensagem: str) -> str:
        while True:
            placa = input(mensagem).strip().upper()
            if placa == "0":
                return None
            if placa:
                return placa
            print("A placa não pode ser vazia.")

    def inserir_carro(self) -> Carros:
        placa = self.solicitar_placa("Placa (Nova, 0 para voltar): ")
        if placa is None:
            return None
        self.mongo.connect()
        if self.mongo.db["carros"].find_one({"placa": placa}) is not None:
            self.mongo.close()
            print(f"O carro com placa {placa} já está cadastrado.")
            return None
        marca = input("Marca (Nova): ").strip()
        modelo = input("Modelo (Novo): ").strip()
        valor_diaria = self.solicitar_valor_diaria()
        documento = {"placa": placa, "marca": marca, "modelo": modelo,
                     "valor_diaria": valor_diaria, "ativo": "S"}
        self.mongo.db["carros"].insert_one(documento)
        self.mongo.close()
        novo = Carros(placa, marca, modelo, valor_diaria, "S")
        print(novo.to_string())
        return novo

    def atualizar_carro(self) -> Carros:
        placa = self.solicitar_placa("Placa do carro que deseja atualizar (0 para voltar): ")
        if placa is None:
            return None
        self.mongo.connect()
        documento = self.mongo.db["carros"].find_one({"placa": placa})
        if documento is None:
            self.mongo.close()
            print(f"O carro com placa {placa} não existe.")
            return None
        marca = input("Marca (Nova): ").strip()
        modelo = input("Modelo (Novo): ").strip()
        valor_diaria = self.solicitar_valor_diaria()
        ativo = input("Carro ativo? [S/N]: ").strip().upper()
        while ativo not in ("S", "N"):
            ativo = input("Opção inválida. Informe S ou N: ").strip().upper()
        self.mongo.db["carros"].update_one(
            {"placa": placa},
            {"$set": {"marca": marca, "modelo": modelo,
                      "valor_diaria": valor_diaria, "ativo": ativo}},
        )
        self.mongo.close()
        atualizado = Carros(placa, marca, modelo, valor_diaria, ativo)
        print(atualizado.to_string())
        return atualizado

    def excluir_carro(self):
        self.mongo.connect()
        carros = list(self.mongo.db["carros"].find(
            {}, {"placa": 1, "marca": 1, "modelo": 1}).sort("placa", 1))
        if not carros:
            self.mongo.close()
            print("Não há veículos cadastrados para excluir.")
            return

        print("\nVeículos:")
        for indice, carro in enumerate(carros, start=1):
            print(f"[{indice}] Placa: {carro['placa']} | {carro['marca']} {carro['modelo']}")

        opcoes = ("0",) + tuple(str(indice) for indice in range(1, len(carros) + 1))
        opcao = config.solicitar_opcao("Selecione o veículo que deseja excluir (0 para cancelar): ", opcoes)
        if opcao == "0":
            self.mongo.close()
            return

        placa = carros[int(opcao) - 1]["placa"]
        confirmar = config.solicitar_opcao(
            f"Confirma a exclusão permanente do veículo {placa}? [S/N]: ", ("S", "N"))
        if confirmar != "S":
            self.mongo.close()
            print("Exclusão cancelada.")
            return

        locacoes = list(self.mongo.db["locacao"].find({"placa": placa}, {"codigo_locacao": 1}))
        if locacoes:
            confirmar_locacoes = config.solicitar_opcao(
                f"Este veículo possui {len(locacoes)} locação(ões). Deseja excluir também essas locações? [S/N]: ",
                ("S", "N"))
            if confirmar_locacoes != "S":
                self.mongo.close()
                print("O veículo não pode ser excluído enquanto houver locações vinculadas.")
                return
            self.mongo.db["locacao"].delete_many({"placa": placa})

        self.mongo.db["carros"].delete_one({"placa": placa})
        self.mongo.close()
        print(f"Veículo {placa} excluído com sucesso.")

    def solicitar_valor_diaria(self) -> float:
        while True:
            entrada = input("Valor da Diária (Novo): ").strip().replace(",", ".")
            try:
                valor = float(entrada)
            except ValueError:
                print("Valor inválido. Informe um número, por exemplo 150.00.")
                continue
            if not math.isfinite(valor) or valor <= 0:
                print("A diária deve ser um valor positivo.")
                continue
            return valor
