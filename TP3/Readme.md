# Generar un compilador simple usando RPly y LLVMlite

Pasar por las diferentes etapas desde el análisis léxico y sintáctico hasta la generación de código intermedio (IR), optimización y generación de resultados.

## Análisis Léxico (Lexer)

Dividir el código fuente en tokens. Usamos RPly para definir nuestro lexer.

Ver
- lexer.py
- salida_lexer

## Análisis Sintáctico (Parser)

Definimos el parser que toma los tokens y se construye un árbol de análisis sintáctico (AST).
Análisis Sintáctico (Parser)

Ahora, definimos el parser que toma estos tokens y construye un árbol de análisis sintáctico (AST).er 
- parser.py
- resultado_parser

Hacer un ejemplo más complejo.

Enviar AST a un archivo.
