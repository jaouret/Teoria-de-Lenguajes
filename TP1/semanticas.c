#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>
#include <locale.h>
#include "semanticas.h"

// tipos: INT_TYPE, REAL_TYPE, CHAR_TYPE

int get_result_type(int type_1, int type_2, int op_type){ /* verificación de tipo y tipo de resultado */
	switch(op_type){
		case NONE: /* compatibilidad de tipo, '1': compatible */
			
			if(type_1 == INT_TYPE){
			
				if(type_2 == INT_TYPE || type_2 == CHAR_TYPE){
					return 1;
				}
				else{
					type_error(type_1, type_2, op_type);
				}
			}
			else if(type_1 == REAL_TYPE){
				
				if(type_2 == INT_TYPE || type_2 == REAL_TYPE || type_2 == CHAR_TYPE){
					return 1;
				}
				else{
					type_error(type_1, type_2, op_type);
				}
			}
			
			else if(type_1 == CHAR_TYPE){
				
				if(type_2 == INT_TYPE || type_2 == CHAR_TYPE){
					return 1;
				}
				else{
					type_error(type_1, type_2, op_type);
				}
			}
			break;
		/* ---------------------------------------------------------- */
		case ARITHM_OP: /* operador arithmetic */
			
			if(type_1 == INT_TYPE){
				
				if(type_2 == INT_TYPE || type_2 == CHAR_TYPE){
					return INT_TYPE;
				}
				
				else if(type_2 == REAL_TYPE){
					return REAL_TYPE;
				}
				else{
					type_error(type_1, type_2, op_type);
				}
			}
			
			else if(type_1 == REAL_TYPE){
				
				if(type_2 == INT_TYPE || type_2 == REAL_TYPE || type_2 == CHAR_TYPE){
					return REAL_TYPE;
				}
				else{
					type_error(type_1, type_2, op_type);
				}
			}
			
			else if(type_1 == CHAR_TYPE){
				
				if(type_2 == INT_TYPE || type_2 == CHAR_TYPE){
					return CHAR_TYPE;
				}
				
				else if(type_2 == REAL_TYPE){
					return REAL_TYPE;
				}
				else{
					type_error(type_1, type_2, op_type);
				}
			}
			else{
				type_error(type_1, type_2, op_type);
			}
			break;
		/* ---------------------------------------------------------- */
		case INCR_OP: /* caso especial de INCR */
			
			if(type_1 == INT_TYPE){
				return INT_TYPE;
			}
			
			else if(type_1 == REAL_TYPE){
				return REAL_TYPE;
			}
			
			else if(type_1 == CHAR_TYPE){
				return CHAR_TYPE;
			}
			else{
				type_error(type_1, type_2, op_type);
			}
			break;
		/* ---------------------------------------------------------- */
		case BOOL_OP: /* oprador Boolean */
		
			if(type_1 == INT_TYPE){
				
				if(type_2 == INT_TYPE || type_2 == CHAR_TYPE){
					return INT_TYPE;
				}
				else{
					type_error(type_1, type_2, op_type);
				}
			}
			
			else if(type_1 == CHAR_TYPE){
				
				if(type_2 == INT_TYPE || type_2 == CHAR_TYPE){
					return CHAR_TYPE;
				}
				else{
					type_error(type_1, type_2, op_type);
				}
			}
			else{
				type_error(type_1, type_2, op_type);
			}
			break;
		/* ---------------------------------------------------------- */
		case NOT_OP: /* caso especial de  NOTOP */
			
			if(type_1 == INT_TYPE){
				return INT_TYPE;
			}
			
			else if(type_1 == CHAR_TYPE){
				return INT_TYPE;
			}
			else{
				type_error(type_1, type_2, op_type);
			}
			break;
		/* ---------------------------------------------------------- */
		case REL_OP: /* Operador Relacional  */
			
			if(type_1 == INT_TYPE){
				
				if(type_2 == INT_TYPE || type_2 == REAL_TYPE || type_2 == CHAR_TYPE){
					return INT_TYPE;
				}
				else{
					type_error(type_1, type_2, op_type);
				}
			}
			else if(type_1 == REAL_TYPE){
				
				if(type_2 == INT_TYPE || type_2 == REAL_TYPE || type_2 == CHAR_TYPE){
					return INT_TYPE;
				}
				else{
					type_error(type_1, type_2, op_type);
				}
			}
			
			else if(type_1 == CHAR_TYPE){
				
				if(type_2 == INT_TYPE || type_2 == REAL_TYPE || type_2 == CHAR_TYPE){
					return INT_TYPE;
				}
				else{
					type_error(type_1, type_2, op_type);
				}
			}
			else{
				type_error(type_1, type_2, op_type);
			}
			break;
		/* ---------------------------------------------------------- */
		case EQU_OP: /* Operador de igualadad */
			
			if(type_1 == INT_TYPE){
				 
				if(type_2 == INT_TYPE || type_2 == CHAR_TYPE){
					return INT_TYPE;
				}
				else{
					type_error(type_1, type_2, op_type);
				}
			}
			else if(type_1 == REAL_TYPE){
				 
				if(type_2 == REAL_TYPE){
					return INT_TYPE;
				}
				else{
					type_error(type_1, type_2, op_type);
				}
			}
			
			else if(type_1 == CHAR_TYPE){
				 
				if(type_2 == INT_TYPE || type_2 == CHAR_TYPE){
					return INT_TYPE;
				}
				else{
					type_error(type_1, type_2, op_type);
				}
			}
			else{
				type_error(type_1, type_2, op_type);
			}
			break;
		/* ---------------------------------------------------------- */
		default: /* error de selecci+on en el case */
			fprintf(stderr, "Error en la seleccion del operador...\n");
			exit(1);
	}
}

void type_error(int type_1, int type_2, int op_type){ /* imprimir el tipo de error */
	fprintf(stderr, "Conflicto de tipo entre %d y %d usando operador %d\n", type_1, type_2, op_type);
	exit(1);
}