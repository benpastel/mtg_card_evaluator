% This script trains models on the input files and prints error stats.

% send output to screen without buffering
% so that we see the disp before a long computation
% this is the default in Matlab but not octave
more off;

% attempt to set directory to toplevel so we can find the data files
path = strsplit(pwd, '/');
if strcmp(path(end), 'model') || strcmp(path(end), 'data')
    cd ..
end
disp('loading data');
X = load('data/feature_matrix.txt');
Y = load('data/price_vector.txt');

disp('preparing data');
[m, n] = size(X);
X = [ones(m, 1) X]; % prepend intercept terms
n = n+1;

large_Y = ((Y'>5)&(Y'<300))';
Y = log(Y);
X_large = X(large_Y,:);
Y_large = Y(large_Y);

% split into training & test sets
train_size = floor(m * .9);
half = floor(m * .5);
test_size = m - train_size;
X_train = X(1:train_size,:);
Y_train = Y(1:train_size);
X_test = X(train_size+1:m,:);
Y_test = Y(train_size+1:m);

disp('running regressions');
X_random = rand(m, n);
[theta_random, rmse_random] = linear_regression(X_random, Y);
[~, rmse_half] = linear_regression(X(1:half,:), Y(1:half,:));
[theta_full, rmse_full] = linear_regression(X, Y);
[theta, rmse_train] = linear_regression(X_train, Y_train);

predicted_y_test = X_test * theta;
predicted_y_train = X_train * theta;
predicted_y_large = X_large * theta;
predicted_y_random = X_random * theta_random;

find_rmse = @(predicted, actual) ...
    sqrt(sum((predicted - actual).^2) / length(actual));

rmse_test = find_rmse(predicted_y_test, Y_test);
rmse_large = find_rmse(predicted_y_large, Y_large);

disp('RMSEs:');
fprintf('\t %0.3f training on random\n', rmse_random);
fprintf('\t %0.3f training on 50%%\n', rmse_half);
fprintf('\t %0.3f training on 90%%\n', rmse_train);
fprintf('\t %0.3f training on full data\n', rmse_full);
fprintf('\t %0.3f testing on 10%%\n', rmse_test);
fprintf('\t %0.3f training on 90%%, counting error on large data only\n', rmse_large);
fprintf('\t %0.2f%% percent testing error improvement over random features\n', ...
    (rmse_random - rmse_test) / rmse_random * 100);
fprintf('\t %0.2f%% percent training error improvement over random features\n', ...
    (rmse_random - rmse_train) / rmse_random * 100);

cd data/ % workaround for strange permissions bug
dlmwrite('theta.csv', theta_full, 'delimiter', '\n', 'precision', 4);
cd ..
disp('Wrote thetas to file. Match them up with feature names like this:')
fprintf('\t data/theta.csv data/feature_names.txt | sort -g -k1 \n');

disp('plotting results');
scatter(predicted_y_random, Y, 'r'); hold on;
scatter(predicted_y_train, Y_train, 'g'); hold on;
scatter(predicted_y_test, Y_test, 'b'); hold on;
plot(-4:6,-4:6,'g');
title('\fontsize{24}Log-price prediction: Random vs. Model')
xlabel('\fontsize{20}\theta^Tx (predicted log-price)')
ylabel('\fontsize{20}y (actual log-price)')
legend('\fontsize{16}Random','\fontsize{16}Train','\fontsize{16}Test')
set(gca,'fontsize',16)
disp('done');
