% So far, this just trains a linear model on the input files
% and prints some stats about it
%
% The input files can be in any format 'load' can read
% e.g. space-separated floats with one training example per line.

X_path = '../data/feature_matrix.txt';

X = load(X_path);

disp('generating random Y');
% Y is random until we have price data
Y = rand(size(X, 1), 1);

disp('running linear regression');
[theta, rmse] = linear_regression(X, Y);
disp('done');

