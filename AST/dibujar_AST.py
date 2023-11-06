from graphviz import Digraph

def dibujar_ast(node, dot=None):
    if dot is None:
        dot = Digraph(comment='AST')

    if isinstance(node, list):
        operador = node[0]
        dot.node(operador, operador)
        for hijo in node[1:]:
            if isinstance(hijo, list):
                hijo_operador = hijo[0]
                dot.node(hijo_operador, hijo_operador)
                dot.edge(operador, hijo_operador)
                dibujar_ast(hijo, dot)
            else:
                dot.node(hijo, hijo)
                dot.edge(operador, hijo)

    return dot


def leer_ast_de_archivo(archivo):
    with open(archivo, 'r') as file:
        ast_str = file.read()
        return eval(ast_str)

# Nombre del archivo que contiene el AST
archivo = 'ast4.txt'

# Lee el AST desde el archivo
ast = leer_ast_de_archivo(archivo)

# Dibuja y guarda el AST
dot = dibujar_ast(ast)
dot.render('ast', view=True)
