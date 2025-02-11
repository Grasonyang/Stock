import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import indicator as ind


def getData(stock_ticker, start_date, end_date, output_csv_file):
    """
        1. 從 yfinance 獲取股票資料
        2. 計算技術指標
        3. 將結果儲存到 CSV 檔案
    """
    # period設定
    macd_fastperiod = 12
    macd_slowperiod = 26
    macd_signalperiod = 9
    kdj_period = 9
    rsi_period = 14
    try:
        df = yf.download(stock_ticker, start=start_date,
                         end=end_date, interval="60m")
        if df.empty:
            raise ValueError(f"找不到股票代碼 {stock_ticker} 的資料。")

        # 分割日期
        df['Year'] = df.index.year
        df['Month'] = df.index.month
        df['Day'] = df.index.day
        # 產生流水 ID
        df['id'] = range(len(df))

        # 計算技術指標
        df = ind.getKDJ(df, period=kdj_period)
        df = ind.getMACD(df, fastperiod=macd_fastperiod,
                         slowperiod=macd_slowperiod, signalperiod=macd_signalperiod)
        # df = ind.getRSI(df)

        # 找到最大的移動窗口大小
        # MACD(slowperiod=26), KDJ(period=9), RSI(period=14)
        max_window = max(26, 9, 14)

        # 將移動窗口之前的值設定為 -1
        indicator_columns = ['K', 'D', 'J', 'MACD',
                             'MACD_Signal', 'MACD_Hist']
        for col in indicator_columns:
            df[col] = np.where(
                df.index < df.index[max_window - 1], -1, df[col])  # 修正索引

        # 重新排序欄位，讓 id 在最前面
        column_order = ['id', 'Year', 'Month', 'Day', 'Open', 'High', 'Low', 'Close', 'Volume',
                        'K', 'D', 'J', 'MACD', 'MACD_Signal', 'MACD_Hist']
        df = df[column_order]
        df.to_csv(output_csv_file, index=False)

    except ValueError as e:
        print(f"值錯誤: {e}")
    except Exception as e:
        print(f"例外錯誤: {e}")


def main():
    """
        1. main function
    """
    stock_ticker = "2454.TW"
    start_date = "2023-09-01"
    end_date = "2024-12-31"
    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d %H:%M:%S")
    output_csv_file = '2454'+now_date+'.csv'
    getData(stock_ticker, start_date, end_date, output_csv_file)


if __name__ == '__main__':
    main()
