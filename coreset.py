#!/usr/bin/python

import multiprocessing
import numpy as np
import mkcells
import ctypes
import time

def make_cells(data, axis):
    doubleptr = ctypes.POINTER(ctypes.c_double)
    usizeptr = ctypes.POINTER(ctypes.c_size_t)

    d = data.ctypes.data_as(doubleptr)
    n, dims = data.shape
    mid = mkcells.make(dims, n, axis, d)
    if mid == 0:
        raise Exception("Failed making cells")

    m = mkcells.number(mid)
    argcells = np.empty(m, dtype=np.uintp)
    d = argcells.ctypes.data_as(usizeptr)
    mkcells.argcells(mid, d)
    mkcells.destroy(mid)

    return argcells

def merge(a, b):
    # http://stackoverflow.com/questions/12427146/combine-two-arrays-and-sort
    c = np.concatenate((a, b))
    c.sort(kind='mergesort')
    flag = np.ones(len(c), dtype=bool)
    np.not_equal(c[1:], c[:-1], out=flag[1:])

    return c[flag]

def split(data, axis):
    n = data.shape[0]
    sort = data[:, axis].argsort()
    rsort = sort[::-1]
    ltr = make_cells(data[sort, :], axis)
    rtl = make_cells(data[rsort, :], axis)
    rtl = np.subtract(n - 1, rtl)[::-1]
    r = merge(ltr, rtl)
    cells = np.split(data, r)

    return [c for c in cells if c.size > 0]

def sample(data, extracols):
    assert(data.shape[0] > 0)
    m = data[:, :-extracols]
    rows = int(np.ceil(np.log(m.shape[0])))

    m = ((m - m.mean(0)) ** 2).sum(1)
    s = m.sum()
    a = np.arange(m.shape[0])
    if s == 0: 
        return data[:rows, :]

    p = m / s
    i = np.random.choice(a, rows, p = p)
    data[i, -1] = 1.0 / p[i]

    avg = np.reshape(data.mean(0), [1, data.shape[1]])
    avg[0, -1] = 1024 ** 2
    data = data[i, :]
    return np.append(data, avg, axis=0)

def coreset(data, depth, axis=0):

    extracols = 1

    if data.shape[0] < 2:
        return data
    if depth == 0:
        return sample(data, extracols)

    cells = split(data, axis)
    axis = (axis + 1) % (data.shape[1] - extracols)
    depth = depth - 1

    points = [coreset(cell, depth, axis) for cell in cells]
    return np.concatenate(points)

def create(data, target, depth):

    if target.size == 0:
        return np.array(), np.array()
    if target.size == 1:
        data = data.reshape(1, data.size)

    dims = data.shape[1]
    target = target.reshape(target.size, 1)
    
    # Append Target
    data = np.asarray(np.append(data, target, 1))
    # Append weights
    data = np.asarray(np.append(data, np.ones([target.size, 1]), 1))

    assert(len(data.shape) > 1 and data.shape[1] != 0)
    assert(data.dtype == np.double)
    assert(depth >= 0)

    data = coreset(data, depth, dims)

    return data[:, :-2], data[:, -2], data[:, -1]

def main():
    data = np.matrix('3 1 1', dtype=np.double)
    target = np.array([1])
    make_cells(data, 0);
    create(data, target, 1)

if __name__ == "__main__":
    tic = time.clock()
    main()
    toc = time.clock()
    print(toc - tic)
