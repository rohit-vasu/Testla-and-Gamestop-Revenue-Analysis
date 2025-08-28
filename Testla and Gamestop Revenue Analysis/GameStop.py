# GameStop Stock and Revenue Graph
import yfinance as yf
import requests
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Get GME Stock Data
# -----------------------------
gme_data = yf.download("GME", start="2010-01-01", end="2023-01-01")
gme_data.reset_index(inplace=True)
gme_data['Date'] = pd.to_datetime(gme_data['Date'])
gme_data.to_csv("gme_data.csv", index=False)

print("First 5 rows of GME Stock Data:")
print(gme_data.head())

# -----------------------------
#  Get GME Revenue Data
# -----------------------------
url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/17.0 Safari/605.1.15"
}

response = requests.get(url, headers=headers)
tables = pd.read_html(response.text)

gme_revenue = tables[1]
gme_revenue.columns = ["Date", "Revenue"]
gme_revenue = gme_revenue.dropna()

# Clean Revenue column and convert to numeric
gme_revenue['Revenue'] = gme_revenue['Revenue'].replace(r"[\$,]", "", regex=True).astype(float)
gme_revenue['Date'] = pd.to_datetime(gme_revenue['Date'])

print("\nLast 5 rows of GME Revenue Data:")
print(gme_revenue.tail())

# -----------------------------
#  Plot GME Stock and Revenue
# -----------------------------
def make_graph(stock_data, revenue_data, title):
    fig, ax1 = plt.subplots(figsize=(14, 6))

    # Plot Stock Price
    ax1.plot(stock_data['Date'], stock_data['Close'], color='red', label='GME Stock Price')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Stock Price (USD)', color='red')
    ax1.tick_params(axis='y', labelcolor='red')

    # Plot Revenue on secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(revenue_data['Date'], revenue_data['Revenue'], color='orange', label='GME Revenue')
    ax2.set_ylabel('Revenue (Millions USD)', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    plt.title(title)
    fig.autofmt_xdate()
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.show()

# Call the plotting function for GameStop
make_graph(gme_data, gme_revenue, "GameStop Stock Price and Revenue Over Time")
