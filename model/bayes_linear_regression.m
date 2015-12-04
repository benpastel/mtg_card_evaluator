function [ theta, rmse ] = bayes_linear_regression( X, Y )
    [m, ~] = size(X);
    if (m ~= size(Y, 1) || size(Y, 2) ~= 1)
        throw(MException('linear_regression:params', 'bad Y shape'));
    end
    lambda = 0; % higher lambda means stricter regularization
        
    % prepend intercepts
    X = [ones(m, 1), X];
    [m,n] = size(X);
    % normal equations
    theta = mldivide(transpose(X)*X+ lambda .* eye(n),transpose(X) * Y);
 
    % find root-mean-squared error
    predicted_y = X * theta;
    rmse = sqrt(sum((predicted_y - Y).^2) / m);
end

