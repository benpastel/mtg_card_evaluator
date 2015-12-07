% So far, this just trains a linear model on the input files
% and prints some stats about it
%
% The input files can be in any format 'load' can read
% e.g. space-separated floats with one training example per line.

disp('loading data');
fflush(stdout);
X = load('../data/feature_matrix.txt');
Y = load('../data/price_vector.txt');

large_Y = ((Y'>5)&(Y'<300))';
Y = log(Y);
X_large = X(large_Y,:);
Y_large = Y(large_Y);

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
%tau = 100000;
%[theta_weighted, ~] = locally_weighted_linear_regression(X_train,Y_train,X_test(1,:),tau);
%predicted_Y_weighted = zeros(test_size,1);
%for i = 1:test_size
%  [theta_weighted, ~] = locally_weighted_linear_regression(X_train,Y_train,X_test(i,:),tau);
%  predicted_Y_weighted(i,1) = [1 X_test(i,:)] * theta_weighted;
%end
%rmse_weighted = sqrt(sum((predicted_Y_weighted - Y_test).^2) / test_size)

[~, rmse_random] = bayes_linear_regression(rand(m, n), Y);
[~, rmse_half] = bayes_linear_regression(X(1:half,:), Y(1:half,:));
[theta_full, rmse_full] = bayes_linear_regression(X, Y);
[theta, rmse_train] = bayes_linear_regression(X_train, Y_train);

predicted_y_test = [ones(test_size, 1), X_test] * theta;
rmse_test = sqrt(sum((predicted_y_test - Y_test).^2) / test_size);

predicted_y_large_test = [ones(size(X_large,1), 1), X_large] * theta;
rmse_large = sqrt(sum((predicted_y_large_test - Y_large).^2) / size(X_large,1));

%A = [Y_large abs(predicted_y_large_test-Y_large)];
%B = sortrows(A);
%scatter(B(:,1), B(:,2))

disp('RMSEs:');
fprintf('\t %0.3f training on random\n', rmse_random);
fprintf('\t %0.3f training on 50%%\n', rmse_half);
fprintf('\t %0.3f training on 90%%\n', rmse_train);
fprintf('\t %0.3f training on full data\n', rmse_full);
fprintf('\t %0.3f testing on 10%%\n', rmse_test);
fprintf('\t %0.3f training on 90%%, counting error on large data only\n', rmse_large);
fprintf('\t %0.2f%% percent training error improvement over random\n', ...
    (rmse_random - rmse_full) / rmse_random * 100);

%dlmwrite('data/theta.csv', theta_full, 'delimiter', '\n', 'precision', 4);
disp('done');



