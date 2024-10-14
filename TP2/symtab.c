#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "semanticas.h"
#include "symtab.h"

/*  ámbito actual */
int cur_scope = 0;

/* bandera para declarar variable */
int declare = 0; // 1: declaro variable, 0: no declaro

// Funciones de la tabla de símbolos

void init_hash_table(){
	int i; 
	hash_table = malloc(SIZE * sizeof(list_t*));
	for(i = 0; i < SIZE; i++) hash_table[i] = NULL;
}

unsigned int hash(char *key){
	unsigned int hashval = 0;
	for(;*key!='\0';key++) hashval += *key;
	hashval += key[0] % 11 + (key[0] << 3) - key[0];
	return hashval % SIZE;
}

void insert(char *name, int len, int type, int lineno){
	unsigned int hashval = hash(name);
	list_t *l = hash_table[hashval];
	
	while ((l != NULL) && (strcmp(name,l->st_name) != 0)) l = l->next;
	
	/* variable aún no en la tabla */
	if (l == NULL){
		/* comprobar si realmente estamos declarando variable */
		if(declare == 1){
			
			l = (list_t*) malloc(sizeof(list_t));
			strncpy(l->st_name, name, len);
			l->st_type = type;
			l->scope = cur_scope;
			l->lines = (RefList*) malloc(sizeof(RefList));
			l->lines->lineno = lineno;
			l->lines->next = NULL;
			
			/* agrego a hashtable */
			l->next = hash_table[hashval];
			hash_table[hashval] = l; 
			printf("Se inserto %s por primera vez con el numero de linea %d...\n", name, lineno);
		}
		else{
			/* agrego para comprobarlo más tarde */
			l = (list_t*) malloc(sizeof(list_t));
			strncpy(l->st_name, name, len);
			l->st_type = type;
			l->scope = cur_scope;
			l->lines = (RefList*) malloc(sizeof(RefList));
			l->lines->lineno = lineno;
			l->lines->next = NULL;
			l->next = hash_table[hashval];
			hash_table[hashval] = l;
			printf("Inserto %s en la linea %d para volver a comprobarlo mas tarde...\n", name, lineno);
			
			/* Añadiendo identificador a la cola de revisión... */
			add_to_queue(l->st_name, PARAM_CHECK);
		}
	}
	/* encontrado en la tabla */
	else{
		// agrego nro de línea
		if(declare == 0){
			/* busco última referencia */
			RefList *t = l->lines;
			while (t->next != NULL) t = t->next;
			
			/* agrego número de línea a la lista de referencias */
			t->next = (RefList*) malloc(sizeof(RefList));
			t->next->lineno = lineno;
			t->next->next = NULL;
			printf("Encontrado %s nuevamente en la linea %d...\n", name, lineno);
		}
		/* nueva entrada */
		else{
			/* Mismo  ámbito - múltiples errores de declaración ... */
			if(l->scope == cur_scope){
				fprintf(stderr, "Una declaracion multiple de la variable %s en la linea %d\n", name, lineno);
 				exit(1);
			}
			/* otro  ámbito - crear nueva entrada */
			else{
				/* preparo entrada */
				l = (list_t*) malloc(sizeof(list_t));
				strncpy(l->st_name, name, len);  
				l->st_type = type;
				l->scope = cur_scope;
				l->lines = (RefList*) malloc(sizeof(RefList));
				l->lines->lineno = lineno;
				l->lines->next = NULL;
				
				/* agrego a hashtable */
				l->next = hash_table[hashval];
				hash_table[hashval] = l; 
				printf("%s insertado para un nuevo ambito con numero de linea %d!\n", name, lineno);
			}	
		}		
	}
}

list_t *lookup(char *name){ /* devolver símbolo si se encuentra o NULL si no se encuentra */
	unsigned int hashval = hash(name);
	list_t *l = hash_table[hashval];
	while ((l != NULL) && (strcmp(name,l->st_name) != 0)) l = l->next;
	return l;
}

void symtab_dump(FILE * of){  
  int i;
  fprintf(of,"------------ ------ ------ ------------\n");
  fprintf(of,"Nombre       Tipo   Ambito Nro de Lineas\n");
  fprintf(of,"------------ ------ ------ ------------\n");
  for (i=0; i < SIZE; ++i){ 
	if (hash_table[i] != NULL){ 
		list_t *l = hash_table[i];
		while (l != NULL){ 
			RefList *t = l->lines;
			fprintf(of,"%-12s ",l->st_name);
			if (l->st_type == INT_TYPE)                fprintf(of,"%-7s","int");
			else if (l->st_type == REAL_TYPE)          fprintf(of,"%-7s","real");
			else if (l->st_type == CHAR_TYPE)          fprintf(of,"%-7s","char");
			else if (l->st_type == ARRAY_TYPE){
				fprintf(of,"array of ");
				if (l->inf_type == INT_TYPE) 		   fprintf(of,"%-7s","int");
				else if (l->inf_type  == REAL_TYPE)    fprintf(of,"%-7s","real");
				else if (l->inf_type  == CHAR_TYPE)    fprintf(of,"%-7s","char");
				else fprintf(of,"%-7s","undef");
			}
			else if (l->st_type == POINTER_TYPE){
				fprintf(of,"%-7s %s","pointer to ");
				if (l->inf_type == INT_TYPE) 		   fprintf(of,"%-7s","int");
				else if (l->inf_type  == REAL_TYPE)    fprintf(of,"%-7s","real");
				else if (l->inf_type  == CHAR_TYPE)    fprintf(of,"%-7s","char");
				else fprintf(of,"%-7s","undef");
			}
			else if (l->st_type == FUNCTION_TYPE){
				fprintf(of,"%-7s %s","function returns ");
				if (l->inf_type == INT_TYPE) 		   fprintf(of,"%-7s","int");
				else if (l->inf_type  == REAL_TYPE)    fprintf(of,"%-7s","real");
				else if (l->inf_type  == CHAR_TYPE)	   fprintf(of,"%-7s","char");
				else fprintf(of,"%-7s","undef");
			}
			else fprintf(of,"%-7s","undef"); // if UNDEF or 0
			fprintf(of,"  %d  ",l->scope);
			while (t != NULL){
				fprintf(of,"%4d ",t->lineno);
			t = t->next;
			}
			fprintf(of,"\n");
			l = l->next;
		}
    }
  }
}

// Tipos de Funciones

void set_type(char *name, int st_type, int inf_type){ // establecer el tipo de una entrada (declaración)
	/* lookup */
	list_t *l = lookup(name);
	
	/* tipo "main" */
	l->st_type = st_type;
	
	/* si matriz, puntero o función */
	if(inf_type != UNDEF){
		l->inf_type = inf_type;
	}	
}

int get_type(char *name){ //obtener el tipo de entrada
	/* lookup  */
	list_t *l = lookup(name);
	
	/* if "simple" type */
	if(l->st_type == INT_TYPE || l->st_type == REAL_TYPE || l->st_type == CHAR_TYPE){
		return l->st_type;
	}
	/* si matriz, puntero o función  */
	else{
		return l->inf_type;
	}
}

// Funciones de gestión del ámbito

void hide_scope(){ /* ocultar el ámbito actual */
	list_t *l;
	int i;
	printf("Ocultando ambito \'%d\':\n", cur_scope);
	/* for all the lists */
	for (i = 0; i < SIZE; i++){
		if(hash_table[i] != NULL){
			l = hash_table[i];
			/* Encuentra el primer elemento que es de otro ámbito */
			while(l != NULL && l->scope == cur_scope){
				printf("Ocultando %s..\n", l->st_name);
				l = l->next;
			}
			/* Establecer la lista igual a ese elemento */
			hash_table[i] = l;
		}
	}
	cur_scope--;
}

void incr_scope(){ /* ir al siguiente ámbito */
	cur_scope++;
}

// Declaración de funciones y parámetros

Param def_param(int par_type, char *param_name, int passing){ // defino parámetero
	Param param; /* Estructura del Parámetro */
	
	
	param.par_type = par_type;
	strcpy(param.param_name, param_name);
	param.passing = passing;
	
	
	return param;
}

int func_declare(char *name, int ret_type, int num_of_pars, Param *parameters){ 
	/* lookup */
	list_t *l = lookup(name);
	

	if(l->st_type != UNDEF){
		
		l->st_type = FUNCTION_TYPE;
		
		
		l->inf_type = ret_type;
		
		
		l->num_of_pars = num_of_pars;
		l->parameters = parameters;
		
		return 0;
	}
	
	else{
		fprintf(stderr, "Funcion %s ya declarada...\n", name);
		exit(1);
	}
}

int func_param_check(char *name, int num_of_pars, Param *parameters){ // comprobar parámetros
	int i, type_1, type_2;
	
	
	list_t *l = lookup(name);
	
	
	if(l->num_of_pars != num_of_pars){
		fprintf(stderr, "La llamada de funcion de %s tiene un numero incorrecto de parametros...\n", name);
		exit(1);
	}
	
	/* comprobar si los parámetros son compatibles */
	for(i = 0; i < num_of_pars; i++){
		/* tipo de parámetro en declaración de función */
		type_1 = l->parameters[i].par_type; 
		
		/* tipo de parámetro en llamada a función*/
		type_2 = parameters[i].par_type; 
		
		/* comprobar la compatibilidad de la llamada de función */
		get_result_type(type_1, type_2, NONE);
		/* el error ocurre automáticamente en la función */
	}
	
	return 0; /* ok */
}

// Revisar las funciones de cola

void add_to_queue(char *name, int type){ /* agrego a la cola */
	revisit_queue *q;
	
	/* cola vacía */
	if(queue == NULL){
	
		q = (revisit_queue*) malloc(sizeof(revisit_queue));
		q->st_name = name;
		q->revisit_type = type;
		q->next = NULL;
		
		/* q "se convierte" en la cola */
		queue = q;
	}
	/* cola no vacía */
	else{
		/* encontrar el último elemento */
		q = queue;
		while(q->next != NULL) q = q->next;
		
		/* añadir elemento al final */
		q->next = (revisit_queue*) malloc(sizeof(revisit_queue));
		q->next->st_name = name;
		q->next->revisit_type = type;
		q->next->next = NULL;
	}		
}

int revisit(char *name){ /* volver a revisar la entrada eliminándola también de la cola */
	revisit_queue *q;
	
	/* caso especial - primera entrada */
	if( strcmp(queue->st_name, name) == 0 ){
		
		/* revisar la entrada dependiendo del tipoe */
		switch(queue->revisit_type){
			case PARAM_CHECK:
				
				break;
			/* ... */
		}
		
		/* elimine la entrada configurando la cola en "siguiente" */
		queue = queue->next;
		
		return 0; // ok
	}
	
	/* busca la entrada que apunta a ella*/
	q = queue;
	while( strcmp(q->next->st_name, name) != 0 ) q = q->next;
	
	/* verificar si no se encontró la entrada */
	if(q == NULL){
		return 1;  // no encontrada
	}
	
	/* revisar la entrada según el tipo */
	switch(q->next->revisit_type){
		case PARAM_CHECK:
			/* PARA HACER: ejecutar la verificación de parámetros */
			break;
		/* ... */
	}
	
	/* elimina la entrada haciendo que el punto de entrada anterior sea */
	/* el "siguiente" de la entrada que queremos eliminar */
	q->next = q->next->next;	
	
	return 0; // ok
}

void revisit_dump(FILE *of){
	int i;
	revisit_queue *q;
	q = queue;
	
	fprintf(of,"------------- ----------------\n");
	fprintf(of,"Identificador Tipo Revisado\n");
	fprintf(of,"------------- ----------------\n");
  	while(q != NULL){
  		fprintf(of, "%-13s", q->st_name);
  		if(q->revisit_type == PARAM_CHECK){
  			fprintf(of,"%s","Comprobacion de parametros");
		}
		
		fprintf(of, "\n");
  		q = q->next;	
	}
}
