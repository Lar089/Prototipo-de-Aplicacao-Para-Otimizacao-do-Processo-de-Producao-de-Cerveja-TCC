
'''
def _ChecarBrahmaZero(malha_producao):
    for cerveja in malha_producao:
        if (cerveja["nome"] == "BRHZ"):
            return True
        else:
            return False  
'''
# Definir as variáveis de estado...


def _gerarArriamento(Cervejaria: object, atividade, malha_producao):
    for cerveja in malha_producao:
        atividade["arriar"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
            "arriar" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["arriar"]["duracao"])


def _gerarTarefas_Processo(Cervejaria: object, atividade, malha_producao):    
    for cerveja in malha_producao:
        atividade["fermentar_1"]["tarefas"][cerveja["SIGLA"]] = (Cervejaria.Tasks(
            "ferm_1" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["fermentar_1"]["duracao"]))
        atividade["recolha"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
            "rec" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["recolha"]["duracao"])
        atividade["fermentar_2"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
            "ferm_2" + cerveja["SIGLA"], num=cerveja["tanques"], length=cerveja["Tempo_fermentacao"])
        atividade["centrifugar"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
            "centri" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["centrifugar"]["duracao"])
        atividade["maturar"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
            "mat" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["maturar"]["duracao"])
    
        atividade["filtragem"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
            "filt" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["filtragem"]["duracao"])
    

def _gerarTarefasBrahma_Zero(Cervejaria: object, atividade, malha_producao):
    for cerveja in malha_producao:
        if(cerveja["SIGLA"] == "BRHZ"):
            atividade["desalcoolizar"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
                "desal" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["desalcoolizar"]["duracao"])
            atividade["decantar"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
                "dec" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["decantar"]["duracao"])
            atividade["CIP_POS_desalcoolizacao"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
                "CIPdes" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["CIP_POS_desalcoolizacao"]["duracao"])

def _gerarTarefas_CIP(Cervejaria: object, atividade, malha_producao):
    bloqueios = {'block_anel17': 1, 'block_anel18': 1, 'block_anel19': 1, 'block_anel20': 1}
    for cerveja in malha_producao:
        #atividade["CIP_dosagem"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
            #"CIPd" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["CIP_dosagem"]["duracao"])                
        atividade["CIP_recolha"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
            "CIPr" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["CIP_recolha"]["duracao"])        
        atividade["CIP_maturada"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
            "CIPlm" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["CIP_maturada"]["duracao"])
        atividade["CIPc_centrifuga"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
            "CIPc" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["CIPc_centrifuga"]["duracao"])
        #atividade["CIPl_centrifuga"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
            #"CIPl" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["CIPl_centrifuga"]["duracao"])
        atividade["CIP_fermentador"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
            "CIPf" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["CIP_fermentador"]["duracao"], **bloqueios)
        atividade["CIP_maturador"]["tarefas"][cerveja["SIGLA"]] = Cervejaria.Tasks(
            "CIPm" + cerveja["SIGLA"], num=cerveja["tanques"], length=atividade["CIP_maturador"]["duracao"], **bloqueios)

    
def gerarTodasAtividades(Cervejaria: object, atividade, malha_producao):
    print('_gerarTarefas_CIP')
    _gerarTarefas_CIP(Cervejaria, atividade, malha_producao)
    print('_gerarTarefas_Processo')
    _gerarTarefas_Processo(Cervejaria, atividade, malha_producao)
    print('_gerarArriamento')
    _gerarArriamento(Cervejaria, atividade, malha_producao)
    print('_gerarTarefasBrahma_Zero')
    _gerarTarefasBrahma_Zero(Cervejaria, atividade, malha_producao)
