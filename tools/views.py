import collections
from datetime import datetime, timedelta, time

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Max, Min

from .models import Weather, WeatherNow, ScheduleItem
from .forms import ScheduleItemForm


def tools_index_view(request):
    return render(request, 'tools/tools_index.html')


def tools_tempo_view(request):
    return render(request, 'tools/tools_tempo.html')


def tools_weather_view(request):
    weather_now = WeatherNow.objects.all()
    return render(request, 'tools/tools_weather.html', {'weather_now': weather_now})


def tools_weather_statistics(request):
    weather_data = collections.OrderedDict()
    weather_data['上海'] = Weather.objects.filter(city='上海').order_by('-updata_time')
    weather_data['北京'] = Weather.objects.filter(city='北京').order_by('-updata_time')
    weather_data['厦门'] = Weather.objects.filter(city='厦门').order_by('-updata_time')
    weather_data['拉萨'] = Weather.objects.filter(city='拉萨').order_by('-updata_time')

    data = collections.OrderedDict()
    for city in weather_data:
        # 0-50优，51-100良,101-150轻度污染,151-200中度污染,201-300重度污染,300-500严重污染,>500爆表
        aqi_counter = collections.OrderedDict({'优':0, '良':0, '轻度污染':0, '中度污染':0, '重度污染':0, '严重污染':0, '爆表':0})
        # 最新的日期
        latest_date = weather_data[city].first().updata_time.date()
        # 最早的日期
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

        # 传递到模板的数据
        data_temp['tmp_max'] = single_day_tmp_max
        data_temp['tmp_min'] = single_day_tmp_min
        data_temp['aqi_counter'] = aqi_counter
        data[city] = data_temp

    return render(request, 'tools/tools_weather_statistics.html', {'data':data})


@login_required
def schedule_view(request):
    if request.method == 'POST':
        form = ScheduleItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('schedule')
    if request.method == 'GET':
        # 删除条目
        if request.GET.get('action', None) == 'delete':
            item_id = request.GET.get('item_id', None)
            if item_id:
                item_need_delete = ScheduleItem.objects.get(id=item_id)
                # 从数据库中删除
                item_need_delete.delete()
                return HttpResponseRedirect('schedule')
        # 目标达成
        if request.GET.get('action', None) == 'finishCheck':
            item_id = request.GET.get('item_id', None)
            if item_id:
                item_finish = ScheduleItem.objects.get(id=item_id)
                # 从数据库中删除
                item_finish.finish = True
                item_finish.save(update_fields=['finish'])
                return HttpResponseRedirect('schedule')
    items = ScheduleItem.objects.filter(user=request.user.username)
    ItemAddForm = ScheduleItemForm()
    return render(request, 'tools/tools_schedule.html', {'items': items, 'ItemAddForm': ItemAddForm})
