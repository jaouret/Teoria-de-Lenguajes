# Flex-Bison-IngInf-UCA

Ejecutar:

flex lexer.l

bison -dv parser.y 

gcc  -o csimple parser.tab.c lex.yy.c

./csimple ejemplo.c

Si se ejecuta bison con -v genera detalle de gramáticas y estados que ayudan a encontrar errores
Se agregó una primera versión con semánticas.

Nota sobre la TS:
Cada símbolo o elemento de lista de la tabla de símbolos almacena atributos e información sobre cada identificador. 
Algunos de ellos son generales, otros son solo para algunos tipos específicos de identificadores. 
Para crear la tabla, insertar en la tabla, buscar una entrada, etc., tenemos que implementar las funciones correctas. 

Resolución de ámbito
Inserción y acceso a entradas

La resolución del ámbito se puede hacer en la Tabla de Símbolos.
El ámbito principal o global tendrá el valor '0' y las funciones tendrán el valor '1'. 
No hay otro valor de ámbito que pueda existir en este momento.
La función de búsqueda debe permitir el acceso a las variables de ámbito '0' y '1' cuando están dentro de las funciones. 
Cuando una variable con el mismo nombre ocurre en ambos ámbitos, sólo se accederá a la variable del ámbito actual. 
Para la función principal el ámbito es '0' y no hay declaración de variables en ningún otro ámbito., lo que significa que podemos usar el mismo código que antes.
Cuando estamos dentro de una función (ámbito 1), primero se revisan las variables de ámbito '1' y, si la variable no es una de ellas, entonces entramos en las variables globales de ámbito '0'.
Para implementar esto hay que insertar los identificadores de ámbito '1' al principio de la lista.
De esa forma la primera entrada que se encontrará en la tabla de símbolos, al buscar una entrada específica, siempre será el identificador/variable de ámbito '1'. 
Si no hay ninguno se puede entrar en las variables de ámbito '0'. Por lo tanto la función de búsqueda no tiene que preocuparse por el ámbito.
La función de inserción debe hacer una nueva entrada cuando estemos en un ámbito diferente. Esto se hace con uan variable de bandera que tiene un valor de '1' cuando se declara y '0' cuando no. Si está en el mismo ámbito y se declarara el mismo identificador se causará un error de declaración múltiple.
