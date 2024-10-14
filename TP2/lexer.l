%option noyywrap

%{
	#include <stdio.h>
	#include <stdlib.h>
	#include <string.h>
	#include <wchar.h>
	#include <locale.h>
	#include "symtab.h"
	#include "semanticas.h"
	#include "parser.tab.h"
	extern FILE *yyin;
	extern FILE *yyout;
	
	int lineno = 1; // inicializar a 1
%}

alfabeto 		[a-zA-Z]
digito 		[0-9]
alfanumerico 		{alfabeto}|{digito}
print		[ -~]

ID 		{alfabeto}+{alfanumerico}*
ICONST		"0"|[0-9]{digito}*
STRING		\"{print}*\"

%%

"COMENTARIO ".*   { printf("Saco comentario en la linea %d\n", lineno); } 	
"MENSAJE_PANTALLA" { printf("MENSAJE_PANTALLA\n"); return MENSAJE_PANTALLA; }
"FIN_LINEA" { printf("FIN_LINEA\n");return FIN_LINEA; }
"VARIABLE"		{ printf("VARIABLE\n");return VARIABLE; }
"INGRESAR_DATOS" { printf("INGRESAR_DATOS\n");return INGRESAR_DATOS; }
"MIENTRAS"	{ printf("MIENTRAS\n");return MIENTRAS; }
"FIN_MIENTRAS"	{ printf("FIN_MIENTRAS\n");return FIN_MIENTRAS; }
"MOSTRAR" { printf("MOSTRAR\n");return MOSTRAR; }
"SALIR"	{ printf(" SALIR\n");return SALIR; }

"+"|"-"		{ printf("SUMOP\n");return SUMOP; }
"=="|"!="		{ printf("IGUALOP\n");return IGUALOP; }
">"|"<"|">="|"<="	{ printf("RELOP\n");return RELOP; }


"["			{ printf("CORCHETE_IZQ\n");return CORCHETE_IZQ; }
"]"			{ printf("CORCHETE_DER\n");return CORCHETE_DER; }
","			{ printf("COMA\n");return COMA; }
"="			{ printf("IGUAL\n");return IGUAL; }

{ID} 			{
				// insertar identificador en la tabla de símbolos
				insert(yytext, strlen(yytext), UNDEF, lineno);
				yylval.symtab_item = lookup(yytext);
				printf("ID %s\n",yytext);return ID;
			}
{ICONST} 		{ yylval.int_val   = atoi(yytext);printf("ICONST %s\n",yytext); return ICONST; }
{STRING} 		{ yylval.str_val = malloc(yyleng * sizeof(char)); strcpy(yylval.str_val, yytext); printf("STRING %s\n",yytext); return STRING; }

"\n" 			{ lineno += 1; }
[ \t\r\f]+		/* saco blancos */

.			{ yyerror("Caracter no reconocido"); }

%%
