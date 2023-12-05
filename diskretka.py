'''Комп'ютерний проєкт'''

# якщо треба словник та Dict=True, якщо неорієнтований граф то Oriented=False
# якщо граф орієнтований, то у списку будуть тапли, якщо ні то множини
def read_graph(file, Dict=False, Oriented=True):
    '''
    Reads a csv and returns a graph in the form of a list or dictionary.
    '''
    with open(file, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for i,l in enumerate(lines):
            lines[i] = [int(i) for i in l.rstrip().split(',')]
    list_graph = [(lines[0][i], lines[1][i]) for i in range(len(lines[0]))]
    if not Dict:
        list_graph = [(lines[0][i], lines[1][i]) for i in range(len(lines[0]))]
        if not Oriented:
            for i,x in enumerate(list_graph):
                list_graph[i] = set(x)
        return list_graph
    else:
        if Oriented:
            res = {i[0]:{k[1] for k in list_graph if k[0]==i[0]} for i in list_graph}
        else:
            res = {}
            for y in set(lines[0] + lines[1]):
                points = set()
                for x in list_graph:
                    if y == x[0]:
                        points.add(x[1])
                    elif y == x[1]:
                        points.add(x[0])
                res[y] = points
        return res
