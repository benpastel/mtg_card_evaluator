% So far, this just trains a linear model on the input files
% and prints some stats about it
%
% The input files can be in any format 'load' can read
% e.g. space-separated floats with one training example per line.

disp('loading data');
X = load('data/feature_matrix.txt');
Y = log(load('data/price_vector.txt'));
       
[m, ~] = size(X);
order = randperm(m);
X = X(order, :);
Y = Y(order);

% prepend intercepts
X = [ones(m, 1), X];

disp('training');
train_m = floor(m * 0.9);

trials = 15;
test_rmses = [];
train_rmses = [];
sizes = linspace(4000, train_m, trials);
trial = 1;
for use_m = sizes    
    X_test = X(train_m+1:m,:);
    Y_test = Y(train_m+1:m);
    
    X_train = X(1:floor(use_m),:);
    Y_train = Y(1:floor(use_m));
    
    [theta, train_rmse] = linear_regression(X_train, Y_train);
    predicted = X_test * theta;
    test_rmse = sqrt(sum((predicted - Y_test).^2) / length(Y_test));
    test_rmses = [test_rmses test_rmse];
    train_rmses = [train_rmses train_rmse];
end
hold on;
ylabel('RMSE');
xlabel('m');
plot(sizes, test_rmses);
plot(sizes, train_rmses);
legend('test', 'train');

