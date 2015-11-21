% So far, this just trains a linear model on the input files
% and prints some stats about it
%
% The input files can be in any format 'load' can read
% e.g. space-separated floats with one training example per line.

disp('loading data');
X = load('data/feature_matrix.txt');
Y = load('data/price_vector.txt');

% positive_features = all(X' > 0)';
% X = X(positive_features, :);
% Y = Y(positive_features);
large_Y = (Y' > 100)';
X_large = X(large_Y,:);
Y_large = log(Y(large_Y));
Y = log(Y);

[m, n] = size(X);

% split into training & test sets
train_size = floor(m * .9);
half = floor(m * .5);
test_size = m - train_size;
X_train = X(1:train_size,:);
Y_train = Y(1:train_size);
X_test = X(train_size+1:m,:);
Y_test = Y(train_size+1:m);

disp('running regressions');
[~, rmse_random] = linear_regression(rand(m, n), Y);
[~, rmse_half] = linear_regression(X(1:half,:), Y(1:half,:));
[~, rmse_full] = linear_regression(X, Y);
[theta, rmse_train] = linear_regression(X_train, Y_train);

predicted_y_test = [ones(test_size, 1), X_test] * theta;
rmse_test = sqrt(sum((predicted_y_test - Y_test).^2) / test_size);

predicted_y_large_test = [ones(size(X_large,1), 1), X_large] * theta;
rmse_large = sqrt(sum((predicted_y_large_test - Y_large).^2) / size(X_large,1));

disp('RMSEs:');
fprintf('\t %0.3f training on random\n', rmse_random);
fprintf('\t %0.3f training on 50%%\n', rmse_half);
fprintf('\t %0.3f training on 90%%\n', rmse_train);
fprintf('\t %0.3f training on full data\n', rmse_full);
fprintf('\t %0.3f testing on 10%%\n', rmse_test);
fprintf('\t %0.3f training on 90%%, counting error on large data only\n', rmse_large);
fprintf('\t %0.2f%% percent training error improvement over random\n', ...
    (rmse_random - rmse_full) / rmse_random * 100);

[~, ranked_features] = sort(theta, 'descend');
scatter(X(:,3),Y); hold on;
xlabel('best feature')
ylabel('log(price)');
t = 0:20;
k = theta(1) + theta(ranked_features(1))*t;
plot(t, k, 'r')
disp('done');



