import sys
#import geopandas as gpd
import requests
import numpy as np
import flask
from bs4 import BeautifulSoup #ダウンロードしてなかったらpipでできるからやってね。
import csv
import re
import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statistics
import math
from scipy import stats
import warnings
import matplotlib.patches as mpatches
matplotlib.use('agg')
from japanmap import pref_names, pref_code, groups, picture
warnings.filterwarnings('ignore')

# URLで年と月ごとの設定ができるので%sで指定した英数字を埋め込めるようにします。
base_url = "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=%s&block_no=%s&year=%s&month=%s&day=1&view=p1"
place_list = ["札幌", "青森", "盛岡", "仙台", "秋田", "山形", "福島", "水戸", "宇都宮", "前橋", "熊谷", "千葉", "東京", "横浜", "新潟", "富山", "金沢", "福井", "甲府", "長野", "岐阜", "静岡", "名古屋", "津", "彦根", "京都", "大阪", "神戸", "奈良", "和歌山", "鳥取", "松江", "岡山", "広島", "山口", "徳島", "高松", "松山", "高知", "福岡", "佐賀", "長崎", "熊本", "大分", "宮崎", "鹿児島", "那覇"]

hokkaido_list = []
hokkaido_list.append(place_list[0])
touhoku_list = place_list[1:7]
kanto_list = place_list[7:14]
tyubu_list = place_list[14:23]
kinki_list = place_list[23:30]
tyugoku_list = place_list[30:35]
shikoku_list = place_list[35:39]
kyushu_list = place_list[39:]


color_num = {0: "white", 1:"red", -1:"blue", 2:"green"}

#取ったデータをfloat型に変えるやつ。(データが取れなかったとき気象庁は"/"を埋め込んでいるから0に変える)
def str2float(str):
    try:
        #return float(str)
        return float(re.sub(r"[^\d.]", "", str))
    except:
        return 0.0

def make_df(place, year, month):
    place_codeA = [81, 62, 45, 44, 14, 21, 23, 31, 32, 33, 35, 34, 36, 54, 56, 55, 48, 41, 57, 42, 43, 40, 52, 51, 49, 45, 53, 50, 46, 68, 69, 61, 60, 67, 66, 63, 65, 64, 73, 72, 74, 71, 81, 82, 85, 83, 84, 86, 88, 87, 91]
    place_codeB = [47784, 47772, 47682, 47662, 47412, 47423, 47430, 47575, 47582, 47584, 47588, 47590, 47595, 47604, 47605, 47607, 47610, 47615, 47616, 47624, 47626, 47629, 47632, 47636, 47638, 47648, 47651, 47656, 47670, 47741, 47746, 47759, 47761, 47765, 47768, 47770, 47777, 47780, 47887, 47891, 47893, 47895, 47762, 47807, 47813, 47815, 47817, 47819, 47827, 47830, 47936]
    place_name = ["山口", "大阪", "千葉", "東京", "札幌", "室蘭", "函館", "青森", "秋田", "盛岡", "山形", "仙台", "福島", "新潟", "金沢", "富山", "長野", "宇都宮", "福井", "前橋", "熊谷", "水戸", "岐阜", "名古屋", "甲府", "銚子", "津", "静岡", "横浜", "松江", "鳥取", "京都", "彦根", "広島", "岡山", "神戸", "和歌山", "奈良", "松山", "高松", "高知", "徳島", "下関", "福岡", "佐賀", "大分", "長崎", "熊本", "鹿児島", "宮崎", "那覇"] 

    # URLで年と月ごとの設定ができるので%sで指定した英数字を埋め込めるようにします。
    base_url = "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=%s&block_no=%s&year=%s&month=%s&day=1&view=p1"

    #最終的にデータを集めるリスト
    All_list = [['年月日', '降水量', '気温_平均', '気温_最高', '気温_最低', '湿度_平均', '湿度_最小', '日照時間']]
    #print(place)
    index = place_name.index(place)

    #print(year)
    #print(month)

    r = requests.get(base_url%(place_codeA[index], place_codeB[index], year, month))
    r.encoding = r.apparent_encoding

    # サイトごとスクレイピング
    soup = BeautifulSoup(r.text)
    # findAllで条件に一致するものをすべて抜き出す。
    # 今回の条件はtrタグでclassがmtxになっているもの。
    rows = soup.findAll('tr',class_='mtx')

    # 表の最初の1~4行目はカラム情報なのでスライスする。
    rows = rows[4:]

    # 1日〜最終日までの１行を取得
    for row in rows:
        # trのなかのtdをすべて抜き出す
        data = row.findAll('td')

        #１行の中には様々なデータがあるので全部取り出す。
        rowData = [] #初期化
        rowData.append(str(year) + "/" + str(month) + "/" + str(data[0].string))
        rowData.append(str2float(data[3].string))
        rowData.append(str2float(data[6].string))
        rowData.append(str2float(data[7].string))
        rowData.append(str2float(data[8].string))
        rowData.append(str2float(data[9].string))
        rowData.append(str2float(data[10].string))
        rowData.append(str2float(data[16].string))

        #天気概況を取りたかったが、前半のコードを変更する必要があるためいったん取得しない
        # rowData.append(str2float(data[19].string))
        # rowData.append(str2float(data[20].string))

        #次の行にデータを追加
        All_list.append(rowData)

    df = pd.DataFrame(All_list[1:], columns=All_list[0])
    df['年月日'] = pd.to_datetime(df['年月日'])

    return df

def test(place, year, month):
    period = 30
    df_list = []
    print(place)
    print(year-period+1)

    for i in range(period):
        new_df = make_df(place, year-period+1+i, month)
        df_list.append(new_df)

    print(year)

    df_v = pd.concat(df_list[:-1], axis=0)

    #print("0:有意差なし、1:平均気温が高い、-1:平均気温が低い")

    #yearで指定した年の平均気温データの正規性判定
    static_year, pvalue_year = stats.shapiro(df_list[-1]["気温_平均"])

    #yearで指定した年から30年前までのデータの正規性判定
    static, pvalue = stats.shapiro(df_v["気温_平均"])

    #正規分布を仮定できる
    if pvalue_year > 0.05 and pvalue > 0.05:

        #バーレット検定で分散の検定を行う
        statistic, pvalue = stats.bartlett(df_list[-1]["気温_平均"], df_v["気温_平均"])

        #棄却できなかったため、等分散を仮定
        if pvalue > 0.05:
            statistic, pvalue = stats.ttest_ind(df_list[-1]["気温_平均"], df_v["気温_平均"], equal_var=True)

            #有意な差がなければ0を返す
            if pvalue >= 0.05:
                return 0

            else:
                statistic, pvalue = stats.ttest_ind(df_list[-1]["気温_平均"], df_v["気温_平均"], equal_var=True, alternative = "greater")
                #平均気温が大きい場合、1を返す
                if pvalue < 0.05:
                    return 1

                statistic, pvalue = stats.ttest_ind(df_list[-1]["気温_平均"], df_v["気温_平均"], equal_var=True, alternative = "less")
                #平均気温が小さい場合、-1を返す
                if pvalue < 0.05:
                    return -1

        #棄却できたため、等分散を仮定できない
        else:
            statistic, pvalue = stats.ttest_ind(df_list[-1]["気温_平均"], df_v["気温_平均"], equal_var=False)

            #有意な差がなければ、0を返す
            if pvalue >= 0.05:
                return 0

            else:
                statistic, pvalue = stats.ttest_ind(df_list[-1]["気温_平均"], df_v["気温_平均"], equal_var=False, alternative = "greater")
                #平均気温が大きい場合、1を返す
                if pvalue < 0.05:
                    return 1

                statistic, pvalue = stats.ttest_ind(df_list[-1]["気温_平均"], df_v["気温_平均"], equal_var=False, alternative = "less")
                #平均気温が小さい場合、-1を返す
                if pvalue < 0.05:
                    return -1

    #正規分布を仮定できない
    else:
        #正規分布を仮定できない為
        # Mann-Whitney(マンホイットニー)のU検定
        statistic, pvalue = stats.mannwhitneyu(df_list[-1]["気温_平均"], df_v["気温_平均"], alternative='two-sided')

        #有意な差がなければ0を返す
        if pvalue >= 0.05:
            return 0
        else:
            statistic, pvalue = stats.mannwhitneyu(df_list[-1]["気温_平均"], df_v["気温_平均"], alternative='greater')

            #平均気温が大きい場合、1を返す
            if pvalue <0.05:
                return 1
            statistic, pvalue = stats.mannwhitneyu(df_list[-1]["気温_平均"], df_v["気温_平均"], alternative='less')

            #平均気温が小さい場合、-1を返す
            if pvalue < 0.05:
                return -1

def make_result(region, place_list, year, month):
    result_list = [2] * 47
    i = 0

    for place in place_list:
        if region == "全国":
            result = test(place, year, month)
            result_list[i] = result

        if region == "北海道":
            result = test(place, year, month)
            result_list[0] = result

        if region == "東北":
            result = test(place, year, month)
            result_list[1+i] = result

        if region == "関東":
            result = test(place, year, month)
            result_list[7+i] = result

        if region == "中部":
            result = test(place, year, month)
            result_list[14+i] = result

        if region == "近畿":
            result = test(place, year, month)
            result_list[23+i] = result

        if region == "中国":
            result = test(place, year, month)
            result_list[30+i] = result

        if region == "四国":
            result = test(place, year, month)
            result_list[35+i] = result

        if region == "九州":
            result = test(place, year, month)
            result_list[39+i] = result
        i = i + 1

    return result_list

def convert_month(month):
    if month == "1":
        return "January"
    if month == "2":
        return "February"
    if month == "3":
        return "March"
    if month == "4":
        return "April"
    if month == "5":
        return "May"
    if month == "6":
        return "June"
    if month == "7":
        return "July"
    if month == "8":
        return "August"
    if month == "9":
        return "September"
    if month == "10":
        return "October"
    if month == "11":
        return "November"
    if month == "12":
        return "December"

def make_map(test_result, image, year, month):
    dict_pref = {}
    color_num = {0: "white", 1:"red", -1:"blue", 2:"green"}

    for i in range(47):
        dict_pref[pref_names[i+1]] = color_num[test_result[i]]
    plt.rcParams['figure.figsize'] = 6, 6
    plt.imshow(picture(dict_pref))
    plt.title("Average temperture in " + convert_month(month) + " of " + year)

    white_patch = mpatches.Patch(color='white', label='no difference')
    red_patch = mpatches.Patch(color='red', label='high')
    blue_patch = mpatches.Patch(color='blue', label='low')
    green_patch = mpatches.Patch(color='green', label='not applicable')
    #plt.legend(handles=[white_patch, red_patch, blue_patch], bbox_to_anchor=(1.35, 1.0))
    plt.legend(handles=[white_patch, red_patch, blue_patch, green_patch])
    plt.savefig(image)

def slice_list(region):
    if region == "全国":
        return place_list
    if region == "北海道":
        return hokkaido_list
    if region == "東北":
        return touhoku_list
    if region == "関東":
        return kanto_list
    if region == "中部":
        return tyubu_list
    if region == "近畿":
        return kinki_list
    if region == "中国":
        return tyugoku_list
    if region == "四国":
        return shikoku_list
    if region == "九州":
        return kyushu_list


def make_csv(place):

    df_list = []
    dt_now = datetime.datetime.now()

    for year in range(1970, dt_now.year):
        for month in range(1, 13):
            df = make_df(place, year, month)
            df_list.append(df)

    year = dt_now.year

    for month in range(1, dt_now.month+1):
        df = make_df(place, year, month)
        df_list.append(df)

    df_concat_multi = pd.concat(df_list)
    df_concat_multi.reset_index(drop=True).to_csv('/Users/ishiikenta/Library/CloudStorage/Dropbox/Mac/Desktop/気象庁HPデータ/data_' + place + '.csv', 
                                                index=False)