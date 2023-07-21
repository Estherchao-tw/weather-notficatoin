import requests
import time
import json

def get_data():

  url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"

  params = {
      "Authorization":"CWB-6991B53F-ABFF-4CFE-A16D-4E689066F1DE",
      "format":"JSON",
      "locationName": "新北市",
  }
  response = requests.get(url, params=params)

  # print(response.text) #跟官方取得的json資料一樣
  # print(response.status_code)

  if response.status_code == 200:
      data = json.loads(response.text)

      location = data["records"]["location"][0]["locationName"]

      weather_elements = data["records"]["location"][0]["weatherElement"]

      start_time = weather_elements[0]["time"][0]["startTime"]
      start_time_d = time.strftime("%m/%d")
      end_time = weather_elements[0]["time"][0]["endTime"]

      weather_stat = weather_elements[0]["time"][0]["parameter"]["parameterName"] # 天氣狀況
      rain_pos = weather_elements[1]["time"][0]["parameter"]["parameterName"] # 下雨機率
      min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"] # 最低溫度
      confort = weather_elements[3]["time"][0]["parameter"]["parameterName"] # 舒適度
      max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"] # 最高溫度

      print(location,start_time_d,weather_stat,rain_pos,min_tem,confort,max_tem) #testing
      line_notify(tuple([location,start_time,start_time_d,end_time,weather_stat,rain_pos,min_tem,confort,max_tem]))
  else:
      print("error:cannot get data")
      line_notify(tuple())

def line_notify(data):

  token = 'gTDR3X2Qn6RJ2kdpFI0DQSBKKfC0Qs6pUWGKLN1E0G2'
  message = "may you have a wonderful day!"

  if len(data) == 0:
     message += "\n [ERROR] 無法取得天氣資訊"
  else:
     message += f"今天{data[2]}，\n{data[0]}天氣:{data[4]}\n"
     message += f"降雨機率: {data[5]}%\n"
     message += f"舒適度: {data[7]}\n"
     message += f"溫度: {data[6]}°C~{data[8]}°C\n"
     
     if int(data[5]) > 60:
        message += f"帶把傘吧！有可能會下雨喔"
     if int(data[6]) <15:
        message += f"今天會很冷，要穿暖一點"
     if int(data[8]) > 30:
        message += f"今天會超熱，喝杯飲料解渴吧!"
       

      
 
  

  url = "https://notify-api.line.me/api/notify"

  payload = {
    "message" : message,
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer ' + token
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  # print(response.text)
  
  # print(response.status_code)

if __name__ == "__main__":
  get_data()
  line_notify(["新北市","2023-07-21 06:00:00","7/9","2023-07-21 18:00:00","多雲午後短暫雷陣雨","70","20","悶熱至易中暑","33"])
else:
  print("not sending message")