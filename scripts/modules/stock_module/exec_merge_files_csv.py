import yfinance as yf
import numpy

from utils.fileCsvUtil import merge_csv

numpy.version.version
yf.version.version

print("numpy version: " + numpy.version.version)
print("yf version: " + yf.version.version)

#merge_csv("_data/stock_data/sp500_2024_11_23_11_01_14", "_data/stock_data/_stock_merge/sp500_2024_11_23")
#merge_csv("_data/stock_data/nasdaq_2024_11_23_11_38_36", "_data/stock_data/_stock_merge/nasdaq_2024_11_23")
#merge_csv("_data/stock_data/sp500_2024_12_01_17_43_36", "_data/stock_data/_stock_merge/sp500_2024_12_01")
#merge_csv("_data/stock_data/nasdaq_2024_12_01_18_16_21", "_data/stock_data/_stock_merge/nasdaq_2024_12_01")
#merge_csv("_data/stock_data/sp500_2025_01_11_20_11_28", "_data/stock_data/_stock_merge/sp500_2025_01_11")
#merge_csv("_data/stock_data/nasdaq_2025_01_11_21_32_38", "_data/stock_data/_stock_merge/nasdaq_2025_01_11")
#merge_csv("_data/stock_data/sp500_2025_02_10_22_35_37", "_data/stock_data/_stock_merge/sp500_2025_02_10")
#merge_csv("_data/stock_data/nasdaq_2025_02_09_22_59_22", "_data/stock_data/_stock_merge/nasdaq_2025_02_10")
#merge_csv("_data/stock_data/sp500_2025_02_10_22_35_37", "_data/stock_data/_stock_merge/sp500_2025_03_09")
#merge_csv("_data/stock_data/nasdaq_2025_02_09_22_59_22", "_data/stock_data/_stock_merge/nasdaq_2025_03_09")
#merge_csv("_data/stock_data/sp500_2025_04_06_18_50_39", "_data/stock_data/_stock_merge/sp500_2025_04_06")
merge_csv("_data/stock_data/nasdaq_2025_04_06_19_34_15", "_data/stock_data/_stock_merge/nasdaq_2025_04_06")