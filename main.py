import pandas as pd
import os
import json
import dealData.main as dealData
import callAPI.main as callAPI
import drawResult.main as drawResult


def readData():
    """
    1. 讀取 CSV 檔案
    2. 從index = 26 開始讀資料
    ex:{
        "id": 0,
        "open": 0.0,
        "close": 0.0,
        "high": 0.0,
        "low": 0.0,
        "volume": 0.0,
        "kdj": {"k": 0.0, "d": 0.0, "j": 0.0},
        "macd": {
            "dif"          :  0.0,
            "dea"          :  0.0,
            "macd"         :  0.0
        }
    }
    """
    try:
        df = pd.read_csv(
            'getData/data/24542025-02-10 12:55:37.csv')
        resultIndex = 56
        datas = dealData.toJson(df)
        i = 0
        for data in datas:
            """
            output是AI回答的結果
            correctResult是真正的股價結果
            """
            output = callAPI.send_message(json.dumps(data))
            correctResult = df.iloc[resultIndex]
            print(correctResult)
            i += 1
            resultIndex += 1
            if i == 10:
                drawResult.getResult(output, correctResult, True)
                break
            drawResult.getResult(output, correctResult)
        print("done")
    except FileNotFoundError:
        print(f"找不到檔案：getData/data/24542025-02-10 12:55:37.csv")
        print(f"目前的工作目錄：{os.getcwd()}")
    except Exception as e:
        print(f"發生錯誤：{e}")


if __name__ == "__main__":
    readData()
