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
%token <int_val> ADDOP EQUOP RELOP FIN_LINEA
%token <int_val> LBRACK RBRACK COMMA ASSIGN
%token <symtab_item> ID
%token <int_val> 	 ICONST
%token <double_val>  FCONST
%token <char_val> 	 CCONST
%token <str_val>     STRING


/* precedencias y asociatividades */
%left LBRACK RBRACK
%left ADDOP
%left RELOP
%left EQUOP
%right ASSIGN
%left COMMA

%start program

%%

program: statements SALIR FIN_LINEA;
statements: statements statement | statement ;
statement: mensaje_statement | mientras_statement | ingresar_datos_statement | mostrar_datos_statement | var_inic | var_dec;
mensaje_statement: MENSAJE_PANTALLA ASSIGN LBRACK STRING RBRACK FIN_LINEA ;
mientras_statement: MIENTRAS expressions FIN_MIENTRAS FIN_LINEA ;
ingresar_datos_statement: INGRESAR_DATOS ID FIN_LINEA;
mostrar_datos_statement: MOSTRAR ID FIN_LINEA;
var_dec: VARIABLE ID var_cola FIN_LINEA;
var_cola: COMMA ID | /* vacio */; 
var_inic: ID ASSIGN ICONST FIN_LINEA;
var_asig: ID ASSIGN ID | ID ASSIGN ID ADDOP ID | ID ASSIGN ID ADDOP ICONST;
expressions: expressions expression | expression;
expression: expression EQUOP expression |
    expression RELOP expression |
    expression ADDOP expression |
	statement |
	ID RELOP ICONST |
	var_asig ;
//	ID ASSIGN ID ADDOP ID; 
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
