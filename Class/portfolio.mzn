array[1..5] of float: cash;
array[1..5] of float: governments;
array[1..5] of float: quality;
array[1..5] of float: maturity;
array[1..5] of float: objective;
array[1..5] of var float: x;

constraint sum(i in 1..5)(cash[i] * x[i]) <= 10;
constraint sum(i in 1..5)(governments[i] * x[i]) >= 4;
constraint sum(i in 1..5)(quality[i] * x[i]) <= 0;
constraint sum(i in 1..5)(maturity[i] * x[i]) <= 0;
constraint forall(i in 1..5)(x[i] >=0);

var float: z = sum(i in 1..5)(objective[i] * x[i]);

solve maximize z;
