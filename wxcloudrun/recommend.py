import dao


# 获取适合穿着的衣服
def get_suitable_clothes(weather_data):
    suitable_clothes = []
    suitable_clothes_store = []
    if not weather_data:
        return suitable_clothes

    temperature_min = float(weather_data['temperature'])
    temperature_max = float(weather_data['temperature'])
    wind_speed = float(weather_data['wind_speed'])
    uv_index = float(weather_data['uv_index'])
    weather_condition = weather_data['weather_condition']
    avg_temperature = (temperature_min + temperature_max) / 2
    # 首先从用户衣橱中查找合适的衣服

    if temperature_min > 23:
        # 规则1：当天气最低温度>23度，推荐的产品组合为内搭+下装
        inner_clothes = dao.query_clothes_by_cat_temp('内搭', (avg_temperature - 2), (avg_temperature + 2))
        bottom_clothes = dao.query_clothes_by_cat_temp('下装', (avg_temperature - 2), (avg_temperature + 2))
        if not inner_clothes:
            suitable_clothes.extend(inner_clothes[0])
        if not bottom_clothes:
            suitable_clothes.extend(bottom_clothes[0])
    elif 10 < temperature_min < 23:
        # 规则2：当10度<天气最低温度<23度，推荐的产品组合外套+内搭+下装
        outer_clothes = dao.query_clothes_by_cat_temp('外套', (temperature_min - 2), (temperature_min - 2))
        inner_clothes = dao.query_clothes_by_cat_temp('内搭', (avg_temperature - 2), (avg_temperature + 2))
        bottom_clothes = dao.query_clothes_by_cat_temp('下装', (avg_temperature - 2), (avg_temperature + 2))
        if not outer_clothes:
            suitable_clothes.extend(outer_clothes[0])
        if not inner_clothes:
            suitable_clothes.extend(inner_clothes[0])
        if not bottom_clothes:
            suitable_clothes.extend(bottom_clothes[0])
    elif temperature_min < 10:
        # 规则3：当天气温度<10度，推荐的产品组合为外套+内搭+下装
        outer_clothes = dao.query_clothes_by_cat_temp('外套', temperature_min, temperature_min)
        inner_clothes = dao.query_clothes_by_cat_temp('内搭', temperature_min, temperature_min)
        bottom_clothes = dao.query_clothes_by_cat_temp('下装', temperature_min, temperature_min)
        if not outer_clothes:
            suitable_clothes.extend(outer_clothes[0])
        if not inner_clothes:
            suitable_clothes.extend(inner_clothes[0])
        if not bottom_clothes:
            suitable_clothes.extend(bottom_clothes[0])

        # 第二优先级：特殊需求
        if wind_speed > 5:  # 假设风速大于5m/s为大风天气
            suitable_clothes_with_windproof = [cloth for cloth in suitable_clothes if '防风' in cloth['label']]
            if suitable_clothes_with_windproof:
                suitable_clothes = suitable_clothes_with_windproof
        if uv_index > 5:  # 假设紫外线指数大于5为需要防晒
            suitable_clothes_with_sun_protection = [cloth for cloth in suitable_clothes if '防晒' in cloth['label']]
            if suitable_clothes_with_sun_protection:
                suitable_clothes = suitable_clothes_with_sun_protection
        if weather_condition in ['雨', '雪']:  # 当下雨或下雪时
            suitable_clothes_with_rain_snow_protection = [cloth for cloth in suitable_clothes if
                                                          '防雨雪' in cloth['label']]
            if suitable_clothes_with_rain_snow_protection:
                suitable_clothes = suitable_clothes_with_rain_snow_protection

    # 如果用户衣橱中没有合适的衣服，从品牌商品库中筛选
    if not suitable_clothes:
        if temperature_min > 23:
            # 规则1：当天气最低温度>23度，推荐的产品组合为内搭+下装
            inner_clothes = dao.query_clothes_store_by_cat_temp('内搭', (avg_temperature - 2), (avg_temperature + 2))
            bottom_clothes = dao.query_clothes_store_by_cat_temp('下装', (avg_temperature - 2), (avg_temperature + 2))
            if not inner_clothes:
                suitable_clothes_store.extend(inner_clothes[0])
            if not bottom_clothes:
                suitable_clothes_store.extend(bottom_clothes[0])
        elif 10 < temperature_min < 23:
            # 规则2：当10度<天气最低温度<23度，推荐的产品组合外套+内搭+下装
            outer_clothes = dao.query_clothes_by_cat_temp('外套', (temperature_min - 2), (temperature_min - 2))
            inner_clothes = dao.query_clothes_by_cat_temp('内搭', (avg_temperature - 2), (avg_temperature + 2))
            bottom_clothes = dao.query_clothes_by_cat_temp('下装', (avg_temperature - 2), (avg_temperature + 2))
            if not outer_clothes:
                suitable_clothes_store.extend(outer_clothes[0])
            if not inner_clothes:
                suitable_clothes_store.extend(inner_clothes[0])
            if not bottom_clothes:
                suitable_clothes_store.extend(bottom_clothes[0])
        elif temperature_min < 10:
            # 规则3：当天气温度<10度，推荐的产品组合为外套+内搭+下装
            outer_clothes = dao.query_clothes_by_cat_temp('外套', temperature_min, temperature_min)
            inner_clothes = dao.query_clothes_by_cat_temp('内搭', temperature_min, temperature_min)
            bottom_clothes = dao.query_clothes_by_cat_temp('下装', temperature_min, temperature_min)
            if not outer_clothes:
                suitable_clothes_store.extend(outer_clothes[0])
            if not inner_clothes:
                suitable_clothes_store.extend(inner_clothes[0])
            if not bottom_clothes:
                suitable_clothes_store.extend(bottom_clothes[0])

    # 返回推荐的衣服列表
    return suitable_clothes, suitable_clothes_store