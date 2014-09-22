import java.io.InputStream;
import java.io.OutputStream;
import java.util.Scanner;
import java.nio.charset.Charset;
import java.util.Arrays;

public class Sensitivity {
    static class Cell {
        int count;
        double cost;
        double [] center;
        double [] ell;
        double [] r;
    }

    static class Point {
        double [] p;
        double s;
        double cost;
        Cell cell;
    }

    static boolean isInside(Point point, Cell cell, int a) {
        while (a-- > 0)
            if (point.p[a] >= cell.r[a] || point.p[a] < cell.ell[a])
                return false;
        return true;
    }

    static void add(double [] ell, double [] r, int a) {
        while (a-- > 0)
            ell[a] += r[a];
    }

    static void div(double [] p, double v, int a) {
        while (a-- > 0)
            p[a] /= v;
    }

    static double sqdist(double [] c, double [] p, int a) {
        double sum = 0;
    
        while (a-- > 0)
            sum += (c[a] - p[a]) * (c[a] - p[a]);

        return sum;
    }

    static void calc(int n, int m, int a, Point [] points, Cell [] cells) {
        for (int i = 0; i < m; i++) {
            Cell cell = cells[i];

            for (int j = 0; j < n; j++) {
                Point point = points[j];

                if (!isInside(point, cell, a))
                    continue;

                point.cell = cell;
                add(cell.center, point.p, a);
                cell.count++;
            }

            if (cell.count == 0)
                continue;

            div(cell.center, cell.count, a);

            for (int j = 0; j < n; j++) {
                Point point = points[j];

                if (point.cell != cell)
                    continue;

                point.cost = sqdist(cell.center, point.p, a);
                cell.cost += point.cost;
            }
        }

        for (int j = 0; j < n; j++)
            points[j].s = points[j].cost / points[j].cell.cost;
    }

    public static double[] calcAll(double [][] P, double [][] L, double [][] R) {
        return new double[10];
    }

    public static double[] calculate(double [][] P, double [][] L, double [][] R) {
        assert(P != null && L != null && R != null);
        assert(P.length > 0 && L.length > 0 && R.length == L.length &&
               P[0].length == L[0].length && L[0].length == R[0].length);

        int n = P.length;
        int m = L.length;
        int a = R[0].length;

        Cell [] cells = new Cell[m];
        Point [] points = new Point[n];

        for (int i = 0; i < n; i++) {
            points[i] = new Point();
            points[i].p = P[i];
        }

        for (int i = 0; i < m; i++) {
            cells[i] = new Cell();
            cells[i].ell = L[i];
            cells[i].r = R[i];
            cells[i].center = new double [a];
        }

        calc(n, m, a, points, cells);

        double [] s = new double[n];
        for (int i = 0; i < n; i++)
            s[i] = points[i].s;
        
        return s;
    }
}

