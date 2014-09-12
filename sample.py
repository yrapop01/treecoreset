#!/usr/bin/python

from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import numpy as np
import time

import coreset

def main():
    # Create a random dataset
    rng = np.random.RandomState(1)
    X = np.sort(5 * rng.rand(80, 1), axis=0)
    y = np.sin(X).ravel()
    y[::5] += 3 * (0.5 - rng.rand(16))

    clf_1 = DecisionTreeRegressor(max_depth=2)
    clf_2 = DecisionTreeRegressor(max_depth=5)
    clf_1.fit(X, y)
    clf_2.fit(X, y)

    # Predict
    X_test = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]
    y_1 = clf_1.predict(X_test)
    y_2 = clf_2.predict(X_test)

    # Plot the results
    plt.figure()
    plt.scatter(X, y, c="k", label="data")
    plt.plot(X_test, y_1, c="g", label="max_depth=2", linewidth=2)
    plt.plot(X_test, y_2, c="r", label="max_depth=5", linewidth=2)
    plt.xlabel("data")
    plt.ylabel("target")
    plt.title("Decision Tree Regression")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
