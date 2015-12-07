function [ theta, rmse] = locally_weighted_linear_regression( X, Y, x_test, tau)
% LOCALLY_WEIGHTED_LINEAR_REGRESSION train and evaluate a simple linear model
% inputs:
%   m x n feature vector X
%   m x 1 training vector Y
%   1 x n test example x_test (for local weights)
%   scalar tau (bandwidth)
%
% outputs:
%   n+1 x 1 model parameter theta
%   RMSE of the model on the training set weighted locally
%       (see wikipedia.org/wiki/Root-mean-square_deviation)
%
    [m, ~] = size(X);
    if (m ~= size(Y, 1) || size(Y, 2) ~= 1 || size(x_test,1) ~= 1)
        throw(MException('linear_regression:params', 'bad Y shape'));
    end
    W = zeros(m,1);
    distances = zeros(m,1);
    for i = 1:m
      W(i,1) = exp(-norm(X(i,:) - x_test)^2/(2*tau^2))/2;
      distances(i,1) = norm(X(i,:) - x_test);
      ####W(i) = 1/(X(i,:)*transpose(x_test)) #SHOULD BE JUST 0S AND 1s
    end
%    min(W)
%    max(W)
%    min(distances)
%    max(distances)
%    hist(W,60)
    % prepend intercepts
    X = [ones(m, 1), X];

    
    % normal equations
    theta = mldivide(transpose(X)*times(W,X),transpose(X) * times(W,Y));
  
    % find root-mean-squared error
%    predicted_y = X * theta;
%    rmse = sqrt(sum(times(W,(predicted_y - Y)).^2) / sum(W));
     rmse = 0;
end