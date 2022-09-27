#define LUNG 100
#include <stdio.h>

// structura grafului
typedef struct 
{
    int V, M, **a;

}Graph;

// aloc memorie pt graf
Graph* create();

void citire(FILE *f, Graph *orientat, Graph *neorientat, Graph *distante, int *n, char ***table);

// ex 2
void cautare(Graph *costuri, int n, char **table);

// ex 3
void total(Graph *costuri, int n);

void printSolution(int dist[], int n);
int minDistance(int dist[], int sps[], int V);
void dijkstra(Graph *g, int s, char **table);

// ex 7
void print_all_paths(Graph *g, int source, int dest, char **table);
void dfs(FILE *f, Graph *g, int source, int dest, int poz, int *visited, int *path, char **table);