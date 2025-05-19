import yfinance as yf
import os
import time

from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils.fileCsvUtil import write_to_csv
from utils.fileUtil import read_file
from utils.financeUtil import calculate_average_rating, calculate_percentage_increase

def build_date_suffix(date):
     year = str(date.year)
     month = str(date.month)
     return year + "_" + month + "_"

def get_stock_data(full_path):
     tickers = read_file(full_path)
     #print("Tickers: "); print(tickers)
     return tickers

def get_time_str():
     current_datetime = datetime.now()
     current_datetime_str = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
     return current_datetime_str

def build_file_csv(dirPath, current_datetime_str, data_list, data_header, ticker_group_index, limit_tickers):
     start_limit = str((limit_tickers*ticker_group_index)+1)
     end_limit = str((limit_tickers*ticker_group_index)+limit_tickers)
     start_limit = start_limit.zfill(4)
     end_limit = end_limit.zfill(4)


     output_dir = dirPath + current_datetime_str
     os.makedirs(output_dir, exist_ok=True)
     output_file = os.path.join(output_dir, f'financial_data_{current_datetime_str}_limit_{start_limit}_to_{end_limit}.csv')

     write_to_csv(data_list, data_header, output_file)

def get_header():
     current_date = date.today()
     current_date_header = date.today()
     current_date_header_month_3 = current_date - relativedelta(months=3)
     current_date_header_month_2 = current_date - relativedelta(months=2)
     current_date_header_month_1 = current_date - relativedelta(months=1)
     current_date_header_month_0 = current_date

     data_header = {
          "ticker": "",
          "price_current": "",
          "price_target": "",
          "percentage_increase": "",
          "is_over_25_percentage": "",
          "recommendation_" + build_date_suffix(current_date_header_month_0) + "rating": "",
          "recommendation_" + build_date_suffix(current_date_header_month_0) + "classification": "",
          "recommendation_" + build_date_suffix(current_date_header_month_3) + "strongBuy": "",
          "recommendation_" + build_date_suffix(current_date_header_month_3) + "buy": "",
          "recommendation_" + build_date_suffix(current_date_header_month_3) + "hold": "",
          "recommendation_" + build_date_suffix(current_date_header_month_3) + "sell": "",
          "recommendation_" + build_date_suffix(current_date_header_month_3) + "strongSell": "",
          "recommendation_" + build_date_suffix(current_date_header_month_3) + "rating": "",
          "recommendation_" + build_date_suffix(current_date_header_month_3) + "classification": "",
          "recommendation_" + build_date_suffix(current_date_header_month_2) + "strongBuy": "",
          "recommendation_" + build_date_suffix(current_date_header_month_2) + "buy": "",
          "recommendation_" + build_date_suffix(current_date_header_month_2) + "hold": "",
          "recommendation_" + build_date_suffix(current_date_header_month_2) + "sell": "",
          "recommendation_" + build_date_suffix(current_date_header_month_2) + "strongSell": "",
          "recommendation_" + build_date_suffix(current_date_header_month_2) + "rating": "",
          "recommendation_" + build_date_suffix(current_date_header_month_2) + "classification": "",
          "recommendation_" + build_date_suffix(current_date_header_month_1) + "strongBuy": "",
          "recommendation_" + build_date_suffix(current_date_header_month_1) + "buy": "",
          "recommendation_" + build_date_suffix(current_date_header_month_1) + "hold": "",
          "recommendation_" + build_date_suffix(current_date_header_month_1) + "sell": "",
          "recommendation_" + build_date_suffix(current_date_header_month_1) + "strongSell": "",
          "recommendation_" + build_date_suffix(current_date_header_month_1) + "rating": "",
          "recommendation_" + build_date_suffix(current_date_header_month_1) + "classification": "",
          "recommendation_" + build_date_suffix(current_date_header_month_0) + "strongBuy": "",
          "recommendation_" + build_date_suffix(current_date_header_month_0) + "buy": "",
          "recommendation_" + build_date_suffix(current_date_header_month_0) + "hold": "",
          "recommendation_" + build_date_suffix(current_date_header_month_0) + "sell": "",
          "recommendation_" + build_date_suffix(current_date_header_month_0) + "strongSell": "",
          "recommendation_" + build_date_suffix(current_date_header_month_0) + "rating": "",
          "recommendation_" + build_date_suffix(current_date_header_month_0) + "classification": "",
          "earning_0_full_date": "",
          "earning_0_eps_estimate": "",
          "earning_0_eps_actual": "",
          "earning_1_full_date": "",
          "earning_1_eps_estimate": "",
          "earning_1_eps_actual": "",
          "earning_2_full_date": "",
          "earning_2_eps_estimate": "",
          "earning_2_eps_actual": "",
     }

     #print("Data Header: "); print(data_header)
     return data_header

def build_stock_data(dirPath, file_name_stocks, stock_suffix):
     data_header = get_header()
     tickers = get_stock_data(dirPath + "/_stock_index/" + file_name_stocks)
     current_date = date.today()
     current_datetime_str = get_time_str()

     limit_tickers = 250
     split_tickers = [tickers[i:i+limit_tickers] for i in range(0, len(tickers), limit_tickers)]
     #print("Split tickers: "); print(split_tickers)

     count = 0
     for ticker_group_index, tickers in enumerate(split_tickers):
          data_list = []
          for ticker_index, ticker in enumerate(tickers):
               try:
                    time.sleep(3)
                    data = {}
                    stock = yf.Ticker(ticker)
                    count = count + 1

                    if(stock.history(period="1d").empty):
                         print("No data for ticker: " + ticker)
                         continue

                    print("Ticker " + str(count) + " - " + ticker)
                    price_targets = stock.get_analyst_price_targets()
                    recommendations = stock.get_recommendations()
                    earnings = stock.get_earnings_history()

                    #print("Analyst Price Targets: "); print(yf.Ticker(ticker).get_analyst_price_targets())
                    #print("Recommendations: "); print(recommendations)
                    #print("Earnings: "); print(earnings)

                    data["ticker"] = ticker
                    data["price_current"] = price_targets.get("current");
                    data["price_target"] = price_targets.get("mean");
                    data["percentage_increase"] = calculate_percentage_increase(price_targets.get("current"), price_targets.get("mean"));
                    data["is_over_25_percentage"] = data["percentage_increase"] >= 25;
                    
                    if recommendations is not None and not recommendations.empty:
                         for index, row in recommendations.iterrows():
                              dateRecommendation = current_date - relativedelta(months=abs(int(row.get("period").replace("m", ""))))
                              year_month = str(dateRecommendation.year) + "_" + str(dateRecommendation.month) + "_";
                              rating = calculate_average_rating(row.get("strongBuy"), row.get("buy"), row.get("hold"), row.get("sell"), row.get("strongSell"))
                              data["recommendation_" + year_month + "strongBuy"] = row.get("strongBuy");
                              data["recommendation_" + year_month + "buy"] = row.get("buy");
                              data["recommendation_" + year_month + "hold"] = row.get("hold");
                              data["recommendation_" + year_month + "sell"] = row.get("sell");
                              data["recommendation_" + year_month + "strongSell"] = row.get("strongSell");
                              data["recommendation_" + year_month + "rating"] = rating[0];
                              data["recommendation_" + year_month + "classification"] = rating[1];
               
                    if earnings is not None and not earnings.empty:
                         for i, (index, row) in enumerate(earnings.iterrows()):
                              dateEarning = index;
                              year_month = str(dateEarning.year) + "_" + str(dateEarning.month) + "_";
                              data["earning_" + str(i) + "_full_date"] = str(dateEarning);
                              data["earning_" + str(i) + "_eps_estimate"] = float(row.get("epsEstimate"));
                              data["earning_" + str(i) + "_eps_actual"] = float(row.get("epsActual"));
               except Exception as e:
                    print("Error: " + str(e))
               
               #print("Object: "); print(data)
               data_list.append(data)

          #print("Object List: "); print(data_list)
          build_file_csv(dirPath + "/" + stock_suffix + "_", current_datetime_str, data_list, data_header, ticker_group_index, limit_tickers)
