import requests
import json
import time

# Discord Webhook 設定
WEBHOOK_URL = "https://discord.com/api/webhooks/1376151705615335535/gmAhBrPLFy2eRcM8fh6tAYRugMOQkPzJ837SjNY-NAGMppnIJdsPq_Fv7GgFlWC86wRA"
PERFORMANCE_ID = "B08T2FMH"
API_URL = "https://ticketapi.ibon.com.tw/api/Event/GetAreasInfo"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

PAYLOAD = {
    "Performance_Id": PERFORMANCE_ID
}

def check_super_rock():
    try:
        response = requests.post(API_URL, headers=HEADERS, data=json.dumps(PAYLOAD))
        if response.status_code != 200:
            print(f"❌ API 錯誤：{response.status_code}")
            return

        data = response.json()
        areas = data.get("Item", {}).get("Areas_Info", [])

        for area in areas:
            if area["PerformancesPriceAreas_Name"] == "超級搖滾區":
                status = "✅ 有票" if area["Sold_Out"] == 0 else "❌ 售完"
                print(f"[{time.strftime('%H:%M:%S')}] 超級搖滾區狀態：{status}")

                if area["Sold_Out"] == 0:
                    message = {
                        "content": f"🎟️ 超級搖滾區有票啦！快搶 👉 https://ticket.ibon.com.tw/Event/B08SCWCO/{PERFORMANCE_ID}"
                    }
                    requests.post(WEBHOOK_URL, json=message)
                break

    except Exception as e:
        print(f"⚠️ 發生錯誤：{e}")

# 每 60 秒執行一次
print("🟢 開始監控超級搖滾區...")
while True:
    check_super_rock()
    time.sleep(60)
