#include <assert.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include "mkcells.h"

#define eprintf(format, ...) {\
    fprintf(stderr,"%s %s %d: ", __FILE__, __func__, __LINE__);\
    fprintf(stderr, format, ##__VA_ARGS__);\
}

#define logi(format, ...) eprintf(format, ##__VA_ARGS__)

#if NDEBUG
#define verify(cond) assert(cond)
#else
#define verify(cond) {if (!(cond)) {eprintf("verification failed\n"); exit(-1);}}
#endif

#define EPS 0.2

typedef struct {
    double *cells;
    index_t *argcells;
    size_t n;
} cells_t;

static cells_t *allocate(size_t dims, size_t n)
{
    cells_t *cells;

    cells = (cells_t *)malloc(sizeof(cells_t));
    if (!cells) {
        eprintf("Out of memory\n");
        return NULL;
    }

    cells->cells = (double *)malloc(n * sizeof(double));
    if (!cells->cells) {
        free(cells);
        eprintf("Out of memory\n");
        return NULL;
    }

    cells->argcells = (index_t *)malloc(n * sizeof(index_t));
    if (!cells->argcells) {
        free(cells->cells);
        free(cells);
        eprintf("Out of memory\n");
        return NULL;
    }

    return cells;
}

size_t make(size_t dims, size_t n, size_t axis, double *data)
{
    double t0, t1, t;
    cells_t *cells;
    int m;

    verify(data);
    verify(n);

    cells = allocate(dims, n);
    if (!cells)
        return 0;

    m = 1;
    t0 = t1 = cells->cells[0] = data[axis];
    cells->argcells[0] = 0;

    for (size_t i = 0; i < n; i++) {
        t = data[dims * i + axis];
        if (fabs(t - t1) > EPS * fabs(t1 - t0)) {
            cells->argcells[m] = i;
            cells->cells[m++] = t1 = t;
        }
    }
    
    cells->n = m;

    return (size_t)cells;
}

size_t number(size_t id)
{
    cells_t *cells = (cells_t *)id;
    return cells->n;
}

void cells(size_t id, double *cells)
{
    cells_t *c = (cells_t *)id;
    memcpy(cells, c->cells, c->n * sizeof(double));
}

void argcells(size_t id, index_t *argcells)
{
    cells_t *c = (cells_t *)id;
    memcpy(argcells, c->argcells, c->n * sizeof(index_t));
}

void destroy(size_t id)
{
    cells_t *cells = (cells_t *)id;
    
    free(cells->cells);
    free(cells);
}

