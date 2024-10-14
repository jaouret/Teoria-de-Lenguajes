# Generar un compilador simple usando RPly y LLVMlite

Pasar por las diferentes etapas desde el análisis léxico y sintáctico hasta la generación de código intermedio (IR), optimización y generación de resultados.
Aegurarse de tener instaladas las dependencias de RPly y llvmlite (pip install rply llvmlite).
Se muestran las etapas del código python por separado pero pueden ponerse todas en el mismo archivo python.

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

## Generación de Código Intermedio (IR) con llvmlite

Convertimos el AST en instrucciones de bajo nivel (LLVM IR) utilizando llvmlite.

Ver
- rep_intermedia.py
- resultado_ri

## Compilación JIT y Ejecución

Utilizamos llvmlite.binding para compilar y ejecutar el código utilizando JIT (Just-In-Time Compilation).  

- jit.py
- resultado_jit

## Resumen del Flujo

    Lexer: Convertimos el código fuente en tokens.
    Ejemplo: (2 + 3) * 4 → Tokens: LPAREN, NUMBER(2), PLUS, NUMBER(3), MULTIPLY, NUMBER(4)

    Parser: Convertimos los tokens en un AST.
    Ejemplo: (' * ', ('+', 2, 3), 4).

    Generación de IR: Convertimos el AST a código LLVM IR.
    Ejemplo de IR:

    llvm

%0 = add i32 2, 3
%1 = mul i32 %0, 4
ret i32 %1

Compilación JIT y Ejecución: Compilamos el IR a código máquina y ejecutamos el resultado.

Ejemplo de ejecución: (2 + 3) * 4 = 20.
