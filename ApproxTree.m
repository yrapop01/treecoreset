classdef ApproxTree
    % Matlab wrapper for Approx Java Class.
    %
    % Note: this code loads Java class Approx. To make it work
    % you should:
    % 1. Compile Approx.java class with:
    %      # javac Approx.java 
    % 2. Make sure that Matlab runs the same Java version as javac.
    %      # javac -version # in shell
    %     >> version -java  % in matlab
    % 3. Add the directory with Approx.class to Matlab's Java
    %    classpath:
    %     >> javaaddpath('path-to-your-directory')
    %
    % Usage example:
    %   >> load carsmall;
    %   >> x = [Cylinders Weight];
    %   >> tree = ApproxTree(x, MPG, 5);
    %   >> tree.predict([2202 4])
    %   >> tree.plot()


    properties
        tree % Java Approx class object
        dims % Approximated data dimensiality
    end

    methods
        function obj = ApproxTree(x, y, h)
        % Approximate data using decision tree.
        % Parameters:
        %   x: NxM data matrix
        %   y: Nx1 target values vector
        %   h: tree height (scalar)
        % Return:
        %   tree: object to be used by Approx.predict(,), for data values x
        %         call y = Approx.predix(tree, x) are the prdicted target values.
        % Usage:
        %   >> tree = ApproxTree(0:0.5:pi, sin(0:0.5:pi), 4);
        %   >> x = 0:02:pi;
        %   >> y = tree.predict(x);
        %   >>
        %   >> figure;
        %   >> plot(0:0.5:pi, sin(0:0.5:pi), 'Color', 'r'); hold on;
        %   >> scatter(x, y, 'Color', 'g');

            if ~exist('Approx', 'class')
                error(['Approx class not found. ' ... 
                       'Please add it to your classpath. ', ...
                       'Type `help ApproxTree` for more info.']);
            end
            
            % Rearrange the data before calling Approx methods.
            if size(x, 1) == 1 
                data = [x(:), y(:)];
            else
                data = [x, y(:)];
            end

            % Store dimensiality.
            obj.dims = size(data, 2) - 1;

            % Get the tree.
            obj.tree = Approx.fit(data, obj.dims, h);
        end

        function y = predict(tree, x)
        % Predict target values using the approximated tree.
        % Parameters:
        %   x: NxM data matrix
        %   h: tree height (scalar)
        % Return:
        %   y: Nx1 target values vector
        % Usage:
        %   >> tree = ApproxTree(0:0.5:pi, sin(0:0.5:pi), 4);
        %   >> x = 0:02:pi;
        %   >> y = tree.predict(x);
        %   >>
        %   >> figure;
        %   >> plot(0:0.5:pi, sin(0:0.5:pi), 'Color', 'r'); hold on;
        %   >> scatter(x, y, 'Color', 'g');

             if size(x, 2) ~= tree.dims
                 error('Used data with different dimensions number for prediction');
             end
             y = Approx.predict(tree.tree, x);
        end

        function plot(tree)
        % Draw tree with thresholds info,

            Approx.prn(tree.tree);
            nodes = tree.tree.printParents;
            labels = tree.tree.printLabels;

            nodes = double(nodes(:))';
            s = {};
            for i=1:numel(nodes)
                s{numel(s)+1} = char(labels(i));
            end

            treeplot(nodes);
            [x, y] = treelayout(nodes);
            text(x(:)+0.02, y(:), s);
        end
    end
end
