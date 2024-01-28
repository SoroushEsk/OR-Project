% Data
int: n;
array[1..n] of float: x;
array[1..n] of float: y;

% Coefficients
var float: a;
var float: b;
array[1..n] of var float: z;  

constraint forall(i in 1..n) (z[i] >= a * x[i] + b - y[i]);
constraint forall(i in 1..n) (z[i] >= y[i] - a * x[i] - b);

solve minimize sum(i in 1..n) (z[i]);

output ["a=", show(a), " b=", show(b), " z=", show(z)];
