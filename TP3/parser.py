from rply import ParserGenerator

# Definir las reglas de gramática para el parser
pg = ParserGenerator(
    ['NUMBER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'LPAREN', 'RPAREN'],
)

# Nodo de número
@pg.production('expression : NUMBER')
def number(p):
    return int(p[0].getstr())

# Nodo de suma
@pg.production('expression : expression PLUS expression')
def expression_plus(p):
    return ('+', p[0], p[2])

# Nodo de multiplicación
@pg.production('expression : expression MULTIPLY expression')
def expression_multiply(p):
    return ('*', p[0], p[2])

# Uso de paréntesis
@pg.production('expression : LPAREN expression RPAREN')
def expression_parens(p):
    return p[1]

# Construir el parser
parser = pg.build()

# Probar el parser
ast = parser.parse(lexer.lex(code))
print("AST generado:", ast)
