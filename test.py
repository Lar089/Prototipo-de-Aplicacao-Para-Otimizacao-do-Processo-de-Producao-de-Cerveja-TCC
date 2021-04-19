import pandas as pd
import plotly.figure_factory as ff
import plotly.io as pio


def load_results( foldername ):
    import pickle
    with open('temp/'+foldername+'/df_solution.pickle', 'rb') as handle:
        df_solution = pickle.load(handle)
    with open('temp/'+foldername+'/stats.pickle', 'rb') as handle:
        stats = pickle.load(handle)
    return df_solution, stats

df_results, stats = load_results('ba9fcf9a-6571-4280-b029-ba04170971b5')
df_results.Inicio = df_results.Inicio.astype(int)
df_results.Fim = df_results.Fim.astype(int)
df_results.Tarefa = df_results.Tarefa.str.replace("SKL",'_LOTE_')
df_results['Lote'] = "LOTE_" + df_results.Tarefa.str.extract(".*_(?P<Lote>\d)").values

#print(df_results)

df_results.rename(columns = {
    'Tarefa': 'Task1', 
    'Recurso': 'Task',
    'Inicio': 'Start',
    'Fim': 'Finish',
    'Lote' : 'Lote'
}, inplace=True)

xlabels = df_results[['Task','Start','Finish']].sort_values(['Start','Finish']).groupby('Task').first().reset_index().sort_values('Start')['Task'].values

pio.templates.default = "simple_white"

fig = ff.create_gantt(df_results, show_hover_fill = True, group_tasks=True, showgrid_x=True, index_col='Lote', show_colorbar=True)
fig['layout']['xaxis'].update({'type': None, 'title' : "Tempo (em unidades de tempo de produção, utc)"}) 
fig['layout']['yaxis'].update({'title' : "Recursos", "categoryorder" : "array", "categoryarray" : xlabels})

#fig.show()


#print(df_results)

#df_results.rename(columns = {
#    'Tarefa': 'Resource', 
#    'Recurso': 'Task',
#    'Inicio': 'Start',
#    'Fim': 'Finish'
#}, inplace=True)

#df_test = df_results['Task']
#print(df_test)
#print(len(df_test))


def split_t(df_test):
    df_r = pd.DataFrame({"Task": []})
    for x in df_test:
        new_text = x.split("_")
        new_text = ' '.join(new_text)
        df_r1 = pd.DataFrame({"Task": [new_text]})
        df_r = df_r.append(df_r1)
    #print(df_r)
    return df_r
    
#df_test = split_t(df_test)
#fig.show()