#!/usr/bin/python

from sklearn.datasets import load_iris
from sklearn import tree
import numpy as np
import time

import coreset

def assertsubset(data0, target0, data, target):
    for j in range(target0.size):
        found = False
        for i in range(len(target)):
            if np.array_equal(data0[j, :], data[i, :]):
                assert(target[i] == target0[j])
                found = True
                break
        assert(found)

def main():
    TestPart = 0.1

    iris = load_iris()
    n = iris.target.size

    ntest = int(round(TestPart * n))
    test = np.random.permutation(n)[:ntest]
    train = [i for i in range(n) if i not in test]

    data = iris.data[train, :]
    target = iris.target[train]

    test_data = iris.data[test, :]
    test_target = iris.target[test]

    data, target, weight = coreset.create(data, target, 2)

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(data, target)

    e = clf.predict(test_data) - test_target
    print(e)

if __name__ == "__main__":
    tic = time.clock()
    main()
    toc = time.clock()
    print(toc - tic)
