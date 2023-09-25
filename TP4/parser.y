%{
	#include "semanticas.c"
	#include "symtab.c"
	#include <stdio.h>
	#include <stdlib.h>
	#include <string.h>
	#include <wchar.h>
	#include <locale.h>
	extern FILE *yyin;
	extern FILE *yyout;
	extern int lineno;
	extern int yylex();
	void yyerror();
%}

/* YYSTYPE union */
%union{
    char char_val;
	int int_val;
	double double_val;
	char* str_val;
	list_t* symtab_item;
}

/* definición de tokens */
%token <int_val> VARIABLE MENSAJE_PANTALLA INGRESAR_DATOS MIENTRAS MOSTRAR FIN_MIENTRAS SALIR
%token <int_val> MOSTRAR_DATOS
%token <int_val> SUMOP IGUALOP RELOP FIN_LINEA
%token <int_val> CORCHETE_IZQ CORCHETE_DER COMA IGUAL
%token <symtab_item> ID
%token <int_val> 	 ICONST
%token <double_val>  FCONST
%token <char_val> 	 CCONST
%token <str_val>     STRING


/* precedencias y asociatividades */
%left CORCHETE_IZQ CORCHETE_DER
%left SUMOP
%left RELOP
%left IGUALOP
%right IGUAL
%left COMA

%start program

%%

program: sentencias SALIR FIN_LINEA;
sentencias: sentencias sentencia | sentencia ;
sentencia: mensaje_sentencia | mientras_sentencia | ingresar_datos_sentencia | mostrar_datos_sentencia | var_inic | var_dec;
mensaje_sentencia: MENSAJE_PANTALLA IGUAL CORCHETE_IZQ STRING CORCHETE_DER FIN_LINEA ;
mientras_sentencia: MIENTRAS expresiones FIN_MIENTRAS FIN_LINEA ;
ingresar_datos_sentencia: INGRESAR_DATOS ID FIN_LINEA;
mostrar_datos_sentencia: MOSTRAR ID FIN_LINEA;
var_dec: VARIABLE ID var_cola FIN_LINEA;
var_cola: COMA ID | /* vacio */; 
var_inic: ID IGUAL ICONST FIN_LINEA;
var_asig: ID IGUAL ID | ID IGUAL ID SUMOP ID | ID IGUAL ID SUMOP ICONST;
expresiones: expresiones expresion | expresion;
expresion: expresion IGUALOP expresion |
    expresion RELOP expresion |
    expresion SUMOP expresion |
	sentencia |
	ID RELOP ICONST |
	var_asig ;
//	ID IGUAL ID SUMOP ID; 
%%

void yyerror ()
{
  fprintf(stderr, "Error de Sintaxis en linea %d\n", lineno);
  exit(1);
}

int main (int argc, char *argv[]){
	
	// inicializar tabla de símbolos
	init_hash_table();
	
	// inicializar la cola de revisión
	queue = NULL;
	
	// análisis
	int flag;
	yyin = fopen(argv[1], "r");
	flag = yyparse();
	fclose(yyin);
	
	printf("Analisis terminado...\n");
	
	if(queue != NULL){
		printf("Advertencia: algo no se ha verificado en la cola de revision...\n");
	}
	
	// symbol table dump
	yyout = fopen("symtab_dump.out", "w");
	symtab_dump(yyout);
	fclose(yyout);
	
	// revisit queue dump
	yyout = fopen("revisit_dump.out", "w");
	revisit_dump(yyout);
	fclose(yyout);
	
	return flag;
}