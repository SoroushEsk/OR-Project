var float: bond_profit;
var float: gold_profit;
var float: stock_profit;
var float: no_spend_profit;

var float: max_bond ;
var float: max_gold ;
var float: max_save ;
var float: max_stock;

var float: total_money;

var float: bond;
var float: gold;
var float: stock;
var float: save;

constraint bond + gold + stock + save <= total_money;

constraint bond >= 0;
constraint gold >= 0;
constraint stock>= 0;
constraint save >= 0;

constraint bond  <= max_bond ;
constraint gold  <= max_gold ;
constraint save  <= max_save ;
constraint stock <= max_stock;

var float: total_profit = bond * bond_profit + gold * gold_profit + stock_profit * stock + no_spend_profit * save;
solve maximize total_profit;

