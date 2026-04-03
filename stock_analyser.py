# STOCK ANALYSER - Personal Finance Tool
# By Emine Ceran | CFG Data Science 2026

# This program gets stock data from the Alpha Vantage API
# and gives a simple summary of stock performance.

# HOW TO SET UP API KEY:
# 1. Go to https://www.alphavantage.co
# 2. Sign up for a free API key
# 3. Replace "YOUR_API_KEY" below with your real key
#
# If requests is not installed, run:
# pip install requests
#
# requests is used to send HTTP requests to the API.
# datetime is used to add the date and time to the output file.

import requests
import datetime

API_KEY = "YOUR_API_KEY"  # Replace with your API key
BASE_URL = "https://www.alphavantage.co/query"


def get_stock_data(symbol):
    
    """
    Fetches stock data from the Alpha Vantage API
    using the given stock symbol.
    Returns a dictionary containing stock information.
    """
   
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "Global Quote" in data and data["Global Quote"]:
        return data["Global Quote"]
    else:
        return None


def analyse_stock(symbol):

    """
    Analyses a single stock using API data.
    Calculates price changes and determines
    whether the stock is going up or down.
    Returns a summary dictionary.
    """

    quote = get_stock_data(symbol)

    if quote is None:
        print(f"Could not find data for {symbol}")
        return None

    try:
        price = float(quote["05. price"])
        change = float(quote["09. change"])
        change_percent = quote["10. change percent"]
        high = float(quote["03. high"])
        low = float(quote["04. low"])
    except (KeyError, ValueError):
        print(f"Problem reading data for {symbol}")
        return None

    is_going_up = change > 0

    if is_going_up:
        trend = "GOING UP"
        message = "Nice! The stock is going up today! Let's hope it continues."
    else:
        trend = "GOING DOWN"
        message = "Negative movement today, but no worries! This could be a chance to buy low and catch future opportunities."

    # String slicing
    short_percent = change_percent[:7]

    result = {
        "symbol": symbol.upper(),
        "price": round(price, 2),
        "change": round(change, 2),
        "change_percent": short_percent,
        "high": round(high, 2),
        "low": round(low, 2),
        "trend": trend,
        "message": message,
        "is_going_up": is_going_up
    }

    return result


def analyse_multiple_stocks(symbols):

    """
    Loops through a list of stock symbols,
    analyses each one, and prints results.
    Returns a list of analysed stock data.
    """

    results = []

    for symbol in symbols:
        print(f"\nFetching data for {symbol}...")

        result = analyse_stock(symbol)

        if result is not None:
            results.append(result)

            print(f"Symbol:  {result['symbol']}")
            print(f"Price:   {result['price']}")
            print(f"Change:  {result['change']} ({result['change_percent']})")
            print(f"High:    {result['high']}")
            print(f"Low:     {result['low']}")
            print(f"Trend:   {result['trend']}")
            print(f"Note:    {result['message']}")
            print("-" * 40)

    return results


def save_results_to_file(results):

    """
    Saves analysed stock results into a text file.
    Includes a timestamp using the datetime module.
    """

timestamp = datetime.datetime.now()

with open("stock_results.txt", "w") as file:
    # "w" mode creates the file if it does not exist and overwrites it if it does
    file.write("STOCK ANALYSIS RESULTS\n")
    file.write(f"Generated on: {timestamp}\n")
    file.write("=" * 40 + "\n")

    for result in results:
        file.write(f"Symbol: {result['symbol']}\n")
        file.write(f"Price: {result['price']}\n")
        file.write(f"Change: {result['change']} ({result['change_percent']})\n")
        file.write(f"High: {result['high']}\n")
        file.write(f"Low: {result['low']}\n")
        file.write(f"Trend: {result['trend']}\n")
        file.write(f"Note: {result['message']}\n")
        file.write("-" * 40 + "\n")

print("\nResults have been saved to stock_results.txt")


if __name__ == "__main__":
    stock_list = ["AAPL", "TSLA", "MSFT"]

    all_results = analyse_multiple_stocks(stock_list)

    if all_results:
        save_results_to_file(all_results)
    else:
        print("No results to save.")