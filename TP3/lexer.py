from rply import LexerGenerator

# Crear un generador de lexer
lg = LexerGenerator()

# Definir las reglas léxicas (tokens)
lg.add('NUMBER', r'\d+')
lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')
lg.add('MULTIPLY', r'\*')
lg.add('DIVIDE', r'/')
lg.add('LPAREN', r'\(')
lg.add('RPAREN', r'\)')
lg.ignore(r'\s+')

# Construir el lexer
lexer = lg.build()

# Ejemplo de código fuente
code = "(2 + 3) * 4"

# Probar el lexer
for token in lexer.lex(code):
    print(token)
