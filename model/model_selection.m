# This will perform forward search over the set of features using k-fold cross validation
# it will return the indices of the best subset of features to use.
# This works best for a small set of features and should probably exclude keyword features
function retval = model_selection(X,Y)
  retval = forward_search(X,Y,10)
endfunction

function retval = forward_search(X,Y,k)
  [m, n] = size(X);
  F_best_overall = [];
  min_gen_error_overall = 100;
  F = [];
  while size(F,2) < n
    min_gen_error = 100;
    F_best = [];
    for i = [1:n]
      if not(any(i==F))
        F_i = [F i];
      endif
      gen_error = k_fold_cross_validation(X(:,F_i),Y,k);
      if (gen_error < min_gen_error)
        min_gen_error = gen_error;
        F_best = F_i;
      endif
      if (gen_error < min_gen_error_overall)
        min_gen_error_overall = gen_error;
        F_best_overall = F_i;
      endif
    endfor
    F = F_best;
  endwhile
  retval = F_best_overall;
endfunction

function retval = k_fold_cross_validation(X,Y,k)
  [m, n] = size(X);
  test_size = floor(m/(1.0*k));
  k_index = 0;
  rmse_test = 0;
  count = 0;
  while k_index < m
    X_train = [];
    Y_train = [];
    if k_index >= 1 && k_index+test_size+1 > m
      X_train = X(1:k_index,:);
      Y_train = Y(1:k_index);
    endif
    if k_index < 1 && k_index+test_size+1 <= m
      X_train = X((k_index+test_size+1):m,:);
      Y_train = Y((k_index+test_size+1):m);
    endif
    if k_index >= 1 && k_index+test_size+1 <= m
      X_train = X([1:k_index (k_index+test_size+1):m],:);
      Y_train = Y([1:k_index (k_index+test_size+1):m]);
    endif
    if k_index < 1 && k_index+test_size+1 > m
      disp('error')
    endif
    X_test = X((k_index+1):min(k_index+test_size,m),:);
    Y_test = Y((k_index+1):min(k_index+test_size,m));
    [theta, rmse_train] = linear_regression(X_train, Y_train);
    rmse_test = rmse_test + generalization_error(X_test, Y_test, theta);
    count = count + 1;
    k_index = k_index + test_size;
  endwhile
  retval = rmse_test / (1.0*count);
endfunction

function rmse_test = generalization_error(X_test, Y_test, theta)
  test_size = size(X_test,1);
  predicted_y_test = [ones(test_size, 1), X_test] * theta;
  rmse_test = sqrt(sum((predicted_y_test - Y_test).^2) / test_size);
endfunction