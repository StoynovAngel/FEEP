from graphviz import Digraph

class RegexperStyleDiagram:
    def __init__(self):
        self.dot = Digraph(graph_attr={'rankdir': 'LR'})
        self.node_id = 0

    def new_node(self, label='', shape='box'):
        name = f"n{self.node_id}"
        self.node_id += 1
        self.dot.node(name, label=label, shape=shape)
        return name

    def build(self, regex: str):
        start = self.new_node('', shape='circle')
        end = self.new_node('', shape='doublecircle')
        self._process_expr(regex, start, end, self.dot)
        return self.dot

    def _process_expr(self, expr: str, entry: str, exit: str, g: Digraph):
        parts = []
        depth = 0
        current = ''
        for c in expr:
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
            if c == '|' and depth == 0:
                parts.append(current)
                current = ''
            else:
                current += c
        parts.append(current)

        if len(parts) > 1:
            for part in parts:
                alt_entry = self.new_node('', shape='point')
                alt_exit = self.new_node('', shape='point')
                g.edge(entry, alt_entry)
                self._process_expr(part, alt_entry, alt_exit, g)
                g.edge(alt_exit, exit)
        else:
            i = 0
            prev = entry
            while i < len(expr):
                c = expr[i]
                if c == '(':
                    j = i + 1
                    depth = 1
                    while j < len(expr):
                        if expr[j] == '(':
                            depth += 1
                        elif expr[j] == ')':
                            depth -= 1
                        if depth == 0: break
                        j += 1

                    group_content = expr[i + 1:j]
                    group_entry = self.new_node('', shape='point')
                    group_exit = self.new_node('', shape='point')
                    g.edge(prev, group_entry)

                    self._process_expr(group_content, group_entry, group_exit, g)

                    if j + 1 < len(expr) and expr[j + 1] in '*+':
                        g.edge(group_exit, group_entry, label=expr[j + 1])
                        i = j + 1
                    else:
                        i = j

                    prev = group_exit
                elif c.isalpha():
                    char_node = self.new_node(c)
                    g.edge(prev, char_node)
                    prev = char_node
                    if i+1 < len(expr) and expr[i+1] in '*+':
                        loop_type = expr[i+1]
                        g.edge(char_node, char_node, label=loop_type)
                        i += 1
                i += 1
            g.edge(prev, exit)


regex_input = input("Enter a simple regular expression (supports a-z, *, +, |, () ): ")
diagram = RegexperStyleDiagram()
graph = diagram.build(regex_input)
output_path = '/mnt/data/user_regexper_diagram'
graph.render(output_path, view=True, format='pdf')
print(f"Diagram saved to: {output_path}.pdf")