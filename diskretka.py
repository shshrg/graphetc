'''Комп'ютерний проєкт'''

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

def hamilton(graph):
    pass

def eiler(graph):
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
    pass

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