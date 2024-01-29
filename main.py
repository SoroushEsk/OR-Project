from dataAnalysis import deleteStockGoldColumn, fillMissingRowGoldAndStock
from dataAnalysis import goldAndStockChangeRate,nextWeekRateGoldAndStock, dataSlice
import ModelHandeling as MH
import pandas as pd
#### Global Variables ==========
number_of_features = 4
amount_of_money    = 50000
gold_csv = pd.read_csv(".\\CSV_FILES\\Gold.csv")
stock_csv = pd.read_csv(".\\CSV_FILES\\Stock.csv")
# gold_csv["Date"] = pd.to_datetime(gold_csv["Date"])
# # set date column as index
# gold_csv.set_index("Date", inplace = True)    
# stock_csv["Date"] = pd.to_datetime(stock_csv["Date"])
# # set date column as index
# stock_csv.set_index("Date", inplace = True)
###=============================
def get_value(coef, csv_row):
    # initial value to the intersect of the prediction
    result = coef[0]
    
    # now multiply other coefs
    for c in range(1, len(coef)):
        result += float(csv_row[f"Profit{c}"].iloc[0]) * coef[c]
    
    return result

def run(day_number):
    # setting global Variables
    global number_of_features
    global amount_of_money
    global gold_csv
    global stock_csv

    last_bond = [0, 0, 0, 0]
    #initialize from 1 of may
    prediction_date = pd.to_datetime("2023-05-01")
    for week in range(38):
        end_date        = prediction_date - pd.DateOffset(days=6)
        start_date      = end_date - pd.DateOffset(days = day_number)

        MH.regressionUpdateDZN(number_of_features, x := dataSlice(gold_csv, start_date, end_date), ".\\DZN_FILES\\gold.dzn")
        MH.regressionUpdateDZN(number_of_features, y := dataSlice(stock_csv, start_date, end_date), ".\\DZN_FILES\\stock.dzn")


        gold_tetha = MH.goldRegression()
        stock_tetha= MH.stockRegression()

        # print("gold coef", gold_tetha)
        # print("stock coef", stock_tetha)

        gold_csv_t  = pd.read_csv(".\\CSV_FILES\\Gold.csv")
        stock_csv_t = pd.read_csv(".\\CSV_FILES\\Stock.csv")

        gold_csv = gold_csv_t
        stock_csv= stock_csv_t

        gold_row  = dataSlice(gold_csv, prediction_date, prediction_date)
        stock_row = dataSlice(stock_csv, prediction_date, prediction_date)


        gold_change_rate = get_value(gold_tetha , gold_row)
        stock_change_rate= get_value(stock_tetha, stock_row)


        print("gold change", gold_change_rate)
        print("stock change", stock_change_rate)

        MH.dicisionMakingDZN(amount_of_money, gold_change_rate, stock_change_rate, float(gold_row["Close"].iloc[0]), last_bond[1:])
        gold, stock, bond = MH.dicisionMaking()

        new_amount_money = amount_of_money - (gold + stock + bond)

        new_amount_money += gold * (1 + float(gold_row["NextWeek"].iloc[0]))
        print("gold", float(gold_row["NextWeek"].iloc[0]), gold)


        new_amount_money += stock* (1 + float(stock_row["NextWeek"].iloc[0]))
        print("stock", float(stock_row["NextWeek"].iloc[0]), stock)


        new_amount_money += last_bond[3] * (1.0054)
        print("bond", bond)

        last_bond = [bond] + last_bond[0:3]
        print(last_bond)
        prediction_date += pd.DateOffset(days=6)

        amount_of_money = new_amount_money
        print(amount_of_money)
        if ( prediction_date >= pd.to_datetime("2023-11-29")) :
            break
        gold_csv_t  = pd.read_csv(".\\CSV_FILES\\Gold.csv")
        stock_csv_t = pd.read_csv(".\\CSV_FILES\\Stock.csv")

        gold_csv = gold_csv_t
        stock_csv= stock_csv_t
        print("-----------------------------------------------------")
# first should create file with "Close" column
# we are using just the one Column
    
deleteStockGoldColumn()
    
# Transactions Closes on weekends or vactions add missing data
# Using Previous Days
    
fillMissingRowGoldAndStock()
    
# Get next Week rate Of change in both data sets
    
nextWeekRateGoldAndStock()
    
# Model using change rate a feature should calculate that
    
goldAndStockChangeRate(number_of_features)

run(30)



