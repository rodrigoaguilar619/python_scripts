import yfinance as yf
import numpy

from stocks.stock_data import build_stock_data

numpy.version.version
yf.version.version

print("numpy version: " + numpy.version.version)
print("yf version: " + yf.version.version)

build_stock_data("_data/stock_data", "_stocks_nasdaq.txt", "nasdaq")