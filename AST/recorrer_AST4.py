def generar_tac(nodo, contador_temp, expresion_detectada=False):
    if isinstance(nodo, list):
        operador = nodo[0]
        if operador == '=':
            # Asignacion
            var = nodo[1]
            operador_por_der, _ = generar_tac(nodo[2], contador_temp, expresion_detectada=True)
            print(f"{var} = {operador_por_der}")
            return var, contador_temp
        else:
            # Operación unaria o binaria
            operador_por_izq, contador_temp = generar_tac(nodo[1], contador_temp, expresion_detectada=True)
            operador_por_der, contador_temp = generar_tac(nodo[2], contador_temp, expresion_detectada=True)

            temp_var = f"t{contador_temp}"
            contador_temp += 1

            if operador == '+':
                operacion = "+"
            elif operador == '-':
                operacion = "-"
            elif operador == '*':
                operacion = "*"
            elif operador == '/':
                operacion = "/"

            if expresion_detectada:
                print(f"{temp_var} = ({operador_por_izq} {operacion} {operador_por_der})")
            else:
                print(f"{temp_var} = {operador_por_izq} {operacion} {operador_por_der}")

            return temp_var, contador_temp
    else:
        # Nodo en rama (variable o constante)
        return nodo, contador_temp

def leer_ast_de_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo_ast:
        cadena_caracteres_ast = archivo_ast.read()
    return cadena_caracteres_ast  # Leo el AST como una cadena de caracteres

if __name__ == "__main__":
    archivo_ast = "ast4.txt"

    # Leo el AST de un archivo
    cadena_caracteres_ast = leer_ast_de_archivo(archivo_ast)

    # Recorro el AST como una lista
    ast = eval(cadena_caracteres_ast)

    # Inicializo contador de variables temporales
    contador_temp_aux = 1

    # Genero TAC
    _, _ = generar_tac(ast, contador_temp_aux)
