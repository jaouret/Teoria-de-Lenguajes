// Commentario
int gcd (int u, int v) {
	if (v == 0)
		return u;
	else
		return gcd(v, v-u);
}
