'''Комп'ютерний проєкт'''
import copy
import matplotlib.pyplot as plt
import networkx as nx

def visualise(graph, colors=False):
    '''Funtion to visualise graphs. If colors is True return graph coloring'''
    for start in list(graph):
        for end in graph[start]:
            if end not in graph:
                graph[end] = []
    G = nx.DiGraph()
    for key, value in graph_coloring(graph).items():
        if colors:
            G.add_node(key, color=value)
        else:
            G.add_node(key)
    G.add_edges_from([(key, value) for key, values in graph.items() for value in values])
    if colors:
        colors = [node[1]['color'] for node in G.nodes(data=True)]
        nx.draw(G, node_color=colors, with_labels=True, font_color='white')
    else:
        nx.draw(G, with_labels=True, font_color='white')

    plt.show()

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
        res[x] = sorted(l)
    return res

def hamilton(graph:dict):
    path = []
    start = list(graph.keys())[0]
    size = len(list(graph.keys()))
    path.append(start)

    def ishamilton(graph, apex, path:list):
        if len(path) == size and start in graph[apex]:
            return (True, path)
        for neigh in graph[apex]:
            if neigh not in path:
                path.append(neigh)
                if ishamilton(graph, neigh, path)[0]:
                    return (True, path)
                path.remove(neigh)
        return (False, path)
    path = ishamilton(graph, start, path)[1]
    if len(path) == 1:
        return False
    return path

def eiler(graph:dict) -> list[int]:
    def iseuler(graph:dict):
        if connected(graph):
            if isorient(graph):
                for apex in graph.keys():
                    if not degree(graph, apex)[0] == degree(graph, apex)[1]:
                        return False
                return strong_c(graph)
            for apex in graph.keys():
                if not degree(graph, apex) % 2 == 0:
                    return False
            return True
        return False

    def valid(graph:dict, edge_start, edge_fin, orientation):
        if len(graph[edge_start]) == 1:
            return True
        new_g = copy.deepcopy(graph)
        new_g[edge_start].remove(edge_fin)
        if not orientation:
            if edge_fin in new_g.keys() and edge_start in new_g[edge_fin]:
                    new_g[edge_fin].remove(edge_start)
        return connected(new_g)

    def euler_edges(graph):
        orientation = isorient(graph)
        graph = loop_search(graph)
        if iseuler(graph):
            start =list(graph.keys())[0]
            def find_cycle(graph:dict, apex, result:list):
                for neigh in graph[apex]:
                    if valid(graph, apex, neigh, orientation):
                        result.append((apex, neigh))
                        graph[apex].remove(neigh)
                        if neigh in graph.keys() and apex in graph[neigh]:
                            if not orientation:
                                graph[neigh].remove(apex)

                        empty = ''
                        for vertex in graph.keys():
                            if not graph[vertex]:
                                empty = vertex 
                            if orientation:
                                for vertex in graph.keys():
                                    if empty in graph[vertex]:
                                        empty = ''
                                        break
                        if empty != '':
                            del graph[empty]

                        return find_cycle(graph, neigh, result)
                return result
            return find_cycle(graph, start, [])
        return False

    vertex_list = []
    edges = euler_edges(graph)
    if edges != False:
        for pair in edges:
            vertex_list.append(pair[0])
        return vertex_list
    return False


def double(graph: dict) -> bool:
    '''
    Checks whether graph is bipartite
    >>> double({0: [2, 3, 4], 1: [2, 3, 4], 2: [0, 1], 3: [0, 1], 4: [0, 1]})
    True
    >>> double({0: [2, 3, 4], 1: [2, 3, 4]})
    True
    >>> double({0: [2, 3, 4], 1: [2, 3, 4], 2: [0, 1], 3: [0, 1], 4: [0, 1, 2]})
    False
    >>> double({1: [7], 2: [4], 3: [2], 4: [1], 5: [5], 6: [5]})
    True
    '''
    empty_nodes = []
    for start in graph:
        for end in graph[start]:
            if end not in graph:
                empty_nodes += [end]
    for empty_node in empty_nodes:
        graph[empty_node] = []
    independent_array = []
    for start in graph:
        if not independent_array:
            independent_array += [[start]]
        else:
            for j, independent_nodes in enumerate(independent_array):
                if start not in independent_nodes:
                    for node in independent_nodes:
                        if node in graph[start] or start in graph[node]:
                            is_last_node = j == len(independent_array) - 1
                            if is_last_node:
                                independent_array += [[start]]
                                if len(independent_array) > 2:
                                    return False
                            break
                    else:
                        independent_nodes += [start]
                        break
                else:
                    break
    return True

def double2(graph: dict) -> bool:
    '''
    Checks whether graph is bipartite. Second implementation using simple cycles.
    >>> double2({0: [2, 3, 4], 1: [2, 3, 4], 2: [0, 1], 3: [0, 1], 4: [0, 1]})
    True
    >>> double2({0: [2, 3, 4], 1: [2, 3, 4]})
    True
    >>> double2({0: [2, 3, 4], 1: [2, 3, 4], 2: [0, 1], 3: [0, 1], 4: [0, 1, 2]})
    False
    >>> double2({1: [7], 2: [4], 3: [2], 4: [1], 5: [5], 6: [5]})
    True
    '''
    all_simple_cycles = find_cycle_(graph)
    cycles_len_is_even = all(not len(cycle)&1 for cycle in all_simple_cycles)
    return cycles_len_is_even


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
            print('Given graphs have different degree of vertex')
            return False
        if dct_2[key] != value:
            print('Given graphs have different degree of vertex')
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
            print('Given grapgs have different degrees of vertex and its neighbours')
            return False
        if dct_2[key] != values:
            print('Given grapgs have different degrees of vertex and its neighbours')
            return False

    # Checks graphs by lengths of their simple cycles
    res_1 = find_cycle_(graph1, True)
    res_2 = find_cycle_(graph2, True)

    dct_1_1 = {}
    for i in res_1:
        tup = tuple(sorted(list(i[1].items())))
        # print(f'i: {i}, i[1]_tup: {tuple(i[1].items())}, tupr: {tup}')
        if (len(i[0]),tup) not in dct_1_1:
            dct_1_1[(len(i[0]),tup)] = 1
        else:
            dct_1_1[(len(i[0]),tup)] += 1

    dct_2_1 = {}
    for i in res_2:
        tup = tuple(sorted(list(i[1].items())))
        # print(f'i: {i}, i[1]_tup: {tuple(i[1].items())}')
        if (len(i[0]),tup) not in dct_2_1:
            dct_2_1[(len(i[0]),tup)] = 1
        else:
            dct_2_1[(len(i[0]),tup)] += 1

    # print(dct_1_1)
    # print(dct_2_1)

    for key, value in dct_1_1.items():
        if key not in dct_2_1:
            print('Given graphs have different length of simple cycles or different degrees \
of vertexes in cycles')
            return False
        if dct_2_1[key] != value:
            print('Given graphs have different length of simple cycles or different degrees \
of vertexes in cycles')
            return False


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
####### HELPING FUNCTIONS
def loop_search(graph:dict):
    for src, dst in graph.items():
        loop = 0
        for item in dst:
            if src == item:
                loop = item
        if loop:
            dst = dst.remove(loop)
    return graph

def isorient(graph:dict):
    for apex, neighs in graph.items():
        for point in neighs:
            if point in graph.keys():
                if apex not in graph[point]:
                    return True
    return False

def connected(graph:dict):
    for apex_src in graph.keys():
        for apex_dst in graph.keys():
            if apex_src != apex_dst:
                n = find_path(graph, apex_src, apex_dst, [])
                m = find_path(graph, apex_dst, apex_src, [])
                if not n and not m:
                    return False
    return True

def degree(graph:dict, apex):
    if isorient(graph):
        degree_out = len(graph[apex])
        degree_in = 0
        for point in graph.keys():
            if apex in graph[point]:
                degree_in +=1
        return (degree_in, degree_out)
    return len(graph[apex])

def find_path(graph:dict, src, dst, res:list):
    res.append(src)
    if src in graph.keys():
        if dst in graph[src]:
            return True
        for apex in graph[src]:
            if apex not in res:
                if find_path(graph, apex, dst, res):
                    return True
    return False

def strong_c(graph:dict):
    for apex_src in graph.keys():
        for apex_dst in graph.keys():
            n = find_path(graph, apex_src, apex_dst, [])
            if not n:
                return n
    return True
def find_cycle_(graph, degree_ = False):
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
        if degree_:
            srt_res = [sorted(i[0]) for i in res_]
        else:
            srt_res = [sorted(i) for i in res_]
        for i in output:
            if sorted(i) not in srt_res:
                if degree_:
                    dct_ = {}
                    for j in sorted(i):
                        if len(graph[j]) not in dct_:
                            dct_[len(graph[j])] = 1
                        else:
                            dct_[len(graph[j])] += 1
                    res_.append((i, dct_))
                else:
                    res_.append(i)
    return res_
