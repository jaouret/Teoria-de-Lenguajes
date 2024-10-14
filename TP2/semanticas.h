/* tipos de tokens */
#define UNDEF 0
#define INT_TYPE 1
#define REAL_TYPE 2
#define CHAR_TYPE 3
#define ARRAY_TYPE 4
#define POINTER_TYPE 5
#define FUNCTION_TYPE 6

/* tipos de operadores */
#define NONE 0		// para comprobar tipos solamente - asignación, parámetro
#define ARITM_OP 1 // SUMOP, MULOP, DIVOP (+, -, *, /)
#define INCR_OP 2   // INCR (++, --)
#define BOOL_OP 3   // OROP, ANDOP (||, &&)
#define NOT_OP 4    // NOTOP (!)
#define REL_OP 5    // RELOP (>, <, >=, <=)
#define IGUAL_OP 6    // IGUALOP (==, !=)

// Declaraciones de funciones
int get_result_type (int type_1, int type_2, int op_type); /* verificación de tipo y tipo de resultado */
void type_error(int type_1, int type_2, int op_type);      /* imprimir error de tipo */
