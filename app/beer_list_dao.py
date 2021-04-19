def create():
    return []
    
def isin(L, beer):
    for item in L:
        if item['Beer'] == beer:
            return True
    return False

def add(L, beer, volume):
    L1 = L.copy()
    L1.append({'Beer' : beer,'volume' : str(volume)})    
    return L1

def remove_by_beer(L, beer):
    L = [item for item in L if not item['Beer'] == beer]
    return L

def remove_by_indexes(L, idx):       
    L1 = L.copy()    
    L1 = [i for j, i in enumerate(L1) if j not in idx]    
    return L1
    
def remove_all(L):    
    return create()

def create_sample():
    L = create()
    L = add(L, 'Skol', 5000)
    return L

if __name__ == "__main__":    
    L = create()
    print('Lista criada:', L)

    L = add(L, 'Skol', 10000)
    L = add(L, 'Brahama', 5000)
    L = add(L, 'Stella', 15000)
    print('Adicionadas Skol, Brahama, Stella:', L)

    L = remove_by_beer(L, 'Skol')
    L = remove_by_beer(L, 'Stella')
    print('Removidas Skol e Stella:', L)

    L = add(L, 'Skol', 10000)    
    L = add(L, 'Stella', 15000)
    print('Adicionadas Skol, Stella:', L)

    L = remove_by_indexes(L, [1])
    print('Removida a segunda cerveja da lista:', L)

    L = remove_all(L)
    print('Removidos todos os elementos', L)

    L = create_sample();
    print('Criada lista de exemplo', L)