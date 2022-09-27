#include <stdio.h>
#include "functii.h"
#include <limits.h>
#include <string.h>
#include <stdlib.h>

Graph* create()
{
    Graph *g = (Graph*)malloc(sizeof(Graph));

    if(g == NULL)
    {
        printf("Graful nu a putut fi alocat!");
        exit(1);
    }

    g->a = NULL;
    g->V = 0;
    g->M = 0;

    return g;
}

void citire(FILE *f, Graph *orientat, Graph *neorientat, Graph *distante, int *n, char ***table)
{
    int i, ok1 = -1, ok2 = -1, numar1 = 0, numar2 = 0;
    char oras[LUNG], *p, *p2;

    while(fgets(oras, LUNG, f))
    {
        oras[strlen(oras) - 1] = 0;

        p = strtok(oras, ",");
        p2 = strtok(NULL, ",");
        p2 = p2 + 1;

        numar1 = atoi(p2);
        
        for(i = 0; i < *n; i++)
        {
            if(strcmp(p, (*table)[i]) == 0)
                ok1 = i;
        }
    
        if(ok1 == -1)
        {
            (*n)++;
            *table = (char**)realloc(*table, (*n) * sizeof(char*));
            (*table)[(*n) - 1] = (char*)malloc(LUNG * sizeof(char));
            strcpy((*table)[*n - 1], p);
            ok1 = *n - 1;

            distante->a = (int**)realloc(distante->a, (*n) * sizeof(int*));
            distante->a[*n - 1] = NULL;
            distante->V++;
            for(i = 0; i < *n; i++)
            {
                distante->a[i] = (int*)realloc(distante->a[i], (*n) * sizeof(int));
            }

            for(i = 0; i < *n; i++)
            {
                distante->a[i][*n - 1] = 0;
                distante->a[*n - 1][i] = 0;
            }

            orientat->a = (int**)realloc(orientat->a, (*n) * sizeof(int*));
            orientat->a[*n - 1] = NULL;
            orientat->V++;
            for(i = 0; i < *n; i++)
            {
                orientat->a[i] = (int*)realloc(orientat->a[i], (*n) * sizeof(int));
            }

            for(i = 0; i < *n; i++)
            {
                orientat->a[i][*n - 1] = 0;
                orientat->a[*n - 1][i] = 0;
            }

            neorientat->a = (int**)realloc(neorientat->a, (*n) * sizeof(int*));
            neorientat->V++;
            neorientat->a[*n - 1] = NULL;
            for(i = 0; i < *n; i++)
                neorientat->a[i] = (int*)realloc(neorientat->a[i], (*n) * sizeof(int));

            for(i = 0; i < *n; i++)
            {
                neorientat->a[i][*n - 1] = 0;
                neorientat->a[*n - 1][i] = 0;
            }
        }

        if(ok2 != -1)
        {
            if(orientat->a[ok2][ok1] == 0)
            {
                orientat->a[ok2][ok1] = 1;
                orientat->M++;
            }

            if(neorientat->a[ok2][ok1] == 0)
            {
                neorientat->a[ok1][ok2] = 1;
                neorientat->a[ok2][ok1] = 1;
                neorientat->M++;
            }

            if(distante->a[ok2][ok1] == 0 || distante->a[ok2][ok1] > numar1 - numar2)
            {
                distante->a[ok2][ok1] = numar1 - numar2;
                distante->a[ok1][ok2] = numar1 - numar2;
                distante->M++;
            }
        }

        numar2 = numar1;
        ok2 = ok1;
        ok1 = -1;

    }

}

void cautare(Graph *costuri, int n, char **table)
{
    int i, j, mn = INT_MAX, mx = INT_MIN, poz_mn_lin, poz_mn_col, poz_mx_lin, poz_mx_col;

    for(i = 0; i < n; i++)
    {
        for(j = 0; j < n; j++)
        {
            if(costuri->a[i][j] < mn && costuri->a[i][j] != 0)
            {
                mn = costuri->a[i][j];
                poz_mn_lin = i;
                poz_mn_col = j;
            }

            if(costuri->a[i][j] > mx && costuri->a[i][j] != 0)
            {
                mx = costuri->a[i][j];
                poz_mx_lin = i;
                poz_mx_col = j;
            }
        }
    }

    FILE *f;

    f = fopen("min.txt", "wt");
    fprintf(f, "%s %s %d", table[poz_mn_lin], table[poz_mn_col], mn);
    fclose(f);

    f = fopen("max.txt", "wt");
    fprintf(f, "%s %s %d", table[poz_mx_lin], table[poz_mx_col], mx);
    fclose(f);


}

void total(Graph *costuri, int n)
{
    FILE *f;
    int i, j, s = 0;

    f = fopen("total.txt", "wt");

    for(i = 0; i < n; i++)
    {
        for(j = 0; j < n; j++)
            s += costuri->a[i][j];
    }

    s /= 2;

    fprintf(f, "%d km de cale ferata", s);

    fclose(f);

}

void printSolution(int dist[], int n)
{
    printf("Varf Distanta fata de sursa \n");
    for (int i = 0; i < n; i++)
        printf("%d %d\n", i, dist[i]);
}

int minDistance(int dist[], int sps[], int V)
{
    int v, min = INT_MAX, min_index;
    for ( v = 0; v < V; v++)
        if (sps[v] == 0 && dist[v] <= min) 
        {
            min = dist[v];
            min_index = v;
        }
    return min_index;
}

void dijkstra(Graph *g, int s, char **table)
{
    int i, j, u, mx = 0;
    char statie[LUNG];
    int dist[g->V];
    int parrent[g->V]; // vectorul cu distantele de la sursa la destinatie
    int sps[g->V]; // sps[i] e 1 daca varful i e inclus in cea mai scurta cale
// initial toate distantele sunt infinit si niciun element nu e in sps
    for ( i = 0; i < g->V; i++)
    {
        dist[i] = INT_MAX;
        sps[i] = 0;
    }
// distanta de la sursa la ea insasi e 0 si adaugam sursa in sps
    dist[s] = 0;
    parrent[s] = -1;
//calculez pentru toate varfurile calea de cost minim
    for (j = 0; j < g->V-1; j++)
    {
// iau varful cu distanta minima pana la sursa dintre varfurile care nu sunt in sps
        u = minDistance(dist, sps, g->V);
        printf("%d\n",u);

// il adaug in sps
        sps[u] = 1;
        for (i = 0; i < g->V; i++)
        {
// Updatez dist[i] daca varful i nu e in sps, daca u si i adiacente si
//daca distanta pe noua ruta e mai mica decat cea stocata anterior
            if (sps[i] == 0 && g->a[u][i]!=0 && dist[u] != INT_MAX && dist[u]+g->a[u][i] < dist[i])
            { 
                dist[i] = dist[u] + g->a[u][i];
                parrent[i] = u;
            }
        }
    }
// afiseaza vectorul cu distantele de la sursa la fiecare varf
    printSolution(dist, g->V);

    for(i = 0; i < g->V; i++) // ex 5
        if(strcmp("Constanta", table[i]) == 0)
        {
            FILE *f;

            f = fopen("ruta.txt", "wt");

            fprintf(f, "%d", dist[i]);

            fclose(f);
        }
// exercitiul 6 --------------------------------------------------------------
    // printez cel mai lung drum de la sursa 
    for(i = 0; i < g->V; i++) 
        if(dist[i] > mx)
        { 
            mx = dist[i]; 
            strcpy(statie, table[i]);
            u=i;
        }

    FILE *f;
    f = fopen("departe.txt", "wt");
    fprintf(f, "%d\n", mx);
    while(u>=0)
    {
        fprintf(f, "%s\n", table[u]);
        u=parrent[u];
    }

    fclose(f);
// ---------------------------------------------------------------------------

} //Complexitatea O(V^2) respectiv O(VxE) pentru reprezentarea cu lista de adiacenta

void print_all_paths(Graph *g, int source, int dest, char **table)
{
    int *visited = calloc(g->V * g->V, sizeof(int));
    int *path = calloc(g->V * g->V, sizeof(int));
    int poz = 0;

    FILE *f = fopen("bucuresti_oradea.txt","wt");

    dfs(f, g, source, dest, poz, visited, path, table);
    free(visited);
    free(path);

    fclose(f);
}

void dfs(FILE *f, Graph *g, int source, int dest, int poz, int *visited, int *path, char **table)
{
    visited[source] = 1;
    path[poz] = source;
    poz++;

    if(source == dest)
    {
        int i;
        for(i = 0; i < poz; i++)
        {
            fprintf(f, "%s\n", table[path[i]]);
        }

        fprintf(f, "\n");
    }
    else
    {
        int i;
        for(i = 0; i < g->V; i++)
        {
            if(g->a[source][i] == 1 && visited[i] == 0)
            {
                dfs(f, g, i, dest, poz, visited, path, table);
            }
        }
    }

    visited[source] = 0;
    poz--;

}
