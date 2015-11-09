% So far, this just trains a linear model on the input files
% and prints some stats about it
%
% The input files can be in any format 'load' can read
% e.g. space-separated floats with one training example per line.

disp('loading data');
raw_X = load('../data/feature_matrix.txt');
  
id_price = load('../data/id_price.dat');
id_featureidx = load('../data/id_featureidx.dat');
 
% match prices to features whenever they share a multiverseid.
%
% NOTE: cards that have multiple multiverseids will be repeated; we should 
% consider something smarter like averaging the prices.
[~, idx1, idx2] = intersect(id_price(:, 1), id_featureidx(:, 1));
Y = id_price(idx1, 2);
feature_indices = id_featureidx(idx2, 2);
X = raw_X(feature_indices, :);

disp('finding baseline');
rand_X = rand(size(X, 1), size(X, 2));
[~, rmse_for_random] = linear_regression(rand_X, Y)

disp('running linear regression');
[~, rmse] = linear_regression(X, Y)
disp('done');



