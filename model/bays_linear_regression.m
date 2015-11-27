function [ theta, rmse ] = linear_regression( X, Y )
% LINEAR_REGRESSION train and evaluate a simple linear model
% inputs:
%   m x n feature vector X
%   m x 1 training vector Y
%
% outputs:
%   n+1 x 1 model parameter theta
%   RMSE of the model on the training set
%       (see wikipedia.org/wiki/Root-mean-square_deviation)
%
    [m, ~] = size(X);
    if (m ~= size(Y, 1) || size(Y, 2) ~= 1)
        throw(MException('linear_regression:params', 'bad Y shape'));
    end

        
    % prepend intercepts
    X = [ones(m, 1), X];
    [m,n] = size(X);
    % normal equations
%     theta = pinv(transpose(X)*X+eye(n)) * transpose(X) * Y;
    theta = mldivide(transpose(X)*X+eye(n),transpose(X) * Y);
 
    % find root-mean-squared error
    predicted_y = X * theta;
    rmse = sqrt(sum((predicted_y - Y).^2) / m);
end

