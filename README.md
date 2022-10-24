# Flex-Bison-IngInf-UCA

Ejecutar:

flex lexer.l
bison -dv parser.y 
gcc  -o csimple parser.tab.c lex.yy.c
./csimple ejemplo.c

Si se ejecuta bison con -v genera detalle de gramáticas y estados que ayudan a encontrar errores
Se agregó una primera versión con semánticas.
