% So far, this just trains a linear model on the input files
% and prints some stats about it
%
% The input files can be in any format 'load' can read
% e.g. space-separated floats with one training example per line.

disp('loading data');
X = load('data/feature_matrix.txt');
Y = load('data/price_vector.txt');

disp('finding baseline');
rand_X = rand(size(X, 1), size(X, 2));
[~, rmse_for_random] = linear_regression(rand_X, Y)

disp('running linear regression');
[~, rmse] = linear_regression(X, Y)
disp('done');



