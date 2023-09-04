from PythonLLVM import ast


class MyVisitor(ast.NodeVisitor):
    def visit_Str(self, node):
        print('String Node: "' + node.s + '"')

class MyTransformer(ast.NodeTransformer):
    def visit_Str(self, node):
        return ast.Str('str: ' + node.s)

parsed = ast.parse("#Commentario")
MyTransformer().visit(parsed)
MyVisitor().visit(parsed)