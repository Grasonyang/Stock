from typing import List, Dict, Any
import json
import pandas as pd
import matplotlib.pyplot as plt

comparedResult = []


def drawImage(comparedResult: List[Dict[str, Any]]) -> None:
    """
    1. comparedResult是一個json array
    2. 根據comparedResult中的stockA、stockB的open、close、high、low數值繪製圖表
    3. stockA、StockB的顏色分開，A是藍色，B是橘色
    4. open、close、high、low繪製，參考股票的線段繪製方式，不管顏色，只管型態
    5. stockB繪製再ID+0.5的位置
    """
    # 檢查comparedResult是否為空
    if not comparedResult:
        print("comparedResult is empty.")
        return

    # 建立繪圖物件
    fig, ax = plt.subplots(figsize=(10, 6))

    # 設定x軸為日期
    dates = [item["date"] for item in comparedResult]  # 假設每個item都有date欄位
    ax.set_xticks(range(len(dates)))
    ax.set_xticklabels(dates, rotation=45, ha="right")

    # 繪製線段
    for i, item in enumerate(comparedResult):
        stockA = item["stockA"]
        stockB = item["stockB"]

        for stock, color in zip([stockA, stockB], ["blue", "orange"]):
            close = stock["close"]
            open_val = stock["open"]
            high = stock["high"]
            low = stock["low"]

            # 根據close和open的關係決定顏色
            line_color = "green" if close > open_val else "red"

            # 繪製線段
            ax.plot([i, i], [low, high], color="black", linewidth=1)  # 垂直線
            ax.plot([i + (0.5 if color == "orange" else 0), i + (0.5 if color ==
                    # 開收盤線
                                                                 "orange" else 0)], [open_val, close], color=line_color, linewidth=2)

    # 設定圖表標題和軸標籤
    ax.set_title("Compared Result")
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")

    # 保存圖表到文件
    plt.tight_layout()
    plt.savefig("result.png")
    plt.close()


def getResult(output: str, correctResult: pd.Series, end: bool = False) -> None:
    """
    1. output資料類型是json
    2. correctResult資料類型是panda dtype
    3. 設置兩個變數stockA、stockB，具有column name: open, close, high, low，使用panda
    4. 當end變成true時繪圖比較A、B的數值
    """
    global comparedResult
    output = json.loads(output)
    id = correctResult['id']
    correctResult_json = {
        "open": float(correctResult['Open']),
        "close": float(correctResult['Close']),
        "high": float(correctResult['High']),
        "low": float(correctResult['Low'])
    }
    output_json = {
        "open": output.get('open'),
        "close": output.get('close'),
        "high": output.get('high'),
        "low": output.get('low')
    }
    print("\n=========correctResult_df=========\n")
    print(correctResult_json)
    print("\n=========output=========\n")
    print(output_json)
    comparedResult.append({
        "date": id,
        "stockA": output_json,
        "stockB": correctResult_json
    })
    if end:
        drawImage(comparedResult)
