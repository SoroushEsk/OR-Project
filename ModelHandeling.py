from minizinc import Instance, Model, Solver 
import pandas as pd

# run the Disition Making model and return (gold, stock, bond)
def dicisionMaking() -> tuple:

    solver = Solver.lookup("cbc")

    model = Model(".\\MZN_FILES\\Buyer.mzn")
    model.add_file(".\\DZN_FILES\\Buyer.dzn")

    instance = Instance(solver, model)
    result = instance.solve()

    return (result['gold'] , result['stock'], result['bond'])

# set the dzn file for model to operate
def dicisionMakingDZN(total_money, gold_profit, stock_profit, gold_price, last_bond):
    buyer_dzn_file = open(".\\DZN_FILES\\Buyer.dzn", 'w')

    # give each component a maximum value based on their profit
    # considering seprating our money and don't put all of them in one basket
    #### --------------------------------------------------------------------
    profit_sum = .0054/4
    if( gold_profit > 0 ):
        profit_sum += gold_profit
    if( stock_profit > 0 ):
        profit_sum += stock_profit

    max_stock= 0
    max_bond =0.000001* total_money
    max_gold = 0

    if( gold_profit > 0 ):
        max_gold = (gold_profit / profit_sum) * total_money * 0.00001
    if( stock_profit > 0 ):
        max_stock =(stock_profit / profit_sum) * total_money
    
    if(profit_sum == .0054/4):
        max_bond = 0.0* total_money
    #### end of finding max value of each 

    buyer_dzn_file.write( f"bond_profit = {.0054/4} ;\n" )
    buyer_dzn_file.write( f"stock_profit = {stock_profit} ;\n") 
    buyer_dzn_file.write( f"gold_profit = {gold_profit} ;\n")
    buyer_dzn_file.write( f"max_bond = {max_bond} ;\n")
    buyer_dzn_file.write( f"max_stock = {max_stock} ;\n")
    buyer_dzn_file.write( f"max_gold = {max_gold} ;\n")
    buyer_dzn_file.write( f"last_week_bond = {last_bond} ;\n")
    buyer_dzn_file.write( f"gold_price = {gold_price}; \n")
    buyer_dzn_file.write( f"total_money = {total_money} ;\n")

# run gold regression function
def goldRegression():
    solver = Solver.lookup("cbc")

    model = Model(".\\MZN_FILES\\Regression.mzn")
    model.add_file(".\\DZN_FILES\\gold.dzn")

    instance = Instance(solver, model)
    result   = instance.solve()

    return [result["offset"]] + result["featureCoef"]

# run stock regression function
def stockRegression():
    solver = Solver.lookup("cbc")

    model = Model(".\\MZN_FILES\\Regression.mzn")
    model.add_file(".\\DZN_FILES\\stock.dzn")

    instance = Instance(solver, model)
    result   = instance.solve()

    return [result["offset"]] + result["featureCoef"]
#set gold.dzn file before run the model
def regressionUpdateDZN(featureNum:int, CSV, filePath) -> None :
    # modifying the gold dzn file
    # load the file first
    dzn_file = open(filePath, "w")

    dzn_file.write(f"sampleNumber  = {len(CSV['Close'])}; \n ")
    dzn_file.write(f"featureNumber = {featureNum}; \n")

    # adding features into sample dicision variable
    featureString = "|"
    for f in range(1, featureNum+1):
        featureString += ', '.join(CSV[f"Profit{f}"].astype(str)) + "|"
    dzn_file.write(f"sample        = [{featureString}]; \n")


    dzn_file.write(f"profit        = [{', '.join(CSV['NextWeek'].astype(str))}]; \n")

