import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

def plot_prices(dates, prices):
    # Convert date strings to datetime objects
    # dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates]

    # Plotting the data
    plt.plot(dates, prices, marker='o', linestyle='-')

    # Adding labels and title
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Price Over Time')

    # Display the plot
    plt.show()


import matplotlib.pyplot as plt
import pandas as pd

def plot_prices_from_csv(file1, file2):
    # Read data from CSV files
    data1 = pd.read_csv(file1)
    data2 = pd.read_csv(file2)

    # Convert date strings to datetime objects
    data1['Date'] = pd.to_datetime(data1['Date'])
    data2['Date'] = pd.to_datetime(data2['Date'])

    # Create subplots
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=True)

    # Plotting the data in the first subplot
    axes[0].plot(data1['Date'], data1['Close'], label='File 1', marker='o', linestyle='-', color = 'blue')
    axes[0].set_ylabel('Close Price - File 1')
    axes[0].legend()

    # Plotting the data in the second subplot
    axes[1].plot(data2['Date'], data2['Close'], label='File 2', marker='o', linestyle='-', color = 'yellow')
    axes[1].set_xlabel('Date')
    axes[1].set_ylabel('Close Price - File 2')
    axes[1].legend()

    # Adding overall title
    plt.suptitle('Close Price Comparison')

    # Display the plot
    plt.show()

# Example usage:
file1_path = ".\\CSV_FILES\\Stock.csv"
file2_path = ".\\CSV_FILES\\Gold.csv"

plot_prices_from_csv(file1_path, file2_path)

