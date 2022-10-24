# Flex-Bison-IngInf-UCA

Ejecutar

flex lexer.l

Si se ejecuta bison con -v genera detalle de gramáticas y estados que ayudan a encontrar errores

bison -dv parser.y 

gcc  -o csimple parser.tab.c lex.yy.c
./csimple ejemplo.c

Se agregó una primera versión con semánticas.
