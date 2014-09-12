#ifndef _MKCELLS_H_
#define _MKCELLS_H_

typedef size_t index_t;

size_t make(size_t dims, size_t n, size_t axis, double *data);
size_t number(size_t id);
void cells(size_t id, double *cells);
void argcells(size_t id, index_t *cells);
void destroy(size_t id);

#endif
