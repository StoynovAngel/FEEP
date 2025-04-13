from graphviz import Digraph
import re

class RegexperStyleDiagram:
    REGEX_PATTERN = r'^[a-zA-Z()*+|]+$'

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

    def process_alternatives(self, parts: list[str], entry: str, exit: str, g: Digraph):
        for part in parts:
            branch_start = self.new_node('', shape='point')
            branch_end = self.new_node('', shape='point')
            g.edge(entry, branch_start)
            self._process_expr(part, branch_start, branch_end, g)
            g.edge(branch_end, exit)

    def _process_expr(self, expr: str, entry: str, exit: str, g: Digraph):
        parts = logical_or(expr)

        if len(parts) > 1:
            self.process_alternatives(parts, entry, exit, g)
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
                        if depth == 0:
                            break
                        j += 1

                    group_content = expr[i + 1:j]
                    group_entry = self.new_node('', shape='point')
                    group_exit = self.new_node('', shape='point')
                    g.edge(prev, group_entry)
                    self._process_expr(group_content, group_entry, group_exit, g)

                    if j + 1 < len(expr) and expr[j + 1] in '*+':
                        apply_quantifier(g, group_exit, group_entry, expr[j + 1], is_group=True)
                        i = j + 1
                    else:
                        i = j

                    prev = group_exit

                elif c.isalpha():
                    char_node = self.new_node(c)
                    g.edge(prev, char_node)

                    if i + 1 < len(expr) and expr[i + 1] in '*+':
                        apply_quantifier(g, char_node, prev, expr[i + 1], is_group=False)
                        i += 1

                    prev = char_node
                i += 1

            g.edge(prev, exit)

def logical_or(expr: str) -> list[str]:
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
    return parts

def apply_quantifier(g: Digraph, current_node: str, prev_node: str, quantifier: str, is_group: bool):
    if quantifier in ('*', '+'):
        if is_group:
            g.edge(current_node, prev_node, label=quantifier, constraint='false')
        else:
            g.edge(current_node, current_node, label=quantifier, constraint='false')

def user_input():
    regex_input = input("Enter a simple regular expression (supports a-z, *, +, |, () ): ")
    if not re.match(RegexperStyleDiagram.REGEX_PATTERN, regex_input):
        print("Error: Invalid characters detected!")
        return user_input()

    try:
        diagram = RegexperStyleDiagram()
        return diagram.build(regex_input)
    except Exception as e:
        print("Error during processing:", e)
        return user_input()

def create_pdf(graph):
    output_path = '/mnt/data/user_regexper_diagram'
    graph.render(output_path, view=True, format='pdf')
    print(f"Diagram saved to: {output_path}.pdf")


if __name__ == "__main__":
    graph = user_input()
    create_pdf(graph)