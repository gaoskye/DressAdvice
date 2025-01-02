import random

from wxcloudrun.common import SourceType, ClothingCategory
from wxcloudrun.dao import query_clothes_by_user_cat_temp, query_clothes_store_by_cat_temp
from wxcloudrun.weather import get_weather


def recommend_clothes(city, user):
    weather_data = get_weather(city)
    suitable_clothes = get_suitable_clothes(weather_data, SourceType.USER_CLOTHES, user)
    suitable_clothes_brand = get_suitable_clothes(weather_data, SourceType.CLOTHES_STORE, user)
    return weather_data, suitable_clothes, suitable_clothes_brand


# 获取适合穿着的衣服
def get_suitable_clothes(weather_data, source_type: SourceType, user):
    suitable_clothes = []
    if not weather_data:
        return suitable_clothes

    inner_clothes, outer_clothes, bottom_clothes = select_by_temp(weather_data, source_type, user)

    if outer_clothes:
        suitable_clothes.append(select_random(filter_by_label(weather_data, outer_clothes)))
    if inner_clothes:
        suitable_clothes.append(select_random(filter_by_label(weather_data, inner_clothes)))
    if bottom_clothes:
        suitable_clothes.append(select_random(filter_by_label(weather_data, bottom_clothes)))

    return suitable_clothes


def select_by_temp(weather_data, source_type: SourceType, user):
    temperature_min = int(weather_data['temperature'])
    temperature_max = int(weather_data['temperature'])
    avg_temperature = round((temperature_min + temperature_max) / 2)

    inner_clothes = []
    outer_clothes = []
    bottom_clothes = []

    if temperature_min > 23:
        # 规则1：当天气最低温度>23度，推荐的产品组合为内搭+下装
        inner_clothes = query_clothes(ClothingCategory.tops, (avg_temperature - 2), (avg_temperature + 2), source_type,
                                      user)
        bottom_clothes = query_clothes(ClothingCategory.bottoms, (avg_temperature - 2), (avg_temperature + 2),
                                       source_type, user)
    elif 10 < temperature_min <= 23:
        # 规则2：当10度<天气最低温度<23度，推荐的产品组合外套+内搭+下装
        outer_clothes = query_clothes(ClothingCategory.outerwear, (temperature_min - 2), (temperature_min - 2),
                                      source_type, user)
        inner_clothes = query_clothes(ClothingCategory.tops, (avg_temperature - 2), (avg_temperature + 2), source_type)
        bottom_clothes = query_clothes(ClothingCategory.bottoms, (avg_temperature - 2), (avg_temperature + 2),
                                       source_type, user)
    elif temperature_min <= 10:
        # 规则3：当天气温度<10度，推荐的产品组合为外套+内搭+下装
        outer_clothes = query_clothes(ClothingCategory.outerwear, temperature_min, temperature_min, source_type, user)
        inner_clothes = query_clothes(ClothingCategory.tops, temperature_min, temperature_min, source_type, user)
        bottom_clothes = query_clothes(ClothingCategory.bottoms, temperature_min, temperature_min, source_type, user)

    return inner_clothes, outer_clothes, bottom_clothes


def filter_by_label(weather_data, clothes_list):
    wind_speed = int(weather_data['windpower'].replace("≤", ""))
    weather_condition = weather_data['weather']

    filter_clothes = []
    if wind_speed > 5:
        # 假设风速大于5m/s为大风天气
        suitable_clothes_with_windproof = [clothes for clothes in clothes_list if '防风' in clothes['label']]
        if suitable_clothes_with_windproof:
            filter_clothes.extend(suitable_clothes_with_windproof)

    if any(condition in weather_condition for condition in ['雨', '雪']):
        suitable_clothes_with_rain_snow_protection = [cloth for cloth in clothes_list if '防水' in cloth['label']]
        if suitable_clothes_with_rain_snow_protection:
            filter_clothes.extend(suitable_clothes_with_rain_snow_protection)

    return filter_clothes if filter_clothes else clothes_list


def query_clothes(category, min_temp, max_temp, type: SourceType, user):
    clothes = []
    if type == SourceType.USER_CLOTHES:
        clothes.extend(query_clothes_by_user_cat_temp(category, min_temp, max_temp, user))
    elif type == SourceType.CLOTHES_STORE:
        clothes.extend(query_clothes_store_by_cat_temp(category, min_temp, max_temp))
    return clothes


def select_random(lst):
    if not lst:
        return None
    return random.choice(lst)

# print(recommend_clothes("上海", "anakin"))
