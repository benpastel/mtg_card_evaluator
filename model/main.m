% This script trains models on the input files and prints error stats.

% send output to screen without buffering
% so that we see the disp before a long computation
% this is the default in Matlab but not octave
more off;

% attempt to set directory to toplevel so we can find the data files
path = strsplit(pwd, '/');
if strcmp(path(end), 'model')
    cd ..
end
disp('loading data');
X = load('data/feature_matrix.txt');
Y = load('data/price_vector.txt');

[m, n] = size(X);

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

%disp('running regressions');
%tau = 14;
%llw_size = test_size;
%predicted_Y_weighted = zeros(llw_size,1);
%for i = 1:llw_size
%  [theta_weighted, ~] = locally_weighted_linear_regression(X_train,Y_train,X_test(i,:),tau);
%  predicted_Y_weighted(i,1) = [1 X_test(i,:)] * theta_weighted;
%end
%rmse_weighted = sqrt(sum((predicted_Y_weighted - Y_test(1:llw_size)).^2) / llw_size)
%rmse_test_restrict = sqrt(sum((predicted_y_test(1:llw_size) - Y_test(1:llw_size)).^2) / llw_size)

disp('running regressions');
X_random = rand(m, n);
[theta_random, rmse_random] = linear_regression(X_random, Y);
[~, rmse_half] = linear_regression(X(1:half,:), Y(1:half,:));
[theta_full, rmse_full] = linear_regression(X, Y);
[theta, rmse_train] = linear_regression(X_train, Y_train);

predicted_y_test = [ones(test_size, 1), X_test] * theta;
rmse_test = sqrt(sum((predicted_y_test - Y_test).^2) / test_size);

predicted_y_train = [ones(train_size, 1), X_train] * theta;

predicted_y_random = [ones(m, 1), X_random] * theta_random;


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
fprintf('\t %0.2f%% percent testing error improvement over random\n', ...
    (rmse_random - rmse_test) / rmse_random * 100);
fprintf('\t %0.2f%% percent training error improvement over random\n', ...
    (rmse_random - rmse_train) / rmse_random * 100);

dlmwrite('data/theta.csv', theta_full, 'delimiter', '\n', 'precision', 4);
disp('done');

scatter(predicted_y_random, Y, 'r'); hold on;
scatter(predicted_y_train, Y_train, 'g'); hold on;
scatter(predicted_y_test, Y_test, 'b'); hold on;
plot(-4:6,-4:6,'g');
title('\fontsize{24}Log-price prediction: Random vs. Model')
xlabel('\fontsize{20}\theta^Tx (predicted log-price)')
ylabel('\fontsize{20}y (actual log-price)')
legend('\fontsize{16}Random','\fontsize{16}Train','\fontsize{16}Test')
set(gca,'fontsize',16)

count = 0;
for i = 1:train_size
  if predicted_y_train(i) <= 1 && Y_train(i) <= 1
    count = count + 1;
  end
  if predicted_y_train(i) > 1 && Y_train(i) > 1
    count = count + 1;
  end
end
count / train_size

count = 0;
for i = 1:test_size
  if predicted_y_test(i) <= 1 && Y_test(i) <= 1
    count = count + 1;
  end
  if predicted_y_test(i) > 1 && Y_test(i) > 1
    count = count + 1;
  end
end
count / test_size

count = 0;
for i = 1:m
  if Y(i) <= 1
    count = count + 1;
  end
end
count/m

count = 0;
for i = 1:m
  if rand() < .92058
    if Y(i) <= 1
      count = count + 1;
    end
  end
end
count/m
