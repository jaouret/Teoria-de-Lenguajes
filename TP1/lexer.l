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
	void ret_print(char *token_type);
	void yyerror();
%}

%x ML_COMMENT

alpha 		[a-zA-Z]
digit 		[0-9]
alnum 		{alpha}|{digit}
print		[ -~]

ID 		{alpha}+{alnum}*
ICONST		"0"|[0-9]{digit}*
FCONST		"0"|{digit}*"."{digit}+
CCONST		(\'{print}\')|(\'\\[nftrbv]\')
STRING		\"{print}*\"

%%

"//".*                  { printf("Saco comentario en la linea %d\n", lineno); } 

"/*"                    { printf("Saco comentario desde la linea %d ", lineno); BEGIN(ML_COMMENT); }
<ML_COMMENT>"*/"        { printf("hasta la linea %d\n", lineno); BEGIN(INITIAL); }
<ML_COMMENT>[^*\n]+		
<ML_COMMENT>"*"			
<ML_COMMENT>"\n"        { lineno += 1; }


"char"|"CHAR"       	{ return CHAR; }
"int"|"INT"		{ return INT; }
"float"|"FLOAT"	{ return FLOAT; }
"double"|"DOUBLE"	{ return DOUBLE; }
"if"|"IF"		{ return IF; }
"else"|"ELSE"		{ return ELSE; }
"while"|"WHILE"	{ return WHILE; }
"for"|"FOR"		{ return FOR; }
"continue"|"CONTINUE"	{ return CONTINUE; }
"break"|"BREAK"	{ return BREAK; }
"void"|"VOID"		{ return VOID; }
"return"|"RETURN"	{ return RETURN; }


"+"|"-"		{ return ADDOP; }
"*"			{ return MULOP; }
"/"			{ return DIVOP; }
"++"|"--"		{ return INCR; }
"||"			{ return OROP; }
"&&"			{ return ANDOP; }
"!"			{ return NOTOP; }
"=="|"!="		{ return EQUOP; }
">"|"<"|">="|"<="	{ return RELOP; }


"("			{ return LPAREN; }
")"			{ return RPAREN; }
"]"			{ return RBRACK; }
"["			{ return LBRACK; }
"{"			{ return LBRACE; }
"}"			{ return RBRACE; }
";"			{ return SEMI; }
"."			{ return DOT; }
","			{ return COMMA; }
"="			{ return ASSIGN; }
"&"			{ return REFER; }


{ID} 			{
				// insertar identificador en la tabla de símbolos
				insert(yytext, strlen(yytext), UNDEF, lineno);
				yylval.symtab_item = lookup(yytext);
				return ID;
			}
{ICONST} 		{ yylval.int_val   = atoi(yytext); return ICONST; }
{FCONST} 		{ yylval.double_val = atof(yytext); return FCONST; }
{CCONST} 		{ yylval.char_val  = yytext[0];    return CCONST; }
{STRING} 		{ yylval.str_val = malloc(yyleng * sizeof(char));
				  strcpy(yylval.str_val, yytext);  return STRING; }


"\n"			{ lineno += 1; }
[ \t\r\f]+		/* saco blancos */

.			{ yyerror("Caracter no reconocido"); }

%%