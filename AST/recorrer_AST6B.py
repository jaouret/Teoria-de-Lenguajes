def generar_tac(nodo, contador_temp, expresion_detectada=False, label_then=None, label_else=None):
    if isinstance(nodo, list):
        operador = nodo[0]

        if operador == '=':
            # Asignación
            var = nodo[1]
            if len(nodo) >= 3:
                operador_por_der, contador_temp = generar_tac(nodo[2], contador_temp, expresion_detectada=True)
            else:
                operador_por_der = None
            print(f"{var} = {operador_por_der}")
            return var, contador_temp

        elif operador == 'if':
            # Construcción if-then-else

            if len(nodo) >= 3:
                condicion, contador_temp = generar_tac(nodo[1], contador_temp, expresion_detectada=True)
            else:
                condicion = None

            etiqueta_else = label_else if label_else else f"L{contador_temp}"
            contador_temp += 1
            etiqueta_fin = f"L{contador_temp}"
            contador_temp += 1

            print(f"if {condicion} goto {etiqueta_else}")
            if len(nodo) >= 3:
                condicion, contador_temp = generar_tac(nodo[2], contador_temp, etiqueta_fin, etiqueta_else)
            else:
                condicion = None


            if len(nodo) > 3:
                print(f"goto {etiqueta_fin}")
                print(f"{etiqueta_else}:")
                if len(nodo) >= 3:
                    condicion, contador_temp = generar_tac(nodo[3], contador_temp, etiqueta_fin, etiqueta_else)
                else:
                    condicion = None

                print(f"{etiqueta_fin}:")

            return None, contador_temp

        else:
            # Operación unaria o binaria
            if len(nodo) >= 2:
                operador_por_izq, contador_temp = generar_tac(nodo[1], contador_temp, expresion_detectada=True)
                operador_por_der, contador_temp = generar_tac(nodo[2], contador_temp, expresion_detectada=True)
            else:
                operador_por_izq = None
                operador_por_der = None


            temp_var = f"t{contador_temp}"
            contador_temp += 1

            operacion = ""  # Inicializa operacion

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
    return eval(cadena_caracteres_ast)

# Example usage
if __name__ == "__main__":
    archivo_ast = "ast6.txt"  # Replace with the path to your AST file

    # Leo el AST de un archivo
    ast = leer_ast_de_archivo(archivo_ast)

    # Inicializo contador de variables temporales
    contador_temp_aux = 1
    generar_tac(ast, contador_temp_aux)
