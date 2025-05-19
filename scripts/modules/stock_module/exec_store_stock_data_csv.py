import math
import pandas as pd
import pymysql

def get_db_connection():
    """Establish a connection to the database."""
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='stock_track',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Connected to the database!")
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()
            print("Database version:", version)
        return connection
    except pymysql.MySQLError as e:
        print("Error while connecting to MySQL:", e)
        return None
    
def get_date_from_path(file_path):
    date_csv = file_path.split("/")[-1]
    date_csv = date_csv.split(".")[0]
    date_csv = date_csv.split("_")
    date_csv = "-".join(date_csv[1:3])
    "set to date first day replacing the last"
    date_csv = date_csv + "-01"

    return date_csv
    
def get_issue_id(cursor, ticker):
    query = "SELECT * FROM catalog_issues WHERE initials like %s"
    cursor.execute(query, (ticker,))
    result = cursor.fetchone()
    if result is not None:
        id_issue = result["id"]
        return id_issue
    else:
        return None
    
def exist_issue_price_target(cursor, id_issue, date):
    query = "SELECT * FROM issues_historical_fair_value WHERE id_issue = %s AND id_date = %s"
    cursor.execute(query, (id_issue, date))
    result = cursor.fetchone()
    if result is not None:
        return True
    else:
        return False
    
def exist_issue_earnings(cursor, id_issue, date):
    query = "SELECT * FROM issues_historical_earning WHERE id_issue = %s AND id_date = %s"
    cursor.execute(query, (id_issue, date))
    result = cursor.fetchone()
    if result is not None:
        return True
    else:
        return False
    
def store_issue_price_target(cursor, id_issue, date, price_target):
    query = "INSERT INTO issues_historical_fair_value (id_issue, id_date, fair_value) VALUES (%s, %s, %s)"
    cursor.execute(query, (id_issue, date, price_target))
    cursor.connection.commit()

def store_issue_earnings(cursor, id_issue, date, earning_estimate, earning_real):
    query = "INSERT INTO issues_historical_earning (id_issue, id_date, earning_estimate, earning_real) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (id_issue, date, earning_estimate, earning_real))
    cursor.connection.commit()

def process_issue_price_target(cursor, ticker, id_issue, date, price_target):

    description = "ticker: " + ticker + " id_issue: " + id_issue.__str__() + " date: " + date + " price_target: " + price_target.__str__()
    
    if exist_issue_price_target(cursor, id_issue, date):                
        print(f"Issue price target already exist. {description}")
        return

    store_issue_price_target(cursor, id_issue, date, price_target)
    print(f"Issue price target stored. {description}")


def process_issue_earnings(cursor, ticker, id_issue, date, earning_estimate, earning_real):

    if math.isnan(earning_estimate):
        print(f"Earning estimate not found. ticker: {ticker}")
        return

    description = "ticker: " + ticker + " id_issue: " + id_issue.__str__() + " date: " + date + " earning_estimate: " + earning_estimate.__str__() + " earning_real: " + earning_real.__str__()

    if exist_issue_earnings(cursor, id_issue, date):                
        print(f"Issue earnings already exist. {description}")
        return

    store_issue_earnings(cursor, id_issue, date, earning_estimate, earning_real)
    print(f"Issue earnings stored. {description}")

#file_path = "_data/stock_data/_stock_merge/sp500_2024_11_23.csv"
#file_path = "_data/stock_data/_stock_merge/sp500_2024_12_01.csv"
#file_path = "_data/stock_data/_stock_merge/sp500_2025_01_11.csv"
#file_path = "_data/stock_data/_stock_merge/sp500_2025_02_10.csv"
#file_path = "_data/stock_data/_stock_merge/sp500_2025_03_09.csv"
#file_path = "_data/stock_data/_stock_merge/sp500_2025_04_06.csv"
#file_path = "_data/stock_data/_stock_merge/nasdaq_2024_11_23.csv"
#file_path = "_data/stock_data/_stock_merge/nasdaq_2024_12_01.csv"
#file_path = "_data/stock_data/_stock_merge/nasdaq_2025_01_11.csv"
#file_path = "_data/stock_data/_stock_merge/nasdaq_2025_02_10.csv"
#file_path = "_data/stock_data/_stock_merge/nasdaq_2025_03_09.csv"
file_path = "_data/stock_data/_stock_merge/nasdaq_2025_04_06.csv"

header_map = {"ticker": "ticker", "price_target": "price_target",
              "earning_full_date_1": "earning_0_full_date", "earning_estimate_1": "earning_0_eps_estimate", "earning_real_1": "earning_0_eps_actual",
              "earning_full_date_2": "earning_1_full_date", "earning_estimate_2": "earning_1_eps_estimate", "earning_real_2": "earning_1_eps_actual",
              "earning_full_date_3": "earning_2_full_date", "earning_estimate_3": "earning_2_eps_estimate", "earning_real_3": "earning_2_eps_actual",
              }

date_csv = get_date_from_path(file_path)
print("Date csv: " + date_csv)

df = pd.read_csv(file_path)
connection = None
#print(df)
#print(df[header_map["ticker"]])

try:
    connection = get_db_connection()
    if connection is None:
        print("Failed to connect to the database. Exiting...")
        exit(1)
    with connection.cursor() as cursor:

        for index, row in df.iterrows():
            '''if(index > 1):
                break'''
            print(f"Row csv {index}: {row[header_map['ticker']]}, {row[header_map['price_target']]}")

            if(math.isnan(row[header_map['price_target']])):
                print(f"Price target not found. ticker: {row[header_map['ticker']]}")
                continue
            
            id_issue = get_issue_id(cursor, row[header_map["ticker"]])
            
            if id_issue is None:
                print(f"Issue not found. ticker: {row[header_map['ticker']]}")
                continue

            process_issue_price_target(cursor, row[header_map["ticker"]], id_issue, date_csv, row[header_map["price_target"]])
            process_issue_earnings(cursor, row[header_map["ticker"]], id_issue, row[header_map["earning_full_date_1"]], row[header_map["earning_estimate_1"]], row[header_map["earning_real_1"]])
            process_issue_earnings(cursor, row[header_map["ticker"]], id_issue, row[header_map["earning_full_date_2"]], row[header_map["earning_estimate_2"]], row[header_map["earning_real_2"]])
            process_issue_earnings(cursor, row[header_map["ticker"]], id_issue, row[header_map["earning_full_date_3"]], row[header_map["earning_estimate_3"]], row[header_map["earning_real_3"]])
            #print(result) 

finally:
    if connection:
        connection.close()
        print("Connection closed.")