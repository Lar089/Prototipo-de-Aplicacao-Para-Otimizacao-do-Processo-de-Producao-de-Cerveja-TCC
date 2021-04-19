from pyschedule import alt
import json


def _LerJson_Cervejas():
    with open("./app/data/cervejas.json", "r") as read_file:
        cerveja = json.load(read_file)
    return cerveja

def _ChecarBrahmaZero(atividade):
    if ("BRHZ" in atividade["desalcoolizar"]["tarefas"].keys()):
        return True
    else:
        return False  


def recursos_Arriamento(Cervejaria, atividade, recursos):
    cerveja = _LerJson_Cervejas()
    lista_propagação = []
    propagadores_em_uso = 0
    for marca, lista_tarefas in atividade["arriar"]["tarefas"].items():
        if(marca in cerveja["producao"]["sala_2"]):
            if(marca == 'BRHZ'):
                for tarefa in lista_tarefas:
                    tarefa += recursos.linhas["Dosagem"][1] 
                    tarefa += alt(recursos.fermentadores_BRHZ)

            elif(marca[0] == 'P'):
                for tarefa in lista_tarefas:
                    lista_propagação.append(tarefa)
                    if(propagadores_em_uso != 2):
                        tarefa += recursos.linhas["Dosagem"][1]
                        tarefa += alt(recursos.propagadores["fermentacao"])
                        propagadores_em_uso += 1
                    else:
                        tarefa += recursos.linhas["Dosagem"][1]
                        tarefa += alt(recursos.fermentadores)
            else:
                for tarefa in lista_tarefas:
                    tarefa += recursos.linhas["Dosagem"][1]
                    tarefa += alt(recursos.fermentadores)

        else:
            if(marca[0] == 'P'):
                for tarefa in lista_tarefas:
                    lista_propagação.append(tarefa)
                    if(propagadores_em_uso != 2):
                        tarefa += recursos.linhas["Dosagem"]
                        tarefa += alt(recursos.propagadores["fermentacao"])
                        propagadores_em_uso += 1
                    else:
                        tarefa += recursos.linhas["Dosagem"]
                        tarefa += alt(recursos.fermentadores)

            else:
                for tarefa in lista_tarefas:
                    tarefa += recursos.linhas["Dosagem"]
                    tarefa += alt(recursos.fermentadores)
    
    for propagacao in lista_propagação[2:]:
        Cervejaria += lista_propagação[0] < propagacao
        Cervejaria += lista_propagação[1] < propagacao
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

def ordenamento_Fermentacao(Cervejaria, atividade, recursos):
    for marca, lista_arriamento in atividade["arriar"]["tarefas"].items():
        for marca_2, lista_fermentacao in atividade["fermentar_1"]["tarefas"].items():
            if(marca == marca_2):
                for index, tarefa_arriar in enumerate(lista_arriamento):
                    for index_2, tarefa_fermentar in enumerate(lista_fermentacao):
                        if(index == index_2):
                            tarefa_fermentar += alt(recursos.fermentadores)
                            tarefa_fermentar += tarefa_arriar*recursos.fermentadores
                            Cervejaria += tarefa_fermentar >= tarefa_arriar

    for marca, lista_fermentacao in atividade["fermentar_1"]["tarefas"].items():
        for marca_2, lista_recolhas in atividade["recolha"]["tarefas"].items():
            if(marca == marca_2):
                for index, tarefa_fermentar in enumerate(lista_fermentacao):
                    for index_2, tarefa_recolha in enumerate(lista_recolhas):
                        if(index == index_2):
                            tarefa_recolha += alt(recursos.linhas["Recolha"])
                            tarefa_recolha += alt(recursos.fermentadores)
                            tarefa_recolha += tarefa_fermentar*recursos.fermentadores
                            Cervejaria += tarefa_recolha >= tarefa_fermentar

    for marca, lista_recolhas in atividade["recolha"]["tarefas"].items():
        for marca_2, lista_fermentacao in atividade["fermentar_2"]["tarefas"].items():
            if(marca ==  marca_2):
                for index, tarefa_recolha in enumerate(lista_recolhas):
                        for index_2, tarefa_fermentar in enumerate(lista_fermentacao):
                            if(index == index_2):
                                tarefa_fermentar += alt(recursos.fermentadores)
                                tarefa_fermentar += tarefa_recolha*recursos.fermentadores
                                Cervejaria += tarefa_fermentar >= tarefa_recolha
    
 #------------------------------------------------------------------------------------------------------                               
#------------------------------------------------------------------------------------------------------

def ordenamento_Fermat(Cervejaria, atividade, recursos):
    propagadores_em_uso = 0
    for marca, lista_centrifugacao in atividade["centrifugar"]["tarefas"].items():
        for marca_2, lista_fermentacao in atividade["fermentar_2"]["tarefas"].items():
            if(marca == marca_2):
                for index, tarefa_centrifugar in enumerate(lista_centrifugacao):
                    for index_2, tarefa_fermentar in enumerate(lista_fermentacao):
                        if(index == index_2):
                            if(marca[0] == 'P' and propagadores_em_uso != 2):
                                tarefa_centrifugar += alt(recursos.fermentadores)
                                tarefa_centrifugar += tarefa_fermentar*recursos.fermentadores
                                tarefa_centrifugar += alt(recursos.propagadores["maturacao"])
                                tarefa_centrifugar += alt(recursos.centrifugas)
                                Cervejaria += tarefa_centrifugar >= tarefa_fermentar
                                propagadores_em_uso += 1
                            else:
                                tarefa_centrifugar += alt(recursos.fermentadores)
                                tarefa_centrifugar += tarefa_fermentar*recursos.fermentadores
                                tarefa_centrifugar += alt(recursos.maturadores)
                                tarefa_centrifugar += alt(recursos.centrifugas)
                                Cervejaria += tarefa_centrifugar >= tarefa_fermentar
    
def ordenamento_PosFermat(Cervejaria, atividade, recursos):
    for marca, lista_centrifugacao in atividade["centrifugar"]["tarefas"].items():
        for marca_2, lista_maturacao in atividade["maturar"]["tarefas"].items():
            if(marca ==  marca_2):
                for index, tarefa_centrifugar in enumerate(lista_centrifugacao):
                        for index_2, tarefa_maturar in enumerate(lista_maturacao):
                            if(index == index_2):
                                tarefa_maturar += alt(recursos.maturadores)
                                tarefa_maturar += tarefa_centrifugar*recursos.maturadores
                                Cervejaria += tarefa_maturar >= tarefa_centrifugar
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    
    if(_ChecarBrahmaZero(atividade)):
        for marca, lista_desalcoolizacao in atividade["desalcoolizar"]["tarefas"].items():
            for marca_2, lista_maturacao in atividade["maturar"]["tarefas"].items():
                if(marca ==  marca_2):
                    for index, tarefa_desalcoolizar in enumerate(lista_desalcoolizacao):
                        for index_2, tarefa_maturar in enumerate(lista_maturacao):
                            if(index == index_2):
                                tarefa_desalcoolizar += alt(recursos.maturadores)
                                tarefa_desalcoolizar += tarefa_maturar*recursos.maturadores
                                tarefa_desalcoolizar += recursos.desalcoolizador
                                Cervejaria += tarefa_desalcoolizar >= tarefa_maturar
    

        for marca, lista_decantacao in atividade["decantar"]["tarefas"].items():
            for marca_2, lista_desalcoolizacao in atividade["desalcoolizar"]["tarefas"].items():
                if(marca ==  marca_2):
                    for index, tarefa_desalcoolizar in enumerate(lista_desalcoolizacao):
                        for index_2, tarefa_decantar in enumerate(lista_decantacao):
                            if(index == index_2):
                                tarefa_decantar += alt(recursos.maturadores)
                                Cervejaria += tarefa_decantar >= tarefa_desalcoolizar

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    
def ordenamento_FimProcesso(Cervejaria, atividade, recursos):
    for marca, lista_filtracao in atividade["filtragem"]["tarefas"].items():
        if(marca != "BRHZ"):
            for marca_2, lista_maturacao in atividade["maturar"]["tarefas"].items():
                if(marca == marca_2):
                    for index, tarefa_filtrar in enumerate(lista_filtracao):
                        for index_2, tarefa_maturar in enumerate(lista_maturacao):
                            if(index == index_2):
                                tarefa_filtrar += alt(recursos.maturadores)
                                tarefa_filtrar += tarefa_maturar*recursos.maturadores
                                tarefa_filtrar += alt(recursos.linhas["Maturada"])
                                Cervejaria += tarefa_filtrar >= tarefa_maturar
        else:
            for marca_2, listadecantar in atividade["decantar"]["tarefas"].items():
                if(marca == marca_2):
                    for index, tarefa_filtrar in enumerate(lista_filtracao):
                        for index_2, tarefa_decantar in enumerate(listadecantar):
                            if(index == index_2):
                                tarefa_filtrar += alt(recursos.maturadores)
                                tarefa_filtrar += tarefa_decantar*recursos.maturadores
                                tarefa_filtrar += alt(recursos.linhas["Maturada"])
                                Cervejaria += tarefa_filtrar >= tarefa_decantar
    
#------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def ordenamento_CIP(Cervejaria, atividade, recursos):
    for marca, lista_cip in atividade["CIP_fermentador"]["tarefas"].items():
        for marca_2, lista_centrifugacao in atividade["centrifugar"]["tarefas"].items():
            if(marca == marca_2):
                for index, tarefa_cip in enumerate(lista_cip):
                    for index_2, tarefa_centrifugar in enumerate(lista_centrifugacao):
                        if(index == index_2):
                            tarefa_cip += alt(recursos.fermentadores)
                            tarefa_cip += tarefa_centrifugar*recursos.fermentadores
                            tarefa_cip += alt(recursos.bombas_de_cip["Cip_Frio"])
                            Cervejaria += tarefa_cip >= tarefa_centrifugar
    
    for marca, lista_cip in atividade["CIPc_centrifuga"]["tarefas"].items():
        for marca_2, lista_centrifugacao in atividade["centrifugar"]["tarefas"].items():
            if(marca == marca_2):
                for index, tarefa_cip in enumerate(lista_cip):
                    for index_2, tarefa_centrifugar in enumerate(lista_centrifugacao):
                        if(index == index_2):
                            tarefa_cip += alt(recursos.centrifugas)
                            tarefa_cip += tarefa_centrifugar*recursos.centrifugas
                            tarefa_cip += alt(recursos.bombas_de_cip["Cip_Quente"])
                            Cervejaria += tarefa_cip >= tarefa_centrifugar
    

    for marca, lista_cip in atividade["CIP_maturada"]["tarefas"].items():
        for marca_2, lista_filtracao in atividade["filtragem"]["tarefas"].items():
            if(marca == marca_2):
                for index, tarefa_cip in enumerate(lista_cip):
                    for index_2, tarefa_filtrar in enumerate(lista_filtracao):
                        if(index == index_2):
                            tarefa_cip += alt(recursos.linhas["Maturada"])
                            tarefa_cip += tarefa_filtrar*recursos.linhas["Maturada"]
                            tarefa_cip += recursos.bombas_de_cip["Cip_Quente"][1]
                            Cervejaria += tarefa_cip >= tarefa_filtrar
    

    for marca, lista_cip in atividade["CIP_recolha"]["tarefas"].items():
        for marca_2, lista_recolhas in atividade["recolha"]["tarefas"].items():
            if(marca == marca_2):
                for index, tarefa_cip in enumerate(lista_cip):
                    for index_2, tarefa_recolha in enumerate(lista_recolhas):
                        if(index == index_2):
                            tarefa_cip += alt(recursos.linhas["Recolha"])
                            tarefa_cip += tarefa_recolha*recursos.linhas["Recolha"]
                            tarefa_cip += recursos.bombas_de_cip["Cip_Quente"][0]
                            Cervejaria += tarefa_cip >= tarefa_recolha

    #----------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------
    
def ordenamentoBRHZ_CIP(Cervejaria, atividade, recursos):
    for marca, lista_cip in atividade["CIP_maturador"]["tarefas"].items():
            for marca_2, lista_filtracao in atividade["filtragem"]["tarefas"].items():
                if(marca == marca_2):
                    print(marca, marca_2)
                    for index, tarefa_cip in enumerate(lista_cip):
                        for index_2, tarefa_filtrar in enumerate(lista_filtracao):
                            if(index == index_2):
                                tarefa_cip += alt(recursos.maturadores)
                                tarefa_cip += tarefa_filtrar*recursos.maturadores
                                tarefa_cip += alt(recursos.bombas_de_cip["Cip_Frio"])
                                Cervejaria += tarefa_cip >= tarefa_filtrar
        
    for marca, lista_cip in atividade["CIP_POS_desalcoolizacao"]["tarefas"].items():
        for marca_2, lista_desalcoolizacao in atividade["desalcoolizar"]["tarefas"].items():
            for index, tarefa_cip in enumerate(lista_cip):
                for index_2, tarefa_desalcoolizar in enumerate(lista_desalcoolizacao):
                    if(index == index_2):
                        tarefa_cip += alt(recursos.maturadores)
                        tarefa_cip += tarefa_desalcoolizar*recursos.maturadores
                        tarefa_cip += alt(recursos.bombas_de_cip["Cip_Frio"])
                        Cervejaria += tarefa_cip >= tarefa_desalcoolizar
    
#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------


def restricoes_Alocacao(Cervejaria, recursos):
    for t in range(0, Cervejaria.horizon):
        Cervejaria += recursos.filas["anel_17"][0]["block_anel17"][t] + recursos.filas["anel_17"][1]["block_anel17"][t] + \
        recursos.filas["anel_17"][2]["block_anel17"][t] + recursos.filas["anel_17"][3]["block_anel17"][t] + \
        recursos.filas["anel_17"][4]["block_anel17"][t] + recursos.filas["anel_17"][5]["block_anel17"][t] + \
        recursos.filas["anel_17"][7]["block_anel17"][t] + recursos.filas["anel_17"][8]["block_anel17"][t] + \
        recursos.filas["anel_17"][9]["block_anel17"][t] + recursos.filas["anel_17"][10]["block_anel17"][t] + \
        recursos.filas["anel_17"][11]["block_anel17"][t] + recursos.filas["anel_17"][11]["block_anel17"][t] <= 1

        Cervejaria += recursos.filas["anel_18"][0]["block_anel18"][t] + recursos.filas["anel_17"][1]["block_anel18"][t] + \
        recursos.filas["anel_17"][2]["block_anel18"][t] + recursos.filas["anel_17"][3]["block_anel18"][t] + \
        recursos.filas["anel_17"][4]["block_anel18"][t] + recursos.filas["anel_17"][5]["block_anel18"][t] + \
        recursos.filas["anel_17"][7]["block_anel18"][t] + recursos.filas["anel_17"][8]["block_anel18"][t] + \
        recursos.filas["anel_17"][9]["block_anel18"][t] + recursos.filas["anel_17"][10]["block_anel18"][t] + \
        recursos.filas["anel_17"][11]["block_anel18"][t] <= 1

        Cervejaria += recursos.filas["anel_19"][0]["block_anel19"][t] + recursos.filas["anel_17"][1]["block_anel19"][t] + \
        recursos.filas["anel_17"][2]["block_anel19"][t] + recursos.filas["anel_17"][3]["block_anel19"][t] + \
        recursos.filas["anel_17"][4]["block_anel19"][t] + recursos.filas["anel_17"][5]["block_anel19"][t] + \
        recursos.filas["anel_17"][7]["block_anel19"][t] + recursos.filas["anel_17"][8]["block_anel19"][t] + \
        recursos.filas["anel_17"][9]["block_anel19"][t] + recursos.filas["anel_17"][10]["block_anel19"][t] + \
        recursos.filas["anel_17"][11]["block_anel19"][t]  <= 1

        Cervejaria += recursos.filas["anel_20"][0]["block_anel20"][t] + recursos.filas["anel_17"][1]["block_anel20"][t] + \
        recursos.filas["anel_17"][2]["block_anel20"][t] + recursos.filas["anel_17"][3]["block_anel20"][t] + \
        recursos.filas["anel_17"][4]["block_anel20"][t] + recursos.filas["anel_17"][5]["block_anel20"][t] + \
        recursos.filas["anel_17"][7]["block_anel20"][t] + recursos.filas["anel_17"][8]["block_anel20"][t] + \
        recursos.filas["anel_17"][9]["block_anel20"][t] + recursos.filas["anel_17"][10]["block_anel20"][t] + \
        recursos.filas["anel_17"][11]["block_anel20"][t]  <= 1
    
    '''
        #CIps longos a cada 48h nas centrifugas
            lista = []
            i = 0
            for t in range(0,horizon-2,2):
                if(t == 0):
                    T = cervejaria.Task('CIP_LC' + str(t), length= 1, periods=[2])
                    T += centrifuge_1
                    T += centrifuge_2
                    lista.append(T)
                    i = i + 1
                else:
                    T = cervejaria.Task('CI_PLC' + str(t), length= 1)
                    T += centrifuge_1
                    T += centrifuge_2
                    lista.append(T)
                    cervejaria += lista[i-1] + 1 <= lista[i]
                    i = i + 1
            
            # CIP DOSAGEM -- BREAK
            for v in variaveis_estado.values():
                for item in v:
                    for t in range(1, horizon):
                        cervejaria += brewhouse_1[item][t -
                                                        1] <= (brewhouse_1[item][t] + 1)
                        cervejaria += brewhouse_2[item][t -
                                                        1] <= (brewhouse_2[item][t] + 1)
    '''
    



def gerarRestricoes(Cervejaria, atividade, recursos):
    recursos_Arriamento(Cervejaria, atividade, recursos)
    ordenamento_Fermentacao(Cervejaria, atividade, recursos)
    ordenamento_Fermat(Cervejaria, atividade, recursos)
    ordenamento_PosFermat(Cervejaria, atividade, recursos)
    ordenamento_FimProcesso(Cervejaria,atividade, recursos)
    ordenamento_CIP(Cervejaria, atividade, recursos)
    ordenamentoBRHZ_CIP(Cervejaria,atividade, recursos)
    restricoes_Alocacao(Cervejaria, recursos)
