# PLY consta de dos módulos separados; lex.py y yacc.py, los cuales se encuentran en un paquete de Python llamado ply.
# El módulo lex.py se utiliza para dividir el texto de entrada en una colección de tokens especificados por una colección de reglas
# de expresión regular. yacc.py se utiliza para reconocer la sintaxis del lenguaje que se ha especificado en forma de gramática libre de contexto.

# Las dos herramientas están diseñadas para trabajar juntas. Específicamente, lex.py proporciona una interfaz para producir tokens. yacc.py
# usa estos tokens de recuperación e invoca reglas gramaticales. La salida de yacc.py suele ser un árbol de sintaxis abstracta (AST).
# Sin embargo, esto depende totalmente del usuario. Si lo desea, yacc.py también se puede utilizar para implementar compiladores
# simples de una sola pasada.

# La principal diferencia entre yacc.py y Unix yacc es que yacc.py no implica un proceso de generación de código separado.
# En cambio, PLY se basa en la reflexión (introspección) para construir sus léxers y analizadores.
# A diferencia de los tradicionales lex / yacc que requieren un archivo de entrada especial que se convierte en un archivo fuente separado,
# las especificaciones dadas a PLY son programas válidos de Python.
# Esto significa que no hay archivos fuente adicionales ni hay un paso especial de construcción del compilador (por ejemplo,
# ejecutar yacc para generar código Python para el compilador).

# lex.py se usa para tokenizar una cadena de entrada.
# Por ejemplo, suponga que está escribiendo un lenguaje de programación y un usuario proporcionó la siguiente cadena de entrada:

# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

# Todos los lexers deben proporcionar una lista de tokens que defina todos los posibles nombres de token que puede producir el lexer.
# Esta lista siempre es necesaria y se utiliza para realizar una variedad de comprobaciones de validación.
# La lista de tokens también es utilizada por el módulo yacc.py para identificar terminales.

# List of token names.   This is always required
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
)

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

#Especificación de tokens

# Cada token se especifica escribiendo una regla de expresión regular compatible con el módulo re de Python.
# Cada una de estas reglas se define mediante declaraciones con un prefijo especial t_ para indicar que define un token.
# Para tokens simples, la expresión regular se puede especificar como cadenas como esta
# (nota: se usan cadenas sin procesar de Python ya que son la forma más conveniente de escribir cadenas de expresiones regulares):
# t_PLUS = r'\+'

# En este caso, el nombre que sigue a t_ debe coincidir exactamente con uno de los nombres proporcionados en los tokens.
# Si es necesario realizar algún tipo de acción, se puede especificar una regla de token como función.
# Por ejemplo, esta regla coincide con números y convierte la cadena en un entero de Python:

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Cuando se usa una función, la regla de expresión regular se especifica en la cadena de documentación de la función.
# La función siempre toma un solo argumento que es una instancia de LexToken.
# Este objeto tiene atributos de tipo que es el tipo de token (como una cadena), valor que es el lexema (el texto real coincidente),
# lineno que es el número de línea actual y lexpos que es la posición del token con respecto al principio del texto de entrada.
# De forma predeterminada, el tipo se establece en el nombre que sigue al prefijo t_.
# La función de acción puede modificar el contenido del objeto LexToken según corresponda.
# Sin embargo, cuando se hace, se debe devolver el token resultante.
# Si la función de acción no devuelve ningún valor, el token se descarta y se lee el siguiente.

# Internamente, lex.py usa el módulo re para hacer su coincidencia de patrones.
# Los patrones se compilan utilizando el indicador re.VERBOSE que se puede utilizar para facilitar la legibilidad.
# Sin embargo, tenga en cuenta que los espacios en blanco sin escape se ignoran y los comentarios están permitidos en este modo.
# Si su patrón incluye espacios en blanco, asegúrese de usar \ s. Si necesita hacer coincidir el carácter #, use [#].

# Al crear la expresión regular maestra, las reglas se agregan en el siguiente orden:
# > Todos los tokens definidos por funciones se agregan en el mismo orden en que aparecen en el archivo lexer.
# > Los tokens definidos por cadenas se agregan a continuación clasificándolos en orden decreciente de longitud de expresión regular
#   (las expresiones más largas se agregan primero).

# Sin este orden, puede resultar difícil hacer coincidir correctamente ciertos tipos de tokens.
# Por ejemplo, si desea tener tokens separados para "=" y "==", debe asegurarse de que "==" esté marcado primero.
# Al ordenar las expresiones regulares en orden de longitud decreciente, este problema se resuelve para las reglas definidas como cadenas.
# Para las funciones, el orden se puede controlar explícitamente ya que las reglas que aparecen primero se verifican primero.

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Para manejar palabras reservadas, debe escribir una sola regla para que coincida con un identificador y realizar una búsqueda
# de nombre especial en una función como esta:

reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE'
}

tokens = ['LPAREN','RPAREN','ID'] + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Controlo palabras reservadas
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
3 + 4 * 10
  + -20 *2
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
    print(tok.type, tok.value, tok.lineno, tok.lexpos)




