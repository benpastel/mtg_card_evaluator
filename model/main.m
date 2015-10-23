function [] = main( X_path, Y_path )
%MAIN
% So far, this just trains a linear model on the input files
% and prints some stats about it
%
% The input files can be in any format 'load' can read
% e.g. space-separated floats with one training example per line.

    X = load(X_path);
    Y = load(Y_path);

    [theta, rmse] = linear_regression(X, Y)
end

