/* tamaño máximo de la tabla hash */
#define SIZE 211

/* tamaño máximo de tokens-identificadores */
#define MAXTOKENLEN 40

/* como se pasa el parametro*/
#define BY_VALUE 1
#define BY_REFER 2


typedef struct Param{
	int par_type;
	char param_name[MAXTOKENLEN];
	
	// para almacenar el valor
	int ival; double fval; char *st_sval;
	int passing; // valor o referencia
}Param;

/* una lista enlazada de referencias (linenos) para cada variable */
typedef struct RefList{ 
    int lineno;
    struct RefList *next;
}RefList;

// estructura que representa un nodo de lista
typedef struct list_t{
	char st_name[MAXTOKENLEN];
    int st_size;
    int scope;
    RefList *lines;
    
	// para almacenar valor y, a veces, más información
	int st_ival; double st_fval; char st_sval;
    int st_type;
    
    // para matrices (tipo info), para punteros (tipo puntero)
	// y para funciones (tipo de retorno)
	int inf_type;
	
	// arreglos
	int *i_vals; double *f_vals; char *s_vals;
	int array_size;
	
	// Parámetros de función
	Param *parameters;
	int num_of_pars;
	
	// puntero al siguiente elemento de la lista
	struct list_t *next;
}list_t;

/* Cola de identificadores para volver a revisar*/
typedef struct revisit_queue{
	// nombre del identificador
	char *st_name;
	int revisit_type;
	struct revisit_queue *next;
}revisit_queue;


#define PARAM_CHECK 1 /* Verificar los parámetros de la llamada a la función cuando se declaran las funciones */

static list_t **hash_table;
static revisit_queue *queue;


// Funciones de la tabla de símbolos
void init_hash_table(); 
unsigned int hash(char *key); 
void insert(char *name, int len, int type, int lineno); 
list_t *lookup(char *name); 
void symtab_dump(FILE *of); 

// Tipo de funciones
void set_type(char *name, int st_type, int inf_type); // set the type of an entry (declaration)
int get_type(char *name); // get the type of an entry

// Funciones de gestión del ámbito
void hide_scope(); // ocultar el ámbito actual
void incr_scope(); // ir al siguiente ámbito

//Declaración de funciones y parámetros
Param def_param(int par_type, char *param_name, int passing); 
int func_declare(char *name, int ret_type, int num_of_pars, Param *parameters); 
int func_param_check(char *name, int num_of_pars, Param *parameters); 

// Revisar las funciones de cola
void add_to_queue(char *name, int type); 
int revisit(char *name); 
void revisit_dump(FILE *of); 
