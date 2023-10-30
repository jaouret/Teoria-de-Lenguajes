%{
int yylex(void);
void yyerror(char *s);
int yywrap(void){
	return 1;
}
#include <stdio.h>
#include<stdlib.h>
enum elementoArbol {nodo_operando, nodo_num, nodo_variable};
typedef struct arbol {
  enum elementoArbol tipoNodo;
   union {
     struct {struct arbol *izq, *der; char operador;} un_operador;
     int a_numero;
     char a_variable;
   } body;
} arbol;
static arbol *construir_operador (arbol *l, char o, arbol *r) {
   arbol *resultado= (arbol*) malloc (sizeof(arbol));
   resultado->tipoNodo= nodo_operando;
   resultado->body.un_operador.izq= l;
   resultado->body.un_operador.operador= o;
   resultado->body.un_operador.der= r;
   return resultado;
}

 static arbol *construir_numero (int n) {
   arbol *resultado= (arbol*) malloc (sizeof(arbol));
   resultado->tipoNodo= nodo_num;
   resultado->body.a_numero= n;
   return resultado;
}
 static arbol *construir_variable (char v) {
   arbol *resultado= (arbol*) malloc (sizeof(arbol));
   resultado->tipoNodo= nodo_variable;
   resultado->body.a_variable= v;
   return resultado;
 }
 static void imprimirArbol (arbol *t, int nivel) {
 #define salto 4
   if (t)
     switch (t->tipoNodo)
     {
       case nodo_operando:
        imprimirArbol (t->body.un_operador.der, nivel+salto);
        printf ("%*c%c\n", nivel, ' ', t->body.un_operador.operador);
        imprimirArbol (t->body.un_operador.izq, nivel+salto);
        break;
       case nodo_num:
        printf ("%*c%d\n", nivel, ' ', t->body.a_numero);
        break;
       case nodo_variable:
        printf ("%*c%c\n", nivel, ' ', t->body.a_variable);
     }
 }
 static void infix_orden_imprimirArbol (arbol *t, int nivel) {
 #define salto 4
   if (t)
     switch (t->tipoNodo)
     {
       case nodo_operando:
        imprimirArbol (t->body.un_operador.izq, nivel+salto);
        printf ("%*c%c\n", nivel, ' ', t->body.un_operador.operador);
        imprimirArbol (t->body.un_operador.der, nivel+salto);
        break;
       case nodo_num:
        printf ("%*c%d\n", nivel, ' ', t->body.a_numero);
        break;
       case nodo_variable:
        printf ("%*c%c\n", nivel, ' ', t->body.a_variable);
     }
 }
 static void postfix_orden_imprimirArbol (arbol *t, int nivel) {
 #define salto 4
   if (t)
     switch (t->tipoNodo)
     {
       case nodo_operando:
        imprimirArbol (t->body.un_operador.izq, nivel+salto);
        imprimirArbol (t->body.un_operador.der, nivel+salto);
        printf ("%*c%c\n", nivel, ' ', t->body.un_operador.operador);
        break;
       case nodo_num:
        printf ("%*c%d\n", nivel, ' ', t->body.a_numero);
        break;
       case nodo_variable:
        printf ("%*c%c\n", nivel, ' ', t->body.a_variable);
     }
 }
%}
%union{
   int a_numero;
   char a_variable;
   struct arbol *a_arbol;
};
%left '+' 
%left '-'
%left '*'
%token <a_numero> numero
%token <a_variable> variable
%type <a_arbol> stmt exp term 

%%
stmt:	variable '=' exp        {$$ = construir_operador(construir_variable($1),'=',$3);printf("imprimirArbol function\n");imprimirArbol ($$,1);printf("orden infix  imprimirtArbol\n");infix_orden_imprimirArbol($$,1);printf("orden postfix imprimirArbol\n");postfix_orden_imprimirArbol($$,1);}
        ;
        
exp:	exp '*' term		{$$ = construir_operador($1,'*',$3);}
	|exp '+' term          	{$$ = construir_operador ($1, '+', $3);}
        | exp '-' term          {$$ = construir_operador ($1, '-', $3);} 
        |term                  	{$$ = $1;}
        ;
        
term:	'(' exp ')'           	{$$ = $2;}	 
	|variable              {$$ = construir_variable ($1);}
        ;
%%
void yyerror (char *s) {
	fprintf (stderr, "%s\n", s);
	}
int main (void) {
	return yyparse();
	}