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

Semántica

La verificación de sintaxis es el segundo paso del compilador, luego sigue el análisis semántica.
Para simplificar la gramática y el analizador, usamos las mismas reglas de sintaxis para algunas reglas. El uso de una subregla específica de esa regla no está permitido. Por ejemplo: Una matriz no puede use una expresión dentro de los corchetes '[' y ']'. Al declarar una matriz con o sin inicialización debemos verificar qué tipo de expresión se usó dentro de los corchetes. Sólo se permite el uso de algún valor constante entero, positivo, y el valor total de la expresión dentro de los paréntesis tiene que dar como máximo ese valor. Lo mismo sucederá cuando se use la matriz, porque el valor entre paréntesis tiene que ser una constante entera del rango [0, "tamaño de la matriz" - 1].

Semántica de declaración

Al declarar una variable debemos verificar si esa variable ya se ha declarado en el ámbito actual en el que nos encontramos. 
Este ámbito es principalmente la misma función. 
Las variables de la función principal serán tratadas como variables globales y por tanto cada función, ya sea principal o de las otras opcionales, tendrá acceso a estas variables. 
Una función opcional puede tener una variable con el mismo nombre, pero solo se podrá acceder a la variable del ámbito actual (resolución de ámbito de variables)

La variable de ámbito actual comienza en '0', lo que significa que el ámbito global o el ámbito de la función principal es el índice '0'. 
Cada vez que ingresamos una función incrementamos (+1) ese valor. Es por eso que el ámbito de la función "func1" es '1'. 
cada vez que salimos de una función (una función termina) decrementamos (-1) ese valor, lo que significa que el valor es '0' después de salir de la función "func1". 
En este caso no se permiten declaraciones anidadas de funciones, por lo que el valor del ámbito será '0' para el ámbito principal o global y '1' para cualquier otra función. 
Cuando salimos de un ámbito, también eliminamos u ocultamos las entradas de la tabla de símbolos correspondientes a ese ámbito. Esto explica cómo el ámbito '1' puede almacenar variables de tres funciones diferentes. Entonces, las variables de una función que estamos dejando no serán accesibles en la siguiente función. En realidad, nunca dejamos el ámbito principal (para llegar a '-1') y, por lo tanto, las variables globales de la función principal estarán siempre accesibles.

El ámbito no es lo único que tenemos que verificar. Comprobamos si ya se ha declarado una variable. Si es así hay un error semántico.
Al declarar variables simples (ID) o punteros sin inicialización (los punteros aún no tienen una inicialización), la verificación de la declaración es suficiente. 
Al declarar una variable de arreglo o matriz con o sin inicialización y al inicializar una variable simple, para la arreglo o matriz y la variable simple, los valores de inicialización reales deben ser del tipo constante correcto.
Una arreglo o matriz de enteros no puede tener valores de doble, por ejemplo, pero una arreglo o matriz de dobles podría tener algunos valores de enteros, porque podemos escribirlos sin "perder" información.
De la misma manera, también tenemos que verificar la expresión dentro de los paréntesis.
La expresión debe dar algún valor constante entero positivo. Se puede usar una constante entera "ICONST", reescribiendo las reglas gramaticales, haciendo que la declaración y el uso de una arreglo o matriz sean cosas completamente diferentes.
