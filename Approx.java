import java.util.Arrays;
import java.util.Comparator;

public class Approx {
    static final int MinSearchSize = 3;

    public static class Tree {
        int axis;
        double threshold;
        double value;
        double cost;
        Tree left;
        Tree right;

        public int [] printParents;
        public String [] printLabels;
    }

    static final class Ascending implements Comparator<double[]> {
        private int axis;

        public Ascending(int axis) {
            this.axis = axis;
        }

        @Override
        public int compare(double [] a, double [] b) {
            return (int) (a[axis] - b[axis]);
        }
    }

    static double expectation(double [][] points, int axis) {
        double mu = 0;

        for (int i = 0; i < points.length; i++)
            mu += points[i][axis];

        return mu / points.length;
    }

    static double variance(double [][] points, int axis) {
        double mu = expectation(points, axis);
        double var = 0;

        for (int i = 0; i < points.length; i++) {
            double v = points[i][axis] - mu;
            var += v * v;
        }

        return var;
    }

    static double varsum(double [][] points, int a) {
        double sum = 0;

        for (int i = 0; i < a; i++)
            sum += variance(points, i);            

        return sum;
    }

    static int chooseAxis(double [][] points, int a) {
        int j = 0;
        double maxvar = variance(points, 0);

        for (int i = 1; i < a; i++) {
            double var = variance(points, i);

            if (var > maxvar) {
                maxvar = var;
                j = i;
            }
        }

        Arrays.sort(points, new Ascending(j));
        return j;
    }

    public static Tree me() {
        return new Tree();
    }

    public static Tree fit(double [][] points, int a, int h) {
        Tree tree = new Tree();
        int left = 0, right = points.length, middle = points.length / 2;

        if (h == 0 || points.length < MinSearchSize) {
            tree.axis = -1;
            tree.value = expectation(points, a);
            tree.cost = varsum(points, a);
            return tree;
        }

        tree.axis = chooseAxis(points, a);

        while (middle != left) {
            tree.left = fit(Arrays.copyOfRange(points, left, middle), a, h - 1);
            tree.right = fit(Arrays.copyOfRange(points, middle, right), a, h - 1);
            
            if (tree.left.cost == tree.right.cost)
                break;

            if (tree.left.cost < tree.right.cost)
                left = middle;
            else
                right = middle + 1;
            
            middle = (left + right) / 2;
        }

        tree.threshold = points[middle][tree.axis];
        tree.cost = tree.left.cost + tree.right.cost;
        return tree;
    }

    public static double [] predict(Tree tree, double [][] x) {
        double [] values = new double [x.length];

        for (int i = 0; i < x.length; i++) {
            Tree t = tree;

            while (t.axis >= 0)
                t = t.threshold < x[i][t.axis] ? t.left : t.right;

            values[i] = t.value;
        }

        return values;
    }

    static int size(Tree tree) {
        if (tree == null)
            return 0;
        return 1 + size(tree.left) + size(tree.right);
    }

    static int printRecurse(Tree tree, int [] parents,
        String [] labels, int parent, int i) {
        if (tree == null)
            return i;

        parents[i] = parent + 1;
        if (tree.axis >= 0)
            labels[i] = String.format("x[%d] = %f\n", tree.axis, tree.threshold);
        else
            labels[i] = String.format("y = %f\n", tree.value);

        parent = i;
        i = i + 1;

        i = printRecurse(tree.left, parents, labels, parent, i);
        i = printRecurse(tree.right, parents, labels, parent, i);

        return i;
    }


    public static void prn(Tree tree) {
        int n = size(tree);

        tree.printParents = new int [n];
        tree.printLabels = new String [n];

        printRecurse(tree, tree.printParents, tree.printLabels, -1, 0);
    }
}

