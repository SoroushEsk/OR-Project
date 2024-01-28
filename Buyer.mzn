var float: bond_profit;
var float: gold_profit;
var float: stock_profit;

var float: max_bond ;
var float: max_gold ;
var float: max_stock;

array[1..3] of var float : last_week_bond;

var float: total_money;

var float: bond;
var float: gold;
var float: stock;

var float: gold_price;
var float: mod_result =  gold - floor(gold / gold_price) * gold_price;
constraint bond + gold + stock  <= total_money - sum (i in 1..3) (last_week_bond[i]);

constraint bond >= 0;
constraint gold >= 0;
constraint stock>= 0;





constraint mod_result = 0.0 ;
constraint bond  <= max_bond ;
constraint gold  <= max_gold ;
constraint stock <= max_stock;

var float: total_profit = bond * bond_profit + gold * gold_profit + stock_profit * stock;
solve maximize total_profit;

