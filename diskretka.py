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
        res[x] = l
    return res

def hamilton(graph):
    pass

def eiler(graph:dict) -> list[int]:
    

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

    def edges(graph):
        edges = 0
        if isorient(graph):
            for apex in graph.keys():
                edges += degree(graph, apex)[0]
            return edges
        for apex in graph.keys():
            edges += degree(graph, apex)
        return edges/2

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
        return 'No Euler cycle'
    
    vertex_list = []
    edges = euler_edges(graph)
    if edges != 'No Euler cycle':
        for pair in edges:
            vertex_list.append(pair[0])
        return vertex_list
    return 'No Euler cycle'

print(eiler(read_graph('test.csv')))

def double(graph):
    pass

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
