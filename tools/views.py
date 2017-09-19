#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Max, Min
from datetime import datetime, timedelta, time
import collections


from .models import Weather, WeatherNow, WeatherForecast, ScheduleItem
from .forms import ScheduleItemForm
#import urllib2
from urllib.request import urlopen
import requests
import json
import ast

# Create your views here.
def ToolsIndexView(request):
    return render(request, 'tools/tools_index.html')

def ToolsTempoView(request):
    return render(request, 'tools/tools_tempo.html')

def ToolsWeatherView(request):
    weather_now = WeatherNow.objects.all()
    return render(request, 'tools/tools_weather.html', {'weather_now': weather_now})

def ToolsWeatherGetDataView(request):
    key = '70b4a25780c44125a37b8f25f946b169'
    citys = ['shanghai', 'beijing', 'xiamen', 'lasa']
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

def WeatherGetDataTimelyView(request):
    weather_data = {}
    urls = ['http://api.heweather.com/x3/weather?cityid=CN101020100&key=70b4a25780c44125a37b8f25f946b169',
            'http://api.heweather.com/x3/weather?cityid=CN101010100&key=70b4a25780c44125a37b8f25f946b169',
            'http://api.heweather.com/x3/weather?cityid=CN101230201&key=70b4a25780c44125a37b8f25f946b169',
            'http://api.heweather.com/x3/weather?cityid=CN101140101&key=70b4a25780c44125a37b8f25f946b169',
           ]
    for url in urls:
        response = urlopen(url)
        #  data = response.read()
        #参数说明http://www.heweather.com/documents/api
        if response:
            data = json.load(response)['HeWeather data service 3.0'][0]
            if data['status'] == 'ok':
                city = data['basic']['city']
                city_id = data['basic']['id']
                update = data['basic']['update']
                aqi = data['aqi']['city']['aqi']
                aqi_str = data['aqi']['city']['qlty']
                pm25 = data['aqi']['city']['pm25']
                tmp = data['now']['tmp']
                #天气情况http://www.heweather.com/documents/condition-code
                condition = data['now']['cond']['code']
                cond_txt = data['now']['cond']['txt']
                #降雨量
                pcpn = data['now']['pcpn']
                #能见度
                vis = data['now']['vis']
                #风向和风速
                wind_direction = data['now']['wind']['dir']
                wind_speed = data['now']['wind']['sc']
                #湿度
                humidity = data['now']['hum']
                #天气预测
                forecast = data['daily_forecast']
                weather_data[city] = {'city':city, 'city_id':city_id, 'update':update, 'aqi':aqi, 'aqi_str':aqi_str, 'pm25':pm25, 'tmp':tmp, 'condition':condition, 'cond_txt':cond_txt, 'pcpn':pcpn, 'vis':vis,  'wind_direction':wind_direction, 'wind_speed':wind_speed, 'humidity':humidity, 'forecast':forecast}
    return JsonResponse(weather_data)

def ToolsWeatherStatistics(request):
    weather_data = collections.OrderedDict()
    weather_data['上海'] = Weather.objects.filter(city='上海').order_by('-updata_time')
    weather_data['北京'] = Weather.objects.filter(city='北京').order_by('-updata_time')
    weather_data['厦门'] = Weather.objects.filter(city='厦门').order_by('-updata_time')
    weather_data['拉萨'] = Weather.objects.filter(city='拉萨').order_by('-updata_time')

    data = collections.OrderedDict()
    for city in weather_data:
        #0-50优，51-100良,101-150轻度污染,151-200中度污染,201-300重度污染,300-500严重污染,>500爆表
        aqi_counter = collections.OrderedDict({'优':0, '良':0, '轻度污染':0, '中度污染':0, '重度污染':0, '严重污染':0, '爆表':0})
        #最新的日期
        latest_date = weather_data[city].first().updata_time.date()
        #最早的日期
        oldest_date = weather_data[city].last().updata_time.date()

        single_day_info = {}
        single_day_tmp_max = collections.OrderedDict()
        single_day_tmp_min= collections.OrderedDict()
        single_day_aqi_max= collections.OrderedDict()
        data_temp = collections.OrderedDict()

        date_loop = oldest_date
        while date_loop <= latest_date:
            date_loop_start = datetime.combine(date_loop, time.min)
            date_loop_end = datetime.combine(date_loop, time.max)
            single_day_info_temp = weather_data[city].filter(updata_time__gte=date_loop_start, updata_time__lte=date_loop_end)
            if single_day_info_temp:
                #单日气候信息
                single_day_info[date_loop.strftime('%Y-%m-%d')] = single_day_info_temp
                #每日最低最高温度
                single_day_tmp_max[date_loop.strftime('%Y-%m-%d')] = single_day_info_temp.aggregate(Max('tmp'))
                single_day_tmp_min[date_loop.strftime('%Y-%m-%d')] = single_day_info_temp.aggregate(Min('tmp'))
                #每日最高空气质量指数
                single_day_aqi_max[date_loop.strftime('%Y-%m-%d')] = single_day_info_temp.aggregate(Max('aqi'))
            date_loop += timedelta(1)
        #计算每类空气指标的天数
        for key, value in single_day_aqi_max.iteritems():
            aqi_num = int(value['aqi__max'])
            if aqi_num <= 50:
                aqi_counter['优'] += 1
            elif aqi_num > 50 and aqi_num <= 100:
                aqi_counter['良'] += 1
            elif aqi_num > 100 and aqi_num <= 150:
                aqi_counter['轻度污染'] += 1
            elif aqi_num > 150 and aqi_num <=200:
                aqi_counter['中度污染'] += 1
            elif aqi_num > 200 and aqi_num <= 300:
                aqi_counter['重度污染'] += 1
            elif aqi_num > 300 and aqi_num <= 500:
                aqi_counter['严重污染'] +=1
            elif aqi_num > 500:
                aqi_counter['爆表'] += 1

        #传递到模板的数据
        data_temp['tmp_max'] = single_day_tmp_max
        data_temp['tmp_min'] = single_day_tmp_min
        data_temp['aqi_counter'] = aqi_counter
        data[city] = data_temp

    return render(request, 'tools/tools_weather_statistics.html', {'data':data})

@login_required
def ScheduleView(request):
    if request.method == 'POST':
        form = ScheduleItemForm(request.POST)
        if form.is_valid():
            #  form_clean = ScheduleItemForm(form.cleaned_data)
            #  form_clean.save()
            form.save()
            return HttpResponseRedirect('schedule')
    if request.method == 'GET':
        #删除条目
        if request.GET.get('action', None) == 'delete':
            item_id = request.GET.get('item_id', None)
            if item_id:
                item_need_delete = ScheduleItem.objects.get(id=item_id)
                #从数据库中删除
                item_need_delete.delete()
                return HttpResponseRedirect('schedule')
        #目标达成
        if request.GET.get('action', None) == 'finishCheck':
            item_id = request.GET.get('item_id', None)
            if item_id:
                item_finish = ScheduleItem.objects.get(id=item_id)
                #从数据库中删除
                item_finish.finish = True
                item_finish.save(update_fields=['finish'])
                return HttpResponseRedirect('schedule')
    items = ScheduleItem.objects.filter(user=request.user.username)
    ItemAddForm = ScheduleItemForm()
    return render(request, 'tools/tools_schedule.html', {'items': items, 'ItemAddForm': ItemAddForm})
