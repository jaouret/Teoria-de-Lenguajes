from PythonLLVM import ast

tree = ast.parse('''
fruits = ['grapes', 'mango']
name = 'peter'

for fruit in fruits:
    print('{} likes {}'.format(name, fruit))
''')

print(ast.dump(tree))