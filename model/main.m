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
rmse_for_random
rmse
percent_improvement = (rmse_for_random - rmse) / rmse_for_random * 100

sample_size = size(X,1)
train_size = floor(sample_size * .9)
test_size = sample_size - train_size
X_train = X(1:train_size,:);
Y_train = Y(1:train_size);
X_test = X(train_size+1:sample_size,:);
Y_test = Y(train_size+1:sample_size);

[theta, rmse_train] = linear_regression(X_train, Y_train);
rmse_train
X_test = [ones(test_size, 1), X_test];
predicted_y_test = X_test * theta;
rmse_test = sqrt(sum((predicted_y_test - Y_test).^2) / test_size)

disp('done');



