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
%token<int_val> CHAR INT FLOAT DOUBLE IF ELSE WHILE FOR CONTINUE BREAK VOID RETURN
%token<int_val> ADDOP MULOP DIVOP INCR OROP ANDOP NOTOP EQUOP RELOP
%token<int_val> LPAREN RPAREN LBRACK RBRACK LBRACE RBRACE SEMI DOT COMMA ASSIGN REFER
%token <symtab_item> ID
%token <int_val> 	 ICONST
%token <double_val>  FCONST
%token <char_val> 	 CCONST
%token <str_val>     STRING

/* precedencias y asociatividades */
%left LPAREN RPAREN LBRACK RBRACK
%right NOTOP INCR REFER
%left MULOP DIVOP
%left ADDOP
%left RELOP
%left EQUOP
%left OROP
%left ANDOP
%right ASSIGN
%left COMMA

%start program

%%

program: declarations statements RETURN SEMI functions_optional ;

/* declaraciones */
declarations: declarations declaration | declaration ;

declaration: { declare = 1; } type names { declare = 0; } SEMI ;

type: INT | CHAR | FLOAT | DOUBLE | VOID ;

names: names COMMA variable | names COMMA init | variable | init ;

variable: ID |
    pointer ID |
    ID array
;

pointer: pointer MULOP | MULOP ;

array: array LBRACK expression RBRACK | LBRACK expression RBRACK ;

init: var_init | array_init ; 

var_init : ID ASSIGN constant ;

array_init: ID array ASSIGN LBRACE values RBRACE ;

values: values COMMA constant | constant ;

/* sentencias = statements */
statements: statements statement | statement ;

statement:
	if_statement | for_statement | while_statement | assigment SEMI |
	CONTINUE SEMI | BREAK SEMI | function_call SEMI | ID INCR SEMI | INCR ID SEMI
;

if_statement:
		IF LPAREN expression RPAREN tail else_if optional_else |
		IF LPAREN expression RPAREN tail optional_else
;

else_if: 
	else_if ELSE IF LPAREN expression RPAREN tail |
	ELSE IF LPAREN expression RPAREN tail
;

optional_else: ELSE tail | /*  vacío */ ;

for_statement: FOR LPAREN assigment SEMI expression SEMI expression RPAREN tail ;

while_statement: WHILE LPAREN expression RPAREN tail ;

tail: LBRACE statements RBRACE ;

expression:
    expression ADDOP expression |
    expression MULOP expression |
    expression DIVOP expression |
    ID INCR |
    INCR ID |
    expression OROP expression |
    expression ANDOP expression |
    NOTOP expression |
    expression EQUOP expression |
    expression RELOP expression |
    LPAREN expression RPAREN |
	var_ref |
    sign constant |
	function_call
;

sign: ADDOP | /*  vacío */ ; 

constant: ICONST | FCONST | CCONST ;

assigment: var_ref ASSIGN expression ;

var_ref: variable | REFER variable ; 

function_call: ID LPAREN call_params RPAREN ;

call_params: call_param | STRING | /*  vacío */

call_param: call_param COMMA expression | expression ; 

/* funciones */
functions_optional: functions | /*  vacío */ ;

functions: functions function | function ;

function: { incr_scope(); } function_head function_tail { hide_scope(); } ;

function_head: { declare = 1; } return_type ID LPAREN { declare = 0; } parameters_optional RPAREN ;

return_type: type | type pointer ;

parameters_optional:  parameters | /*  vacío */ ;

parameters: parameters COMMA parameter | parameter ;

parameter : { declare = 1; } type variable { declare = 0; } ;

function_tail: LBRACE declarations_optional statements_optional return_optional RBRACE ;

declarations_optional: declarations | /*  vacío */ ;

statements_optional: statements | /*  vacío */ ;

return_optional: RETURN expression SEMI | /*  vacío */ ;

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
