#!/usr/bin/python

import multiprocessing
import numpy as np
import mkcells
import ctypes
import time

def cartesian(arrays, out=None):
    """
    http://stackoverflow.com/questions/1208118/using-numpy-to-build-an-array-of-all-combinations-of-two-arrays/1235363#1235363
    """

    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in range(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    return out

def span(data):
    eps = 0.5
    sigma = 0.1

    g = []

    for i in range(data.shape[1]):
        x = data[:, i].max() - data[:, i].min()
        if x == 0:
            g += [[data[0, i], data[0, i] * (1+eps)]]
            continue

        m = np.ceil(np.log2(x / sigma) / np.log2(1 + eps))
        if m < 2:
            g += [[data[:, i].min(), data[:, i].max() * (1+eps)]]
            continue

        r = np.power(1 + eps, np.arange(m))
        r = r - r.min() + data[:, i].min()
        g += [r]

    return g

def grid(data):
    G = cartesian(span(data))

    C = cartesian([range(G.shape[0]), range(G.shape[0])])
    C = C[C[:, 0] < C[:, 1], :]
    A = np.array([G[C[:, 0], :], G[C[:, 1], :]])
    
    L = G[C[:, 0], :]
    R = G[C[:, 1], :]

    F = (L < R).all(1)
    L = L[F, :]
    R = R[F, :]

    return L, R

def sensitivity(data):
    L, R = grid(data)

    center = np.empty((L.shape[0], data.shape[1]))
    cost = np.zeros((L.shape[0],))

    for i in range(L.shape[0]):
        count = 0
        
        for j in range(data.shape[0]):
            p = data[j, :]
            if (p >= R[i, :]).any() or (p < L[i, :]).any():
                continue
            center[i, :] += p
            count += 1
        
        if count == 0:
            continue

        center[i, :] /= count

        for j in range(data.shape[0]):
            p = data[j, :]
            if (p >= R[i, :]).any() or (p < L[i, :]).any():
                continue
            cost[i] += ((p - center[i, :]) ** 2).sum()

    s = np.zeros((data.shape[0],))

    for j in range(data.shape[0]):
        p = data[j, :]
        for i in range(L.shape[0]):
            if (cost[i] == 0 or p >= R[i, :]).any() or (p < L[i, :]).any():
                continue
            s[j] += ((p - center[i]) ** 2).sum() / cost[i]
    
    return s

def sample(data, size):
    assert(0 <= size <= data.shape[0])

    data = np.array(data, dtype=np.double)

    s = sensitivity(data)

    if s.sum() == 0:
        return data[:size, :], np.ones((size,)) / size
    s = s / s.sum()

    i = np.random.choice(np.arange(data.shape[0]), size, p = s)
    data = data[i, :]
    w = 1 / s[i]

    return data, w

def main():
    # i = 4
    # while np.ceil(np.power(np.log2(i), 2 * 3)) > i:
    #     i *= 2
    # print i
    data = np.random.rand(10000, 3)
    size = np.ceil(np.power(np.log2(data.shape[0]), 2 * data.shape[1]));
    size = min(max(size, 1), data.shape[0])
    sample(data, size)

if __name__ == "__main__":
    tic = time.clock()
    main()
    toc = time.clock()
    print(toc - tic)
