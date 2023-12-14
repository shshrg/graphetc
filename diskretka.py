'''Комп'ютерний проєкт'''
from itertools import permutations

def read_graph(file):
    '''
    Reads a csv and returns a graph in the form of a list or dictionary.
    '''
    with open(file, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for i,l in enumerate(lines):
            lines[i] = [int(i) for i in l.rstrip().split(',')]
    list_graph = [(lines[0][i], lines[1][i]) for i in range(len(lines[0]))]
    all_points = set([x[0] for x in list_graph])
    res = {}
    for x in all_points:
        l = []
        for y in list_graph:
            if y[0] == x:
                l.append(y[1])
        res[x] = l
    return res

def hamilton(graph):
    pass

def eiler(graph):
    pass

def double(graph):
    pass

def find_cycle_(graph):
    '''
    Function, which returns all the cycles from given graph
    '''
    def recur_find_cycle(graph, key, lst_of_keys = None, res = None, deep = 0):
        if lst_of_keys is None:
            lst_of_keys = [key]
        if res is None:
            res = []
        if key in graph:
            for i in graph[key]:
                if i not in lst_of_keys:
                    lst_of_keys.append(i)
                    recur_find_cycle(graph,i,lst_of_keys,res,deep+1)
                    if lst_of_keys[-1] in graph and lst_of_keys[0] in graph[lst_of_keys[-1]] and \
deep != 0 and sorted(lst_of_keys) not in [sorted(i) for i in res]:
                        res.append(lst_of_keys.copy())
                    lst_of_keys.remove(i)
        return res

    res_ = []
    for key in graph.keys():
        output = recur_find_cycle(graph, key)
        srt_res = [sorted(i) for i in res_]
        for i in output:
            if sorted(i) not in srt_res:
                res_.append(i)
    return res_

def isomorph(graph1, graph2):
    '''
    This function checks if given pair of graphs is isomorphic
    '''
    # Checks graphs by amount of vertexes
    if len(graph1.keys()) != len(graph2.keys()):
        print('Given graphs have different number of vertexes')
        return False

    # Checks graphs by amount of edges
    lst_1 = []
    for key, values in graph1.items():
        lst_1.extend(values)

    lst_2 = []
    for key, values in graph2.items():
        lst_2.extend(values)

    if len(lst_1) != len(lst_2):
        print('Given graphs have different amount of edges')
        return False

    # Checks graphs by degree of vertexes
    dct_1 = {}
    for key, values in graph1.items():
        if len(values) in dct_1:
            dct_1[len(values)] += 1
        else:
            dct_1[len(values)] = 1

    dct_2 = {}
    for key, values in graph2.items():
        if len(values) in dct_2:
            dct_2[len(values)] += 1
        else:
            dct_2[len(values)] = 1

    for key, value in dct_1.items():
        if key not in dct_2:
            return False
        if dct_2[key] != value:
            return False

    # Checks graphs by degree of the vertex and degree of its neighbours
    dct_1 = {}
    for key, values in graph1.items():
        res_lst = []
        for value in values:
            res_lst.append(len(graph1[value]))
        tup = tuple(sorted(res_lst))
        if (len(values), tup) not in dct_1:
            dct_1[len(values), tup] = 1
        else:
            dct_1[len(values), tup] += 1

    dct_2 = {}
    for key, values in graph2.items():
        res_lst = []
        for value in values:
            res_lst.append(len(graph2[value]))
        tup = tuple(sorted(res_lst))
        if (len(values), tup) not in dct_2:
            dct_2[len(values), tup] = 1
        else:
            dct_2[len(values), tup] += 1

    for key,values in dct_1.items():
        if key not in dct_2:
            return False
        if dct_2[key] != values:
            return False

    # Checks graphs by lengths of their simple cycles
    def recursive_find_cycle(graph, key, lst_of_keys = None, res = None, deep = 0):
        if lst_of_keys is None:
            lst_of_keys = [key]
        if res is None:
            res = []
        for i in graph[key]:
            if i not in lst_of_keys:
                lst_of_keys.append(i)
                recursive_find_cycle(graph,i,lst_of_keys,res,deep+1)
                if lst_of_keys[0] in graph[lst_of_keys[-1]] and deep != 0:
                    res.append(lst_of_keys.copy())
                lst_of_keys.remove(i)
        return res

    dct_1 = {}
    for i in find_cycle_(graph1):
        if len(i) not in dct_1:
            dct_1[len(i)] = 1
        else:
            dct_1[len(i)] += 1

    dct_2 = {}
    for i in find_cycle_(graph2):
        if len(i) not in dct_2:
            dct_2[len(i)] = 1
        else:
            dct_2[len(i)] += 1

    for key, value in dct_1.items():
        if key not in dct_2:
            return False
        if dct_2[key] != value:
            return False


    graph1_ = []
    for key,values in graph1.items():
        graph1_.append((key, sorted(values)))
    graph1_ = dict(graph1_)

    graph2_ = []
    for key,values in graph2.items():
        graph2_.append((key, sorted(values)))
    graph2_ = dict(graph2_)

    mat_1 = []
    for val in graph1_.values():
        lst_app = []
        for ind_x in graph1_:
            if ind_x not in val:
                lst_app.append(0)
            else:
                lst_app.append(1)
        mat_1.append(lst_app)

    mat_2 = []
    for val in graph1_.values():
        lst_app = []
        for ind_x in graph1_:
            if ind_x not in val:
                lst_app.append(0)
            else:
                lst_app.append(1)
        mat_2.append(lst_app)

    if mat_1 == mat_2:
        return True

    for i in list(permutations(mat_1, len(graph1_.keys()))):
        if i == mat_2:
            return True

def graph_coloring(graph):
    """Розфарбовування графа жадібним алгоритмом
    >>> graph_coloring({'A': ['B', 'C'], 'B': ['A', 'C'], 'C': ['B', 'A']})
    {'A': 'Red', 'B': 'Green', 'C': 'Blue'}
    >>> graph_coloring({'A': ['B', 'C', 'D'], 'B': ['A', 'C'], 'C': ['A', 'B', 'D'], 'D': ['A', 'C']})
    {'A': 'Red', 'B': 'Green', 'C': 'Blue', 'D': 'Green'}
    >>> graph_coloring({'A': ['B', 'C'], 'B': ['A', 'C'], 'C': ['A', 'B'], 'D': ['B', 'E'], 'E': ['D']})
    {'A': 'Red', 'B': 'Green', 'C': 'Blue', 'D': 'Red', 'E': 'Green'}
    >>> graph_coloring({'A': ['B', 'C', 'D'], 'B': ['A', 'C', 'D'], 'C': ['A', 'B', 'D'], 'D': ['A', 'B', 'C']})
    'Неможливо зафарбувати'
    >>> graph_coloring({'A': ['B', 'C', 'D', 'E'], 'B': ['A', 'C', 'D', 'E'], 'C': ['A', 'B', 'D', 'E'], 'D': ['A', 'B', 'C', 'E'], 'E': ['A', 'B', 'C', 'D']})
    'Неможливо зафарбувати'
    """
    def color(lst): # функція для визначення кольору
        colors = set(lst) # всі кольори, які вже використані
        color_lst = ['Red', "Green", "Blue"] # можливі кольори
        for i in range(3): # перевіряємо, якого кольору немає в сусідів
            if color_lst[i] not in colors: # якщо такого кольору немає, то повертаємо його
                return color_lst[i]
        return None
    color_dict = dict() # словник, де ключ - вершина, а значення - колір
    for node in graph: # проходимо по всіх вершинах
        visited_color = [color_dict[elem] for elem in graph[node] if elem in color_dict]
# перевіряємо, які кольори вже використані
        color_dict[node] = color(visited_color) # зафарбовуємо вершину
        if color_dict[node] is None: # якщо не вдалося зафарбувати, то повертаємо None
            return "Неможливо зафарбувати"
    return color_dict
