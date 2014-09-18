#!/usr/bin/python

from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import numpy as np
import time

import grid

D = 5

def main():
    # Create a random dataset
    rng = np.random.RandomState(1)
    x = np.sort(5 * rng.rand(64 * 4, 1), axis=0)
    y = np.sin(x).ravel()
    y[::64] += 3 * (0.5 - rng.rand(4))

    data = np.array([x, y]).transpose()
    size = int(np.log2(data.shape[0])) ** 2

    data, w = grid.sample(data, size)
    x_1, y_1 = data[:, 0].reshape((size, 1)), data[:, 1].reshape((size, 1))

    i = range(size)
    i = np.random.choice(i, size)
    x_2, y_2 = x[i], y[i]

    clf_1 = DecisionTreeRegressor(max_depth=D)
    clf_1.fit(x_1, y_1, sample_weight=w)

    clf_2 = DecisionTreeRegressor(max_depth=D)
    clf_2.fit(x_2, y_2)

    # Predict
    X_test = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]
    y_1 = clf_1.predict(X_test)
    y_2 = clf_2.predict(X_test)

    # Plot the results
    plt.figure()
    plt.scatter(x, y, c="k", label="data")
    plt.plot(X_test, y_1, c="g", label="coreset", linewidth=2)
    plt.plot(X_test, y_2, c="r", label="random", linewidth=2)
    plt.xlabel("data")
    plt.ylabel("target")
    plt.title("Decision Tree Regression")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
