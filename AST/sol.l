%{
#include"y.tab.h"
%}

%%
[0-9]+			{yylval.a_numero = atoi(yytext); return numero;}

[a-zA-Z]		{yylval.a_variable = yytext[0];return variable;}

[-+*/( )=]              {return yytext[0];}

[ \t\n]			{;}

.			{printf("Caracter No Aceptado");}
%%