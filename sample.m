function [i, w] = sample(data, sz, epsil, sigma)
    [L, R] = grid(data, epsil, sigma);
    s = javaSens(L, R, data);
    
    sm = sum(s);
    if sm == 0
        i = 1:sz;
        w = ones(sz, 1) ./ sz;
        return;
    end

    p = s ./ sm;
    i = randsample(numel(p), sz, true, p);
    w = 1 ./ s(i);
end

function ans = cartesian(xy)
    % From http://pastebin.com/DXz25c2P
    if numel(xy) < 1
        ans = [];
        return;
    end

    x = xy{1};
    x = x(:);
    if numel(xy) == 1
        ans = x;
        return;
    end

    y = xy(2:end);
    y = cartesian(y);
       
    nx = size(x, 1);
    ny = size(y, 1);
    rx = repmat(x.', ny, 1);
    ry = repmat(y, nx, 1);
    ans = [rx(:), ry];
end

function g = span(data, epsil, sigma)
    g = {};

    for i=1:size(data, 2)
        x = max(data(:, i)) - min(data(:, i));
        if x == 0
            g{numel(g)+1} = [data(1, i), data(1, i) * (1+epsil)];
            continue;
        end

        m = ceil(log(x / sigma) / log(1+epsil));
        if m < 2
            g{numel(g)+1} = [min(data(:, i)), max(data(:, i)) .* (1+epsil)];
            continue;
        end

        r = (1+epsil) .^ (0:m);
        r = r - min(r) + min(data(:, i));
        g{numel(g)+1} = r;
    end
end

function [L, R] = grid(data, epsil, sigma)
    axes = span(data, epsil, sigma);
    G = cartesian(axes);
    C = cartesian({1:size(G, 1), 1:size(G, 1)});
    C = C(C(:, 1) < C(:, 2), :);
    
    L = G(C(:, 1), :);
    R = G(C(:, 2), :);
    
    A = all(L < R, 2);
    L = L(A, :);
    R = R(A, :);
end

function s = javaSens(L, R, data)
    % The next code loads Java class Sensitivity. To make it work
    % you should:
    % 1. Compile Sensitivity.java class with:
    %      # javac Sensitivity.java 
    % 2. Make sure that Matlab runs the same Java version as javac.
    %      # javac -version
    %     >> version -java % in matlab
    % 3. Add the directory with Sensitivity.class to Matlab's Java
    %    classpath:
    %      # javaaddpath('path-to-your-directory')
    if ~exist('Sensitivity', 'class')
        error('Sensitivity class not found. Please add it to your classpath.');
    end
    assert(size(L, 1) > 0 && size(R, 1) > 0 && size(data, 1) > 0);
    assert(size(L, 2) == size(R, 2) && size(R, 2) == size(data, 2));
    o = Sensitivity;
    s = o.calculate(data, L, R);
end

% function s = cSens(L, R, data)
%     % The next code executes c sensitivity program. To make it work
% 
%     % 1. Compile sensitivity.c with any compiler which supports c99. Make sure
%     %    MATLAB is defined (run the compiler with -DMATLAB).
%     % 2. Define in Matlab command line a global variable with the path to the
%     %    compiled executable:
%     %     >> global SensitivityExecutable
%     %     >> SensitivityExecutable = 'path-to-the-compiled-executable'
%     if ~exist('SensitivityExecutable', 'var')
%         error('SensitivityExecutable global variable is not defined');
%     end
%     n = size(data, 1);
%     m = size(L, 1);
%     a = size(R, 2);
% 
%     LR = [L'; R']';
%     LR = LR(:);
%     data = data(:);
% 
%     p = Process(SensitivityExecutable);
%     p.write(sprintf('POINTS %u CELLS %u AXES %u\n', n, m, a));
%     p.write(num2hex(data));
%     p.write(num2hex(LR));
% 
%     s = hex2num(strsplit(p.read(), '\n'));
% 
%     if p.wait() ~= 0
%         error('Sensitivity process terminated unexpectedly');
%     end
% end
