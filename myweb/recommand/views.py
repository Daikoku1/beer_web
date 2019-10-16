from django.shortcuts import render, redirect
from .models import input_beer, Beer
from .forms import beerForm

from django_pandas.io import read_frame
import pandas as pd
import numpy as np
import operator

def recommand(*args, data):
    """
    :param args: this
    :param data:
    :return:
    """
    # Pre-Processing
    for col in data.columns:
        if col == 'name' or col == 'id':
            continue
        data[col] = data[col].apply(lambda x: eval(x))

    # 각 feature별 리스트 생성
    feel = []
    look = []
    taste = []
    smell = []
    # 각 feature의 값들은 리뷰의 카운트 / 전체 카운트 값을 가중치로
    # 모든 feature의 가줓이는 하나의 딕셔너리에
    # key = 해당 feature의 명칭, value 가중치 값
    new_dict = {}
    for arg in args:
        if arg not in list(data.name):
            return ["존재하지 않는 맥주입니다. 다시 입력해주세요."], False
        for feature in ['feel', 'look', 'taste', 'smell']:
            data_f = data[data['name'] == arg][feature].values[0]
            for key in data_f.keys():
                if key in new_dict.keys():
                    new_dict[key] = new_dict[key] + (data_f[key] / sum(data_f.values()))
                else:
                    new_dict[key] = (data_f[key] / sum(data_f.values()))

    result_dict = {}
    for j in range(len(data)):
        value = 0
        for feature in ['feel', 'look', 'taste', 'smell']:
            data_t = data.loc[j][feature]
            name = data.loc[j]['name']
            for key in data_t:
                if key in new_dict.keys():
                    value += new_dict[key] * data_t[key] / sum(data_t.values())

        result_dict[name] = value

    # max_값 찾기(3개 출력)
    a_list = sorted(result_dict.items(), key=operator.itemgetter(1), reverse=True)

    result = []
    cnt = 0
    while cnt != 3:
        beer = a_list.pop(0)[0]
        if beer not in args:
            cnt += 1
            result.append([beer,str(int(data[data['name'] == beer].id))])
    return result, True

def home(request):
    if request.method == 'POST':
        form = beerForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/result')
    else:
        form = beerForm()
    return render(request, 'user/home.html', {'form': form})

def result(request):
    beerquery = input_beer.objects.order_by('-id')
    dataset = Beer.objects.all()
    beerdf = read_frame(dataset)

    recommand_result, chk = recommand(beerquery[0].first, beerquery[0].second, beerquery[0].third, data=beerdf)

    return render(request, 'user/result.html', {'result': recommand_result, 'check': chk})

def intro(request):
    return render(request, 'user/intro.html')

