import logging
import requests
import json
logger = logging.getLogger('weather')

def generate_weather_url(city):
    # 使用高德地图API的URL
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    # 替换为你的高德地图API密钥
    api_key = "ce24e09665ee450aeeffa8780c7f6521"
    # 构造完整的URL，包括城市和API密钥
    return f"{url}?city={city}&key={api_key}"

def get_weather(city):
    weather_url = generate_weather_url(city)
    response = requests.get(weather_url)
    assert response.status_code == 200, "查询天气网络失败"
    weather = json.loads(response.text)
    assert weather["status"] == "1", "查询天气失败"
    if not weather["lives"]:
        raise ValueError("未查询到天气信息")
    return weather["lives"][0]

# city_name = "上海"
# print(get_weather(city_name))



