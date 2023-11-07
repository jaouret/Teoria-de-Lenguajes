from graphviz import Digraph

import graphviz


def create_graph(tree):
    dot = graphviz.Digraph(comment='AST Tree')
    _create_graph(tree, dot)
    return dot


def _create_graph(tree, dot, parent=None):
    if isinstance(tree, list):
        operator = tree[0]
        node_label = str(operator)

        if parent is not None:
            dot.node(node_label)
            dot.edge(parent, node_label)

        for sub_tree in tree[1:]:
            _create_graph(sub_tree, dot, node_label)
    else:
        node_label = str(tree)
        if parent is not None:
            dot.node(node_label)
            dot.edge(parent, node_label)


# Árbol de ejemplo
tree = ["if",
        [">", "x", 0],
            ["=", "y", 1],
        ["else",
            [["=", "y", 0]]
         ]
        ]

dot = create_graph(tree)
dot.render('ast_tree', view=True)
