import json


def toJson(df):
    """
    格式化每一筆為json
    """
    datas = []
    for index, row in df.iterrows():
        if index >= 26:
            data = {
                "id": int(row['id']),
                "open": float(row['Open']),
                "close": float(row['Close']),
                "high": float(row['High']),
                "low": float(row['Low']),
                "volume": float(row['Volume']),
                "kdj": {
                    "k": float(row['K']),
                    "d": float(row['D']),
                    "j": float(row['J'])
                },
                "macd": {
                    "dif": float(row['MACD']),
                    "dea": float(row['MACD_Signal']),
                    "macd": float(row['MACD_Hist'])
                }
            }
            datas.append(data)
    return toDataArray(datas)


def toDataArray(data):
    """
    以30為基準，作為滑動窗口，窗口中的30比json object，會放入新的array中
    """
    data_array = []
    for i in range(len(data)-30):
        add_prompt_data = {
            "prompt": "基於過去 30 天的股票數據 (包含開盤價、收盤價、最高價、最低價、成交量、KDJ、MACD 等指標)，預測第 31 天的各項指標數值輸出。",
            "data": data[i:i+30]
        }
        data_array.append(add_prompt_data)
    return data_array
