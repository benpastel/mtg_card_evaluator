X = [
    0, 1, 0;
    2, 0, 1;
    4, 0, 0;
    6, 0, 0
];

Y = [
    10;
    11; 
    12;
    13
];

expected_theta = [
    10; % intercept
    0.5;
    0;
    0
];
expected_rmse = 0;
epsilon = 0.00001; % for float comparison

[theta, rmse] = linear_regression(X, Y);
if ~(all(abs(theta - expected_theta) < epsilon) ...
        && abs(rmse - expected_rmse) < epsilon)
    disp('linear regression test failed');
else
    disp('linear regression test passed');
end

