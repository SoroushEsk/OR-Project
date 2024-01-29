from dataAnalysis import deleteStockGoldColumn, fillMissingRowGoldAndStock
from dataAnalysis import goldAndStockChangeRate,nextWeekRateGoldAndStock

# first should create file with "Close" column
# we are using just the one Column
deleteStockGoldColumn()
# Transactions Closes on weekends or vactions add missing data
# Using Previous Days
fillMissingRowGoldAndStock()
# Get next Week rate Of change in both data sets
nextWeekRateGoldAndStock()
# Model using change rate a feature should calculate that
goldAndStockChangeRate(30)



