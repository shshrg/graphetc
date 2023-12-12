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

def eiler(graph):
    pass

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