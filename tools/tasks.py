from celery import shared_task


@shared_task()
def tools_weather_get_data():
    key = '70b4a25780c44125a37b8f25f946b169'
    citys = ['shanghai', 'huhehaote', 'beijing', 'xiamen', 'lasa']
    urls = ['https://free-api.heweather.com/v5/weather?city=%s&key=%s' %(city, key) for city in citys]

    # delete the exit instances and later create the new instances
    WeatherForecast.objects.all().delete()
    for index, url in enumerate(urls):
        response = requests.get(url)
        # 参数说明http://www.heweather.com/documents/api
        if response:
            data = json.loads(response.text)['HeWeather5'][0]
            if data['status'] == 'ok':
                # basic info
                city = data['basic']['city']
                city_id = data['basic']['id']
                update_loc = data['basic']['update']['loc']
                update_utc = data['basic']['update']['utc']
                # now weather info
                cond_code = data['now']['cond']['code']
                cond_txt = data['now']['cond']['txt']
                fl = data['now']['fl']   # sendible temperature
                hum = data['now']['hum']  # relative humidity
                pcpn = data['now']['pcpn']  # precipitation
                pres = data['now']['pres']  # pressure
                tmp = data['now']['tmp']  # temperature
                vis = data['now']['vis']  # visibility
                wind_deg = data['now']['wind']['deg']  # wind degree
                wind_dir = data['now']['wind']['dir']  # wind direction
                wind_sc = data['now']['wind']['sc']  # wind scale
                wind_spd = data['now']['wind']['spd']  # wind speed
                # aqi
                aqi_index = data['aqi']['city']['aqi']
                aqi_qlty = data['aqi']['city']['qlty']
                # create the weather now model instance
                weathernow_ins, created = WeatherNow.objects.update_or_create(city_id=city_id, defaults={'city':city,
                                                                                                         'city_id':city_id, 'update_loc':update_loc, 'update_utc':update_utc, 'cond_code':cond_code,
                                                                                                         'cond_txt':cond_txt, 'fl':fl, 'hum':hum, 'pcpn':pcpn, 'pres':pres, 'tmp':tmp, 'vis':vis,
                                                                                                         'wind_deg':wind_deg, 'wind_dir':wind_dir, 'wind_sc':wind_sc, 'wind_spd':wind_spd,
                                                                                                         'aqi_index':aqi_index, 'aqi_qlty':aqi_qlty},)
                weathernow_ins.save()

                # forecast
                daily_forecast = data['daily_forecast']
                for index, i_forecast in enumerate(daily_forecast):
                    fc_city = city
                    fc_index = index
                    # astro
                    fc_mr = i_forecast['astro']['mr']
                    fc_ms = i_forecast['astro']['ms']
                    fc_sr = i_forecast['astro']['sr']
                    fc_ss = i_forecast['astro']['ss']
                    # condition
                    fc_txt_d = i_forecast['cond']['txt_d']
                    fc_txt_n = i_forecast['cond']['txt_n']
                    # other
                    fc_date = i_forecast['date']
                    fc_hum = i_forecast['hum']
                    fc_pcpn = i_forecast['pcpn']
                    fc_pop = i_forecast['pop']
                    fc_pres = i_forecast['pres']
                    fc_uv = i_forecast['uv']
                    fc_vis = i_forecast['vis']
                    # temperature
                    fc_tmp_max = i_forecast['tmp']['max']
                    fc_tmp_min = i_forecast['tmp']['min']
                    # wind
                    fc_wind_deg = i_forecast['wind']['deg']
                    fc_wind_dir = i_forecast['wind']['dir']
                    fc_wind_sc = i_forecast['wind']['sc']
                    fc_wind_spd = i_forecast['wind']['spd']
                    # create the forecast model instance
                    fc_ins = WeatherForecast(fc_city=city, fc_index=fc_index, fc_mr=fc_mr, fc_ms=fc_ms, fc_sr=fc_sr,
                                             fc_ss=fc_ss, fc_txt_d=fc_txt_d, fc_txt_n=fc_txt_n, fc_date=fc_date,
                                             fc_hum=fc_hum, fc_pcpn=fc_pcpn, fc_pop=fc_pop, fc_pres=fc_pres,
                                             fc_uv=fc_uv, fc_vis=fc_vis, fc_tmp_max=fc_tmp_max, fc_tmp_min=fc_tmp_min,
                                             fc_wind_deg=fc_wind_deg, fc_wind_dir=fc_wind_dir, fc_wind_sc=fc_wind_sc, fc_wind_spd=fc_wind_spd,
                                             weathernow=weathernow_ins)
                    fc_ins.save()
                # renew the forecast model instance
            else:
                return render(request, 'tools/tools_weather_get_data.html', {'status': 'bad status'})


    return render(request, 'tools/tools_weather_get_data.html', {'status': 'ok'})
