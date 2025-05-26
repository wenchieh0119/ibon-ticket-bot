import requests
import json
import time

print("✅ 檔案載入成功", flush=True)

WEBHOOK_URL = "https://discord.com/api/webhooks/1376151705615335535/gmAhBrPLFy2eRcM8fh6tAYRugMOQkPzJ837SjNY-NAGMppnIJdsPq_Fv7GgFlWC86wRA"
PERFORMANCE_ID = "B08T20ZV"  # 🎯 7/5 場
EVENT_ID = "B08SCWCO"
API_URL = "https://ticketapi.ibon.com.tw/api/Event/GetAreasInfo"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

def check_super_rock():
    try:
        payload = {
            "Performance_Id": PERFORMANCE_ID
        }

        print("🔁 呼叫 API...", flush=True)
        response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))
        print(f"🔧 回應狀態碼：{response.status_code}", flush=True)

        if response.status_code != 200:
            print(f"❌ API 錯誤：{response.status_code}", flush=True)
            return

        data = response.json()
        item = data.get("Item")

        if not item:
            print("⚠️ API 回傳無 Item 欄位，回傳內容如下：", flush=True)
            print(json.dumps(data, indent=2, ensure_ascii=False), flush=True)
            return

        areas = item.get("Areas_Info", [])
        for area in areas:
            if area["PerformancesPriceAreas_Name"] == "超級搖滾區":
                status = "✅ 有票" if area["Sold_Out"] == 0 else "❌ 售完"
                remaining = area.get("Discount_Limit", "?")
                print(f"[{time.strftime('%H:%M:%S')}] 超級搖滾區狀態：{status}，剩餘：{remaining} 張", flush=True)

                if area["Sold_Out"] == 0:
                    message = {
                        "content": f"🎟️ 【7/5 超級搖滾區】有票啦！目前剩下 {remaining} 張！快搶 👉 https://ticket.ibon.com.tw/Event/{EVENT_ID}/{PERFORMANCE_ID}"
                    }
                    requests.post(WEBHOOK_URL, json=message)
                break
        else:
            print("⚠️ 找不到超級搖滾區", flush=True)

    except Exception as e:
        print(f"⚠️ 發生錯誤：{e}", flush=True)

if __name__ == "__main__":
    print("🟢 開始監控 7/5 超級搖滾區...", flush=True)
    while True:
        check_super_rock()
        time.sleep(60)
