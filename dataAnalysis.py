import pandas as pd

# Function that only saves necessary column
def deleteUnnecessaryColumns(filePath:str, resultName:str) -> None:
    # get the csv not edited file
    timeSeriesTable = pd.read_csv(filePath)

    # create a new table with needed colmns
    necessaryColumns = timeSeriesTable[["Date", "Close"]]

    # create new csv file that has only needed columns
    necessaryColumns.to_csv(resultName, index = False)

# Function that clear the gold and stock tables
def deleteStockGoldColumn():
    # only save "Closed" column of both gold and stock
    deleteUnnecessaryColumns(".\\CSV_FILES\\GLD.csv", ".\\CSV_FILES\\Gold.csv")
    deleteUnnecessaryColumns(".\\CSV_FILES\\^IXIC.csv", ".\\CSV_FILES\\Stock.csv")

# Fill the week end data with previous days
def fillNonExistingDates(csv_path:str) -> None:
    # get the data file 
    timeSeriesTable = pd.read_csv(csv_path)

    # set Date column as index column 
    timeSeriesTable["Date"] = pd.to_datetime(timeSeriesTable["Date"])
    timeSeriesTable.set_index("Date", inplace=True)

    # Resample the data to ensure all dates are present
    timeSeriesTable_resampled = timeSeriesTable.resample('D').asfreq()

    # Fill missing values using forward fill
    timeSeriesTable_resampled = timeSeriesTable_resampled.bfill()

    timeSeriesTable_resampled.to_csv(csv_path)

# get Gold and Stock and fill not existing rows
def fillMissingRowGoldAndStock():
    
    # Gold file
    fillNonExistingDates(".\\CSV_FILES\\Gold.csv")

    # Stock File 
    fillNonExistingDates(".\\CSV_FILES\\Stock.csv")

# save Next week profit rate
def addNextWeekChangeRate(filePath):
    tableSeries = pd.read_csv(filePath)

    # find the next week change rate based on today
    nextWeek = [(tableSeries["Close"][i+7] - tableSeries["Close"][i] ) / tableSeries["Close"][i] for i in range(0, len(tableSeries["Close"]) - 7)]        
    nextWeek = nextWeek + [0] * 7
    tableSeries["NextWeek"] = nextWeek 

    tableSeries.to_csv(filePath)

# set the next week value of change rate for gold and stock
def nextWeekRateGoldAndStock():
    #Gold-----------------
    addNextWeekChangeRate(".\\CSV_FILES\\Gold.csv")
    #Stock----------------
    addNextWeekChangeRate(".\\CSV_FILES\\Stock.csv")

# gets a csv file and then adds the number of columns you want with appropriate values finally returns the edited filedef addNewCol(numofCols , fileName):
def addChangeRateColumns(filePath, featureNum):
    file = pd.read_csv(filePath) 

    for day in range(1,featureNum+1):
        profit = [(file["Close"][i]-file["Close"][i - day])/file["Close"][i] for i in range(day, len(file["Close"]))]        
        profit = [0]*day + profit
        file["Profit"+ str(day)] = profit    

    file.to_csv(filePath)
        
# add change rate to gold and stock csv file
def goldAndStockChangeRate(featureNum : int) -> None:
     # Gold Change rate-----------------------
     addChangeRateColumns(".\\CSV_FILES\\Gold.csv", featureNum)
     # Stock Change rate------------------------
     addChangeRateColumns(".\\CSV_FILES\\Stock.csv", featureNum)

# slice table in csv from start to end 
def dataSlice(CSV, start_date, end_date):
    # put out any type of date in correct format
    start_date  = pd.to_datetime(start_date)
    end_date    = pd.to_datetime(end_date)
    CSV["Date"] = pd.to_datetime(CSV["Date"])

    # set date column as index
    CSV.set_index("Date", inplace = True)

    # slice the table between to time periods
    return CSV.loc[start_date : end_date]












