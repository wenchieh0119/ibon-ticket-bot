import requests
import json
import time

print("✅ 檔案載入成功", flush=True)

WEBHOOK_URL = "https://discord.com/api/webhooks/1376151705615335535/gmAhBrPLFy2eRcM8fh6tAYRugMOQkPzJ837SjNY-NAGMppnIJdsPq_Fv7GgFlWC86wRA"
API_URL = "https://ticketapi.ibon.com.tw/api/Event/GetAreasInfo"

# ✅ 要監控的三個場次（日期: (Performance_Id, Event_Id)）
PERFORMANCES = {
    "7/4": ("B08SK4AM", "B08SCWCO"),
    "7/5": ("B08T20ZV", "B08SCWCO"),
    "7/6": ("B08T2FMH", "B08SCWCO"),
}

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# 🔒 避免重複通知
notified = {}

def check_super_rock(date_str, performance_id, event_id):
    try:
        payload = {"Performance_Id": performance_id}

        print(f"🔁 [{date_str}] 呼叫 API...", flush=True)
        response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))
        print(f"🔧 回應狀態碼：{response.status_code}", flush=True)

        if response.status_code != 200:
            print(f"❌ [{date_str}] API 錯誤：{response.status_code}", flush=True)
            return

        data = response.json()
        item = data.get("Item")

        if not item:
            print(f"⚠️ [{date_str}] API 回傳空資料，跳過", flush=True)
            return

        areas = item.get("Areas_Info", [])
        for area in areas:
            if area["PerformancesPriceAreas_Name"] == "超級搖滾區":
                status = "✅ 有票" if area["Sold_Out"] == 0 else "❌ 售完"
                remaining = area.get("Discount_Limit", "?")
                print(f"[{time.strftime('%H:%M:%S')}] [{date_str}] 超級搖滾區狀態：{status}，剩餘：{remaining} 張", flush=True)

                if area["Sold_Out"] == 0:
                    # 若已通知過，不再重複發送
                    if notified.get(performance_id) == remaining:
                        print(f"🔁 [{date_str}] 已通知過 {remaining} 張，略過", flush=True)
                        return

                    # 發送 Discord 通知
                    message = {
                        "content": f"🎟️ 【{date_str} 超級搖滾區】有票啦！目前剩下 {remaining} 張！快搶 👉 https://ticket.ibon.com.tw/Event/{event_id}/{performance_id}"
                    }
                    requests.post(WEBHOOK_URL, json=message)
                    notified[performance_id] = remaining
                break
        else:
            print(f"⚠️ [{date_str}] 找不到超級搖滾區", flush=True)

    except Exception as e:
        print(f"⚠️ [{date_str}] 發生錯誤：{e}", flush=True)

if __name__ == "__main__":
    print("🟢 開始監控所有超級搖滾區（7/4～7/6）...", flush=True)
    while True:
        for date_str, (performance_id, event_id) in PERFORMANCES.items():
            check_super_rock(date_str, performance_id, event_id)
        time.sleep(60)
