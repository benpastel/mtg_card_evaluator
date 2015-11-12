% So far, this just trains a linear model on the input files
% and prints some stats about it
%
% The input files can be in any format 'load' can read
% e.g. space-separated floats with one training example per line.

disp('loading data');
X = load('../data/feature_matrix.txt');
Y = load('../data/price_vector.txt');

positive_features = all(X' > 0)';
X = X(positive_features, :);
Y = log(Y(positive_features));

disp('finding baseline');
rand_X = rand(size(X, 1), size(X, 2));
[~, rmse_for_random] = linear_regression(rand_X, Y);

disp('running linear regression');
[theta, rmse] = linear_regression(X, Y);

percent_improvement = (rmse_for_random - rmse) / rmse_for_random * 100

disp('done');



