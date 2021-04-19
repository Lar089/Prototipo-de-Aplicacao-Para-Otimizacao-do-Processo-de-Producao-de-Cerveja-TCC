
from pyschedule import Scenario
import json


class Fabrica:

    def __init__(self, filas={}, propagadores={}, fermentadores=[], maturadores=[], centrifugas=[], bombas_de_cip={}, desalcoolizador=[], linhas={}, fermentadores_BRHZ=[]):
        self._filas = filas
        self._fermentadores = fermentadores
        self._maturadores = maturadores
        self._centrifugas = centrifugas
        self._bombas_de_cip = bombas_de_cip
        self._desalcoolizador = desalcoolizador
        self._linhas = linhas
        self._propagadores = propagadores
        self._fermentadores_BRHZ = fermentadores_BRHZ

    @staticmethod
    def _LerJson_da_Fabrica():
        with open("./app/data/fabricas.json", "r") as read_file:
            estrutura_fabrica = json.load(read_file)
        return estrutura_fabrica

    @staticmethod
    def _BuscaAreaFria():  # Futuramente escolher qualquer area e retorna-la na função
        estrutura_fabrica = Fabrica._LerJson_da_Fabrica()
        area_fria = estrutura_fabrica['estrutura']['producao']['area_fria']        
        return area_fria

    @staticmethod
    def _remove_item(my_list, *args):
        deletar = list(args)
        for item in deletar:
            while item in my_list:
                my_list.remove(item)
        return my_list

    def BuscaFilas(self, Cervejaria):
        area_fria = self._BuscaAreaFria()        
        for fila in area_fria['filas']:            
            tanques = []
            if(fila['nome'] == "anel_19"):
                for tanque in fila["tanques"]:
                    tanques.append(Cervejaria.Resource(
                        name=tanque['nome'], cost_per_period=1))
                self._filas[fila["nome"]] = tanques
            else:
                for tanque in fila["tanques"]:
                    tanques.append(Cervejaria.Resource(
                        name=tanque['nome']))
                self._filas[fila['nome']] = tanques           
        

    def BuscaFermentadores(self):
        self._fermentadores = self._filas["anel_17"] + \
            self._filas["anel_18"] + self._filas["anel_19"]

    def BuscaMaturadores(self):
        self._maturadores = self._filas["anel_19"] + \
            self._filas["anel_20"]

    def BuscaPropagadores(self):
        tanque_17, tanque_18 = self._filas["anel_17"][-1], self._filas["anel_18"][-1]
        self._propagadores["fermentacao"] = [tanque_17, tanque_18]
        tanque_19, tanque_20 = self._filas["anel_19"][-1], self._filas["anel_20"][-1]
        self._propagadores["maturacao"] = [tanque_19, tanque_20]

    def BuscaFermentadores_BRHZ(self):
        self._fermentadores_BRHZ = self._filas["anel_18"] + \
            self._filas["anel_19"]
        self._fermentadores_BRHZ.pop(10)
        self._fermentadores_BRHZ.pop(20)

    def BuscaCentrifuga(self, Cervejaria):
        area_fria = Fabrica._BuscaAreaFria()
        for centrifuga in area_fria["centrifugas"]:
            self._centrifugas.append(
                Cervejaria.Resource(name=centrifuga["nome"]))

    def BuscaBombasCip(self, Cervejaria):
        area_fria = Fabrica._BuscaAreaFria()
        for bombas_de_cip in area_fria["Bombas_de_Cip"]:
            lista_de_bombas = []
            for bomba in bombas_de_cip["quantidade"]:
                lista_de_bombas.append(Cervejaria.Resource(bomba["nome"]))
            self._bombas_de_cip[bombas_de_cip["tipo"]] = lista_de_bombas

    def BuscaLinhas(self, Cervejaria):
        area_fria = Fabrica._BuscaAreaFria()
        for tipo_de_linha in area_fria["Linhas"]:
            lista_de_linhas = []
            for linha in tipo_de_linha["quantidade"]:
                lista_de_linhas.append(Cervejaria.Resource(linha["nome"]))
            self._linhas[tipo_de_linha["tipo"]] = lista_de_linhas

    def BuscaDesalcoolizador(self, Cervejaria):
        area_fria = Fabrica._BuscaAreaFria()
        for desalcoolizador in area_fria["Desalcoolizador"]:
            self._desalcoolizador.append(
                Cervejaria.Resource(name=desalcoolizador["nome"]))

    def gerarRecursos(self, Cervejaria):
        self.BuscaFilas(Cervejaria)
        self.BuscaCentrifuga(Cervejaria)
        self.BuscaBombasCip(Cervejaria)
        self.BuscaLinhas(Cervejaria)
        self.BuscaDesalcoolizador(Cervejaria)
        self.BuscaFermentadores()
        self.BuscaMaturadores()
        self.BuscaPropagadores()
        self.BuscaFermentadores_BRHZ()        

    @property
    def fermentadores(self):
        return self._fermentadores

    @property
    def maturadores(self):
        return self._maturadores

    @property
    def filas(self):
        return self._filas

    @property
    def propagadores(self):
        return self._propagadores

    @property
    def centrifugas(self):
        return self._centrifugas

    @property
    def bombas_de_cip(self):
        return self._bombas_de_cip

    @property
    def linhas(self):
        return self._linhas

    @property
    def desalcoolizador(self):
        return self._desalcoolizador

    @property
    def fermentadores_BRHZ(self):
        return self._fermentadores_BRHZ
