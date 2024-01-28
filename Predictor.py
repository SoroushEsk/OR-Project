import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from minizinc import Instance, Model, Solver 

total_money = 50000

def disicionMaking():
    solver = Solver.lookup("cbc")
    model = Model("./Buyer.mzn")
    model.add_file("./Buyer.dzn")
    instance = Instance(solver, model)
    result = instance.solve()


    return (result['gold'] , result['stock'], result['bond'])
def get_close_value_by_date(target_date, df):

    # Convert the 'date' column to a pandas datetime object
    df['Date'] = pd.to_datetime(df['Date'])
    while(True):
        # Filter the DataFrame based on the target date
        filtered_df = df[df['Date'] == pd.to_datetime(target_date)]

        # Check if any rows were found for the given date
        if not filtered_df.empty:
            # Extract the 'close' value from the filtered DataFrame
            close_value = filtered_df['Close'].iloc[0]
            return close_value
        target_date -= pd.DateOffset(days = 1)
    
    print(f"No data found for the date {target_date}")
    return None
def buyAndSell():

    last_bond = [0, 0 , 0, 0]
    stock_file_path = '^IXIC.csv'
    gold_file_path = 'GLD.csv'
    start_date = pd.to_datetime('2023-04-24')
    end_date   = pd.to_datetime('2023-05-01')
    global total_money
    # Write data to .dzn files
    for i in range(36):
        stock_data, gold_data = load_and_preprocess_data(stock_file_path, gold_file_path,  start_date, end_date)

        write_to_dzn(stock_data, 'stock.dzn')
        write_to_dzn(gold_data, 'gold.dzn')

        model = Model("lineRegression.mzn")  
        solver = Solver.lookup("cbc")
        
        a_stock, b_stock = solve_and_extract_coefficients('stock.dzn', model, solver)
        a_gold, b_gold = solve_and_extract_coefficients('gold.dzn', model, solver)
        
        
        stock_data, gold_data = load_and_preprocess_data(stock_file_path, gold_file_path, start_date,end_date + pd.DateOffset(days=7))


        next_gold = list(gold_data["Days"])[-1] * a_gold + b_gold
        next_stock = list(stock_data["Days"])[-1] * a_stock + b_stock
        

        
        current_gold_price  =  get_close_value_by_date(end_date, gold_data)
        current_stock_price =  get_close_value_by_date(end_date, stock_data)



        gold_profit   =  (next_gold-current_gold_price) / current_gold_price 
        stock_profit  =  (next_stock-current_stock_price) / current_stock_price
        


        setCoefDisicion(total_money, gold_profit, stock_profit, current_gold_price, last_bond[1:])
        gold, stock, bond = disicionMaking()
        print(gold, stock, bond)

        # print(stock_data, gold_data)
        gold_real_price  = get_close_value_by_date(end_date + pd.DateOffset(days = 6), gold_data)
        stock_real_price = get_close_value_by_date(end_date + pd.DateOffset(days = 6), stock_data)
        


        profit = total_money - (gold + stock + bond)
        profit += last_bond[3] * (1.0054)
        


        gold_profit  = (gold_real_price - current_gold_price)/ current_gold_price
        profit += gold * (1 + gold_profit)



        stock_profit = (stock_real_price- current_stock_price)/ current_stock_price
        profit += stock * ( 1 + stock_profit)
        print("gold_profit", gold_profit)
        print(stock_profit)

        last_bond = [bond] + last_bond[0:3]
        end_date += pd.DateOffset(days=6)
        start_date += pd.DateOffset(days = 6)

        total_money = profit
        
        print(total_money)
        print(end_date)

        print("-------------------------------------------")
        if end_date >= pd.to_datetime("2023-11-9"):
            break

    print(total_money + sum(last_bond)*(1.0054))

def setCoefDisicion(total_money, gold_profit, stock_profit, gold_price, last_bond):
    buyer_dzn_file = open("Buyer.dzn", 'w')


    profit_sum = .0054/4
    if( gold_profit > 0 ):
        profit_sum += gold_profit
    if( stock_profit > 0 ):
        profit_sum += stock_profit

    max_stock= 0
    max_bond =( (.0054/4) / profit_sum )* total_money
    max_gold = 0

    if( gold_profit > 0 ):
        max_gold = (gold_profit / profit_sum) * total_money
    if( stock_profit > 0 ):
        max_stock =(stock_profit / profit_sum) * total_money
    
    if(profit_sum == .0054/4):
        max_bond = 0.0* total_money
    max_gold = total_money
    max_stock= total_money

    buyer_dzn_file.write( f"bond_profit = {.0054/4} ;\n" )
    buyer_dzn_file.write( f"stock_profit = {stock_profit} ;\n") 
    buyer_dzn_file.write( f"gold_profit = {gold_profit} ;\n")
    buyer_dzn_file.write( f"max_bond = {max_bond} ;\n")
    buyer_dzn_file.write( f"max_stock = {max_stock} ;\n")
    buyer_dzn_file.write( f"max_gold = {max_gold} ;\n")
    buyer_dzn_file.write( f"last_week_bond = {last_bond} ;\n")
    buyer_dzn_file.write( f"gold_price = {gold_price}; \n")
    buyer_dzn_file.write( f"total_money = {total_money} ;\n")


# Function to load and preprocess data
def load_and_preprocess_data(stock_file, gold_file, start_date=None, end_date=None):
    stock_data = pd.read_csv(stock_file)
    gold_data = pd.read_csv(gold_file)
    
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    gold_data['Date'] = pd.to_datetime(gold_data['Date'])

    if start_date is not None and end_date is not None:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        stock_data = stock_data[(stock_data['Date'] >= start_date) & (stock_data['Date'] <= end_date)]
        gold_data = gold_data[(gold_data['Date'] >= start_date) & (gold_data['Date'] <= end_date)]

    stock_data = stock_data[['Date', 'Close']]
    gold_data = gold_data[['Date', 'Close']]

    stock_data['Days'] = (stock_data['Date'] - stock_data['Date'].min()).dt.days
    gold_data['Days'] = (gold_data['Date'] - gold_data['Date'].min()).dt.days

    return stock_data, gold_data


# Function to write data to .dzn file
def write_to_dzn(data, filename):
    with open(filename, 'w') as file:
        file.write(f'n = {len(data)};\n')
        file.write('x = [' + ', '.join(data['Days'].astype(str)) + '];\n')
        file.write('y = [' + ', '.join(data['Close'].astype(str)) + '];\n')


# Function to solve the model and extract coefficients
def solve_and_extract_coefficients(data_file, model, solver):
    instance = Instance(solver, model)
    instance.add_file(data_file)
    result = instance.solve()

    a = float(result["a"])
    b = float(result["b"])
    return a, b


buyAndSell()


# # File paths and date range
# stock_file_path = '^IXIC.csv'
# gold_file_path = 'GLD.csv'
# start_date = '2023-04-20'
# end_date =   '2023-05-01'

# # Load and preprocess data
# stock_data, gold_data = load_and_preprocess_data(stock_file_path, gold_file_path, start_date, end_date)

# # Write data to .dzn files
# write_to_dzn(stock_data, 'stock.dzn')
# write_to_dzn(gold_data, 'gold.dzn')

# model = Model("lineRegression.mzn")  
# solver = Solver.lookup("cbc")

# a_stock, b_stock = solve_and_extract_coefficients('stock.dzn', model, solver)
# a_gold, b_gold = solve_and_extract_coefficients('gold.dzn', model, solver)

def plot_data_with_regression(stock_data, gold_data, a_stock, b_stock, a_gold, b_gold):
    # Calculate regression line values
    stock_data['Regression'] = a_stock * stock_data['Days'] + b_stock
    gold_data['Regression'] = a_gold * gold_data['Days'] + b_gold

    # Plot the data with regression lines
    plt.figure(figsize=(14, 7))

    # Stock data and regression line
    plt.subplot(1, 2, 1)
    plt.plot(stock_data['Date'], stock_data['Close'], label='Stock Close Price', color='blue')
    plt.plot(stock_data['Date'], stock_data['Regression'], label='Stock Regression Line', color='red', linestyle='--')
    plt.title('Stock Prices Over Time with Regression Line')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)

    # Gold data and regression line
    plt.subplot(1, 2, 2)
    plt.plot(gold_data['Date'], gold_data['Close'], label='Gold Close Price', color='gold')
    plt.plot(gold_data['Date'], gold_data['Regression'], label='Gold Regression Line', color='green', linestyle='--')
    plt.title('Gold Prices Over Time with Regression Line')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

# Example usage
# plot_data_with_regression(stock_data, gold_data, a_stock, b_stock, a_gold, b_gold)


def plot_next_week_with_regression(stock_file, gold_file, a_stock, b_stock, a_gold, b_gold, start_date, end_date):
    end_date = pd.to_datetime(end_date)

    # Calculate the date range for the next week
    start_date_next_week = end_date + pd.DateOffset(days=1)
    end_date_next_week = end_date + pd.DateOffset(days=7)

    # Load data
    stock_data, gold_data = load_and_preprocess_data(stock_file, gold_file, start_date_next_week, end_date_next_week)

    if stock_data.empty or gold_data.empty:
        print("No data available for the next week.")
        return

    # Calculate regression values for the next week
    stock_data['Regression'] = a_stock * stock_data['Days'] + b_stock
    gold_data['Regression'] = a_gold * gold_data['Days'] + b_gold

    # Plot the data with regression lines
    plt.figure(figsize=(14, 7))

    # Stock data and regression line
    plt.subplot(1, 2, 1)
    plt.plot(stock_data['Date'], stock_data['Close'], label='Stock Close Price', color='blue')
    plt.plot(stock_data['Date'], stock_data['Regression'], label='Stock Regression Line', color='red', linestyle='--')
    plt.title('Stock Prices for Next Week with Regression Line')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)

    # Gold data and regression line
    plt.subplot(1, 2, 2)
    plt.plot(gold_data['Date'], gold_data['Close'], label='Gold Close Price', color='gold')
    plt.plot(gold_data['Date'], gold_data['Regression'], label='Gold Regression Line', color='green', linestyle='--')
    plt.title('Gold Prices for Next Week with Regression Line')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

# Usage
# plot_next_week_with_regression(stock_file_path, gold_file_path, a_stock, b_stock, a_gold, b_gold, start_date, end_date)