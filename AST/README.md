- recorrer_AST4.py
- recorrer_AST5.py (incorpora expresiones if then)
- dibujar_AST.py genera versión gráfica del AST
- ast5.txt es un AST en forma de texto, como entrada de los programas anteriores
- ast4.txt es un AST en forma de texto, como entrada de los programas anteriores

Programas en Python que trabajan con un Árbol de Sintaxis Abstracta (AST) y generan Código de Tres Direcciones (TAC) a partir de ese AST.

.generar_tac(nodo, contador_temp, expresion_detectada=False):
Esta es una función que genera el código TAC a partir del AST.
Recibe tres parámetros:
- nodo: El nodo actual del AST que se está procesando.
- contador_temp: Un contador que lleva la cuenta de las variables temporales.
- expresion_detectada: Un indicador opcional que se utiliza para distinguir si el nodo actual representa una expresión matemática. Por defecto, se establece en False.

En el caso base de la recursión, se verifica si el nodo es una lista.
Si lo es, se procede a analizar el operador del nodo.

Si el operador es '=' (una asignación), se extrae la variable a la que se asigna el resultado y se generan códigos TAC para los operadores a la izquierda y a la derecha de la asignación. Luego, se imprime la asignación.

Si el operador no es '=', se considera una operación unaria o binaria. Se generan códigos TAC para los operadores a la izquierda y a la derecha y se crea una variable temporal (temp_var)	para almacenar el resultado. Luego, se imprime la operación.

- leer_ast_de_archivo(nombre_archivo): Esta función lee el AST desde un archivo con el nombre especificado y lo devuelve como una cadena de caracteres.

En el bloque if __name__ == "__main__":, se inicia la ejecución del programa.
Se lee el AST desde un archivo, se convierte a una estructura de datos en forma de lista,	se inicializa el contador de variables temporales y se llama a la función generar_tac para generar el código TAC.

El código utiliza recursión para recorrer el AST y generar el código TAC correspondiente.
El resultado se imprime en la consola.
El AST se debe proporcionar en un archivo con el nombre "ast4.txt" o modificar la variable archivo_ast con el nombre del archivo adecuado.

