COMENTARIO Programa para análisis léxico y sintáctico
MENSAJE_PANTALLA = ["Serie de Fibonacci"] FIN_LINEA
MENSAJE_PANTALLA = ["Ingresar cantidad de numeros de la serie deseados"] FIN_LINEA

VARIABLE a FIN_LINEA
VARIABLE c FIN_LINEA
INGRESAR_DATOS c FIN_LINEA

a = 0 FIN_LINEA
b = 1 FIN_LINEA
MOSTRAR a FIN_LINEA
MIENTRAS c > 0 
    MOSTRAR a FIN_LINEA
    c = a + b
    a = b
    b = c
    c = c - 1
FIN_MIENTRAS FIN_LINEA
SALIR FIN_LINEA
