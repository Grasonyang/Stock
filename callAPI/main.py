"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""

import os
import json
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

os.environ["GEMINI_API_KEY"] = "AIzaSyAdwVSlYhhrmFWyrRd12ApwQF5_wCeBdOY"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_schema": content.Schema(
        type=content.Type.OBJECT,
        enum=[],
        required=["open", "close", "high", "low", "reason"],
        properties={
            "open": content.Schema(
                type=content.Type.NUMBER,
            ),
            "close": content.Schema(
                type=content.Type.NUMBER,
            ),
            "high": content.Schema(
                type=content.Type.NUMBER,
            ),
            "low": content.Schema(
                type=content.Type.NUMBER,
            ),
            "reason": content.Schema(
                type=content.Type.STRING,
            ),
        },
    ),
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction="你是一個股票的觀察者，你基於過去 30 天的股票數據 (包含開盤價、收盤價、最高價、最低價、成交量、KDJ、MACD 等指標)，預測第 31 天的各項指標數值輸出。\n輸出內容\n\"open\": number,\n\"close\": number,\n\"high\": number,\n\"low\": number,\n\"reason\": \"原因\"",
)

history = []
chat_session = model.start_chat(
    history=history,
)


def send_message(input):
    global chat_session
    output = chat_session.send_message(input)
    if check_output(output) is False:
        return send_message(input)
    record_message(input, output)
    return deal_output(output)


def record_message(input, output):
    global history
    history.append({"role": "user", "parts": [input]})
    history.append({"role": "model", "parts": [output]})


def check_output(output):
    """
    檢查 Gemini API 回傳的輸出是否有效。

    Args:
        output: Gemini API 回傳的 GenerateContentResponse 物件。

    Returns:
        True: 如果輸出有效。
        False: 如果輸出無效，需要重新發送請求。
    """

    try:
        # 1. 檢查 candidates 是否存在且不為空
        if not output.candidates:
            print("Error: No candidates found in the output.")
            return False

        # 2. 遍歷 candidates 檢查 finish_reason
        for candidate in output.candidates:
            if not candidate.content.parts:  # 檢查 parts 是否存在
                print("Error: No parts found in the candidate's content.")
                return False

            for part in candidate.content.parts:  # 遍歷 parts
                try:
                    text = part.text
                    # 嘗試解析 text 是否為 JSON (如果你的模型輸出是 JSON)
                    json.loads(text)  # 如果不是 JSON 會拋出異常
                except json.JSONDecodeError:
                    # 只顯示前50個字元，避免過長
                    print(
                        f"Warning: Candidate text is not valid JSON: {text[:50]}...")
                    # 如果你的模型預期輸出 JSON，但實際上不是，這可能是一個錯誤
                    # 你可以選擇直接返回 False，或者根據情況決定是否重試
                    # return False  # 如果你希望模型輸出嚴格的 JSON 格式
                    pass  # 如果你允許模型輸出非 JSON 格式

                finish_reason = candidate.finish_reason
                if finish_reason != "STOP":
                    print(
                        f"Warning: Candidate finish_reason is not STOP: {finish_reason}")
                    # 根據 finish_reason 判斷是否需要重試
                    # 一些非 STOP 的 finish_reason 可能需要重試，例如 LENGTH
                    # 但有些則不需要，例如 CONTENT_FILTER
                    if finish_reason == "LENGTH":  # 舉例
                        return False  # 如果是長度限制，可以考慮重試

        # 3. (可選) 檢查 avg_logprobs (設定閾值)
        # for candidate in output.candidates:
        #     avg_logprobs = candidate.avg_logprobs
        #     if avg_logprobs is not None and avg_logprobs < -2.0:  # 示例閾值
        #         print(f"Warning: Low avg_logprobs: {avg_logprobs}")
        #         return False

        return True  # 所有檢查都通過，表示輸出有效

    except AttributeError as e:  # 捕捉缺失屬性的錯誤
        print(f"Error: Incomplete output structure: {e}")
        return False
    except Exception as e:  # 捕捉其他未知錯誤
        print(f"An unexpected error occurred during output check: {e}")
        return False


def deal_output(output):
    print(output)
    # 檢查是否有 candidates
    if output.candidates:
        # 遍歷每個 candidate
        for candidate in output.candidates:
            # 檢查 content 是否存在
            if candidate.content:
                # 檢查 parts 是否存在
                if candidate.content.parts:
                    # 遍歷每個 part
                    for part in candidate.content.parts:
                        # 提取 text
                        text = part.text
                        return text
                else:
                    print("No parts found in the content for this candidate.")
            else:
                print("No content found for this candidate.")
    else:
        print("No candidates found in the output.")

    # response:
    # GenerateContentResponse(
    #     done=True,
    #     iterator=None,
    #     result=protos.GenerateContentResponse({
    #         "candidates": [
    #             {
    #                 "content": {
    #                     "parts": [
    #                         {
    #                             "text": "{\n  \"close\": 538.5,\n  \"high\": 539.5,\n  \"low\": 537.5,\n  \"open\": 538.0,\n  \"reason\": \"The stock is showing signs of potential stabilization after a recent downtrend. The KDJ is low, suggesting oversold conditions, and the MACD is negative. Expect a slightly lower open, with a potential range between 537.5 and 539.5.\"\n}"
    #                         }
    #                     ],
    #                     "role": "model"
    #                 },
    #                 "finish_reason": "STOP",
    #                 "avg_logprobs": -0.04098757108052572
    #             }
    #         ],
    #         "usage_metadata": {
    #             "prompt_token_count": 71668,
    #             "candidates_token_count": 114,
    #             "total_token_count": 71782
    #         },
    #         "model_version": "gemini-2.0-flash"
    #     }),
    # )
