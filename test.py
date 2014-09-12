#!/usr/bin/python

from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import numpy as np
import time

import coreset

def main():
    # Create a random dataset
    rng = np.random.RandomState(1)
    X = np.sort(5 * rng.rand(1024 * 16, 1), axis=0)
    y = np.sin(X).ravel()
    y[::16] += 3 * (0.5 - rng.rand(1024))

    D = 2
    x_0, y_0, w_0 = coreset.create(X, y, D)

    i = np.arange(y.size)
    i = np.random.choice(i, x_0.shape[0])
    x_1, y_1 = X[i], y[i]

    clf_1 = DecisionTreeRegressor(max_depth=D)
    clf_2 = DecisionTreeRegressor(max_depth=D)
    clf_1.fit(x_0, y_0)
    clf_2.fit(x_1, y_1)

    # Predict
    X_test = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]
    y_1 = clf_1.predict(X_test)
    y_2 = clf_2.predict(X_test)

    # Plot the results
    plt.figure()
    plt.scatter(X, y, c="k", label="data")
    plt.plot(X_test, y_1, c="g", label="cft1", linewidth=2)
    plt.plot(X_test, y_2, c="r", label="cft2", linewidth=2)
    plt.xlabel("data")
    plt.ylabel("target")
    plt.title("Decision Tree Regression")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
