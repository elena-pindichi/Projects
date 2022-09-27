#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <limits.h>
#include "functii.h"

int main()
{
    FILE *f, *g;
    Graph *orientat = NULL, *neorientat = NULL, *distante = NULL;
    char nume[LUNG], **table = NULL;
    int n = 0, source, dest, **dist = NULL, **next = NULL, mx = 0, poz1 = 0, poz2 = 0;
    long long cost = 0;


    orientat = create();
    neorientat = create();
    distante = create();

    f = fopen("_all_files.txt", "rt");

    while(fgets(nume, LUNG, f))
    {   
        nume[strlen(nume) - 1] = 0;
        g = fopen(nume, "rt");
        if(g == NULL)
        {
            printf("Nu am putut deschide fisierul:( %s\n", nume);
            exit(1);
        }
        citire(g, orientat, neorientat, distante, &n, &table);
        fclose(g);
    }

    fclose(f);

    for(int i = 0; i < n; i++)
    {
        if(strcmp(table[i], "Bucuresti Nord") == 0)
        {
            source = i; // retinem pozitia sursei Bucuresti Nord
            break;
        }
    }

    for(int i = 0; i < n; i++)
    {
        if(strcmp(table[i], "Oradea") == 0)
        {
            dest = i; // retinem pozitia statiei Oradea
            break;
        }
    }

    cautare(distante, n, table);

    total(distante, n);

    dijkstra(distante, source, table);

    // print_all_paths(neorientat, source, dest, table);

    // Floyd - Warshall

    dist = (int**)malloc(sizeof(int*) * n);  // initializam matricea dist
    for(int i = 0; i < n; i++)
    {
        dist[i] = (int *)malloc(n * sizeof(int));
    }

    next = (int**)malloc(sizeof(int*) * n);  // initializam matricea dist
    for(int i = 0; i < n; i++)
    {
        next[i] = (int *)malloc(n * sizeof(int));
    }

    for(int i = 0; i < n; i++)
        for(int j = 0; j < n; j++)
        {
            if(neorientat->a[i][j] == 1)
            {
                dist[i][j] = distante->a[i][j];
                next[i][j] = j;
            }
            else
            {
                dist[i][j] = INT_MAX;
                next[i][j] = -1;
            }
        }
    
    for(int i = 0; i < n; i++) 
        dist[i][i] = 0;

    for(int k = 0; k < n; k++)
    {
        for(int i = 0; i < n; i++)
        {
            for(int j = 0; j < n; j++)
            {
                if(dist[i][k] != INT_MAX && dist[k][j] != INT_MAX)
                {
                    cost = dist[i][k] + dist[k][j];
                    if(cost < dist[i][j])
                    {
                     dist[i][j] = cost;
                     next[i][j] = next[i][k];
                    }
                }
            }
        }
    }

    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < n; j++)
        {
            if(dist[i][j] > mx)
            {
                mx = dist[i][j];
                poz1 = i;
                poz2 = j;
            }
        }
    }

    f = fopen("drum_lung.txt", "wt");
    fprintf(f, "%s %s %d", table[poz1], table[poz2], mx);
    fclose(f);

    return 0;
}