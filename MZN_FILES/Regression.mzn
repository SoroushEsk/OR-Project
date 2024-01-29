% Data
int: sampleNumber ;
int: featureNumber;
array[1..featureNumber,1..sampleNumber] of float: sample;

array[1..sampleNumber] of float: profit ;


% Coefficients

array[1..featureNumber] of var float: featureCoef ;
var float: offset;

array[1..sampleNumber] of var float: z;  

constraint forall(i in 1..sampleNumber) (z[i] >= (sum ( j in 1..featureNumber ) (featureCoef[j] * sample[j, i])) + offset - profit[i]);
constraint forall(i in 1..sampleNumber) (z[i] >= (profit[i] - sum ( j in 1..featureNumber ) (featureCoef[j] * sample[j, i])) - offset);

solve minimize sum(i in 1..sampleNumber) (z[i]);

output ["a=", show(featureCoef), " b=", show(offset), " z=", show(z)];
