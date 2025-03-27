from graphviz import Digraph

class RegexperCleanDiagram:
    def __init__(self):
        self.dot = Digraph(graph_attr={'rankdir': 'LR'})
        self.node_id = 0

    def new_node(self, label, shape='box'):
        name = f"n{self.node_id}"
        self.node_id += 1
        self.dot.node(name, label=label, shape=shape)
        return name

    def build_diagram(self):
        # Start node
        start = self.new_node('', shape='circle')
        last = start

        # a* (loop)
        a_node = self.new_node('a')
        self.dot.edge(last, a_node, label='repeat')
        self.dot.edge(a_node, a_node, label='loop')
        last = a_node

        # (b|c) directly connected
        b_node = self.new_node('b')
        c_node = self.new_node('c')
        self.dot.edge(last, b_node)
        self.dot.edge(last, c_node)

        # d* from both b and c (no merge node)
        d_node = self.new_node('d')
        self.dot.edge(b_node, d_node, label='repeat')
        self.dot.edge(c_node, d_node, label='repeat')
        self.dot.edge(d_node, d_node, label='loop')

        # End node
        end = self.new_node('', shape='doublecircle')
        self.dot.edge(d_node, end)

        return self.dot


# Build and render the cleaned diagram
clean_diagram = RegexperCleanDiagram()
clean_graph = clean_diagram.build_diagram()
clean_graph.render('/mnt/data/clean_regexper_diagram', view=True, format='pdf')