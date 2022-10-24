/* Programa ejemplo con:
declaraciones: declarations 
sentencias: statements 
funciones: functions
*/

// main (declarations statements)
// declaraciones = declarations
int i;                    // variable simple
char c = 'c';             // variable inicializada
double val = 2.5, res[6]; // variable double inicializada y arreglo
double *p;                // variable tipo puntero			  
// sentencias = statements
p = &res; // asignación = assigment
for(i = 0; i < 10; i++){ 
	if(i > 5){ 
    	break;
	}
	else if(i == 5){
		i = 2 * i;
		val = func1();
		*p = add(val, i);
		print(res[i]);
		print("\n");
		continue;
	}
	else{
		*p = add(val, i);
    	val = res[i];
   	 	print(res[i]);
    	print("\n");
    	p = p + 1;
	}
	
	if(i == 2 && val == 4.5){ 
		print("itera: 3\n");
	}
}

while(i < 12){ 
	print(i);
	print(" ");
	func2(c);
	i++;
}
print("\n");
return;

// otras funciones (functions)
int func1(){ 		/* sin parámetros */
	// sentencias = statements
	return 5;
}
void func2(char c){ /* con 1 parámetro */
	// declaraciones = declarations
	char *s;
	// sentencias = statements
	*s = c;
	print(*s);
}
double add (double a, int b){  /* con 2 parámetros */
    // declaraciones = declarations
    double res;
    // sentencias = statements
    res = a + b;
    return res;
}
