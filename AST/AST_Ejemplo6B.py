import ast

code = """
if 1 == 1 and 2 == 2 and 3 == 3:
    test = 1
"""

tree = ast.parse(code)
print(ast.dump(ast.parse(code)))
print(ast.unparse(tree))