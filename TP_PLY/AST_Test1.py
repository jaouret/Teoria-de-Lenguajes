import nltk
#defining Contex Free Grammar
grammar = nltk.CFG.fromstring("""
program -> statements SALIR FIN_LINEA
statements -> statements statement | statement  
statement -> mensaje_statement | mientras_statement | ingresar_datos_statement | mostrar_datos_statement | var_inic | var_dec 
mensaje_statement -> MENSAJE_PANTALLA ASSIGN LBRACK STRING RBRACK FIN_LINEA  
mientras_statement -> MIENTRAS expressions FIN_MIENTRAS FIN_LINEA  
ingresar_datos_statement -> INGRESAR_DATOS ID FIN_LINEA 
mostrar_datos_statement -> MOSTRAR ID FIN_LINEA 
var_dec -> VARIABLE ID var_cola FIN_LINEA 
var_cola -> COMMA ID | /* vacio */  
var_inic -> ID ASSIGN ICONST FIN_LINEA 
var_asig -> ID ASSIGN ID | ID ASSIGN ID ADDOP ID | ID ASSIGN ID ADDOP ICONST 
expressions -> expressions expression | expression 
expression -> expression EQUOP expression |
    expression RELOP expression |
    expression ADDOP expression |
	statement |
	ID RELOP ICONST |
	var_asig  
  """)

sentence = 'MENSAJE_PANTALLA = ["Serie de Fibonacci"] FIN_LINEA'.split()
def parse(sent):
    #Returns nltk.Tree.Tree format output
    a = []
    parser = nltk.ChartParser(grammar)
    for tree in parser.parse(sent):
        a.append(tree)
    return(a[0])

#Gives output as structured tree
print(parse(sentence))

#Gives tree diagrem in tkinter window
parse(sentence).draw()