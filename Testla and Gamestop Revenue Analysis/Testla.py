# Tesla Stock and Revenue Analysis
import yfinance as yf
import requests
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
#  Get Tesla Stock Data
# -----------------------------
tesla_data = yf.download("TSLA", start="2010-06-29", end="2023-01-01")  # adjust dates if needed
tesla_data.reset_index(inplace=True)
tesla_data['Date'] = pd.to_datetime(tesla_data['Date'])
tesla_data.to_csv("tesla_data.csv", index=False)

print("First 5 rows of Tesla Stock Data:")
print(tesla_data.head())

# -----------------------------
#  Get Tesla Revenue Data
# -----------------------------
url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/17.0 Safari/605.1.15"
}

response = requests.get(url, headers=headers)
tables = pd.read_html(response.text)

tesla_revenue = tables[1]
tesla_revenue.columns = ["Date", "Revenue"]
tesla_revenue = tesla_revenue.dropna()

# Clean Revenue column and convert to numeric
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].replace(r"[\$,]", "", regex=True).astype(float)

# Convert Date column to datetime
tesla_revenue['Date'] = pd.to_datetime(tesla_revenue['Date'])

print("\nLast 5 rows of Tesla Revenue Data:")
print(tesla_revenue.tail())

# -----------------------------
#  Plot Tesla Stock and Revenue
# -----------------------------
def make_graph(stock_data, revenue_data, title):
    fig, ax1 = plt.subplots(figsize=(14, 6))

    # Plot Stock Price
    ax1.plot(stock_data['Date'], stock_data['Close'], color='blue', label='Tesla Stock Price')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Stock Price (USD)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Plot Revenue on secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(revenue_data['Date'], revenue_data['Revenue'], color='green', label='Tesla Revenue')
    ax2.set_ylabel('Revenue (Millions USD)', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    plt.title(title)
    fig.autofmt_xdate()
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.show()

# Call plotting function
make_graph(tesla_data, tesla_revenue, "Tesla Stock Price and Revenue Over Time")
