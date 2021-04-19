#from pyschedule import Scenario, solvers, plotters, alt
import pyschedule
import json

#from app.otimizacao.Recursos import Fabrica
#from app.otimizacao.Tarefas import gerarTodasAtividades
#from app.otimizacao.Restricoes import gerarRestricoes

import matplotlib.pyplot as plt
import pandas as pd

from Recursos import Fabrica
from Tarefas import gerarTodasAtividades
from Restricoes import gerarRestricoes

def _LerJson_Atividades():
    with open("./app/data/atividades.json", "r") as read_file:
        atividades = json.load(read_file)
    return atividades

def _tratarVolume(malha_producao):
    capacidade_tanque = 5000
    for produzir in malha_producao:  # arredondar o valor do uso dos tanques ou distribuir os valores
        produzir["tanques"] = int(produzir["volume"] / capacidade_tanque)


import operator
def plot_get_solution(scenario,img_filename=None,resource_height=1.0,show_task_labels=True,
         color_prec_groups=False,hide_tasks=[],hide_resources=[],task_colors=dict(),fig_size=(15,5),
		 vertical_text=False) :
	"""
	Plot the given solved scenario using matplotlib
	Args:
		scenario:    scenario to plot
		msg:         0 means no feedback (default) during computation, 1 means feedback
	"""
	try :
		import matplotlib
		if img_filename is not None:
			matplotlib.use('Agg')
		import matplotlib.patches as patches, matplotlib.pyplot as plt
	except :
		raise Exception('ERROR: matplotlib is not installed')
	import random

	S = scenario
	# trivial connected components implementation to avoid
	# having to import other packages just for that
	def get_connected_components(edges) :
		comps = dict()
		for v,u in edges :
			if v not in comps and u not in comps :
				comps[v] = v
				comps[u] = v
			elif v in comps and u not in comps :
				comps[u] = comps[v]
			elif v not in comps and u in comps :
				comps[v] = comps[u]
			elif v in comps and u in comps and comps[v] != comps[u] :
				old_comp = comps[u]
				for w in comps :
					if comps[w] == old_comp :
						comps[w] = comps[v]
		# replace component identifiers by integers startting with 0
		values = list(comps.values())
		comps = { T : values.index(comps[T]) for T in comps }
		return comps

	tasks = [ T for T in S.tasks() if T not in hide_tasks ]

	# get connected components dict for coloring
	# each task is mapping to an integer number which corresponds
	# to its connected component
	edges = [ (T,T) for T in tasks ]
	if color_prec_groups :
		edges += [ (T,T_) for P in set(S.precs_lax()) | set(S.precs_tight()) \
	                   for T in P.tasks() for T_ in P.tasks() \
                           if T in tasks and T_ in tasks ]
	comps = get_connected_components(edges)

	# color map
	colors = ['#7EA7D8','#A1D372','#EB4845','#7BCDC8','#FFF79A'] #pastel colors
	#colors = ['red','green','blue','yellow','orange','black','purple'] #basic colors
	colors += [ [ random.random() for i in range(3) ] for x in range(len(S.tasks())) ] #random colors
	color_map = { T : colors[comps[T]] for T in comps }
	# replace colors with fixed task colors

	for T in task_colors :
		color_map[T] = task_colors[T]
	hide_tasks_str = [ T for T in hide_tasks ]
	for T in scenario.tasks():
		if hasattr(T,'plot_color'):
			if T['plot_color'] is not None:
				color_map[T] = T['plot_color']
			else:
				hide_tasks_str.append(T)

	solution = S.solution()	
	solution = [ [str(T),str(R),str(x),str(y)] for (T,R,x,y) in solution if T not in hide_tasks_str ] #tasks of zero length are not plotted	        
	df_solution = pd.DataFrame(solution, columns=['Tarefa', 'Recurso', 'Inicio','Fim'])	
	return df_solution


def otimizar(malha_producao, horizon):
    print('Iniciando a otimização')
    print(malha_producao)
    print(horizon)
    print('Criando do objeto de otimização')  
    Cervejaria = pyschedule.Scenario("Cervejaria", horizon=horizon)
    print('Carregando atividades de produção')
    atividade = _LerJson_Atividades()    
    recursos = Fabrica()
    recursos.gerarRecursos(Cervejaria)      
    print('Gerando as atividades (tasks)')
    gerarTodasAtividades(Cervejaria, atividade, malha_producao)    
    print('Gerandos as restrições (constraints)')
    gerarRestricoes(Cervejaria, atividade, recursos)
    print('Definindo o objetivo de otimização')
    Cervejaria.use_flowtime_objective()
    print('Executando a otimização')    
    pyschedule.solvers.mip.solve(Cervejaria, msg=1, kind='CBC', ratio_gap=.0)
    print('Otimização concluída')    
    print('Salvando a otimização, caso queira ser explorada no script exploring_last_optimization')
    import pickle
    with open('last_optimization.pickle', 'wb') as handle:
        pickle.dump(Cervejaria, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('Processo de otimização finalizado')
    print('Extraindo as tarefas e recursos da solução')
    df_solution = plot_get_solution(Cervejaria,  fig_size=(30, 10))            
    print('Obtendo estatísticas da solução')
    stats = {
        'makespan' : 0
    }
    print('Retornando resposta para o front end')
    return df_solution, stats
    

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Beer House Optimization Backend!")
    
    parser.add_argument("-data", nargs="?", help="Foldername", dest='foldername')
    parser.add_argument("-horizon", nargs="?", help="Horizon", dest='horizon')
    args = parser.parse_args()
    
    foldername = args.foldername
    horizon = args.horizon

    import pickle
    with open('temp/'+foldername+'/dict_to_optimize.pickle', 'rb') as handle:
        print('Lendo o arquivo dict_to_optimize.pickle')
        dict_to_optimize = pickle.load(handle)
        df_solution, stats = otimizar(dict_to_optimize, int(horizon) )
                
        # Se retornou alguma solução		
        if len(df_solution) > 0:
            print('Salvando a solução em arquivo')
			# Este arquivo é rápido de salvar e carregar mas é binário
			# Se quiserem criar um CSV podem ficar a vontade
            with open('temp/'+foldername+'/df_solution.pickle', 'wb') as handle:
                pickle.dump(df_solution, handle, protocol=pickle.HIGHEST_PROTOCOL)  
            with open('temp/'+foldername+'/stats.pickle', 'wb') as handle:
                pickle.dump(stats, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            print('Não foi encontrada nenhuma solução', len(df_solution))
			

if __name__ == '__main__':
    main()
	
