from flask import Flask, render_template, request, flash
from test import *

app = Flask(__name__, static_folder='./static')
image = "static/images/japanmap.png"

@app.route('/', methods=['GET', 'POST'])
def index():
    title = "気象庁のデータ可視化"

    try:
        if request.method == 'POST':
            region = request.form['region']
            year = request.form['year']
            month = request.form['month']

        else:
            region = request.args.get('region')
            year = request.args.get('year')
            month = request.args.get('month')

        return render_template("index.html", title=title, region=region, year=year, month=month)
    except Exception as e:
        return render_template("index.html", title=title, region="地方の取得に失敗", year="年の取得に失敗", month="月の取得に失敗")

@app.route('/temperture', methods=['GET', 'POST'])
def temperture():
    title = "地方別の過去の平均気温との有意さのマッピング"

    try:
        if request.method == 'POST':
            region = request.form['region']
            year = request.form['year']
            month = request.form['month']

        else:
            region = request.args.get('region')
            year = request.args.get('year')
            month = request.args.get('month')

        return render_template("temperture.html", title=title, region=region, year=year, month=month)
    except Exception as e:
        return render_template("temperture.html", title=title, region="地方の取得に失敗", year="年の取得に失敗", month="月の取得に失敗")


@app.route('/map', methods=["POST", "GET"])
def map():
    title = "地方別の過去の平均気温との有意さのマッピング"

    if request.method == 'POST':
        region = request.form['region']
        year = request.form['year']
        month = request.form['month']

    else:
        region = request.args.get('region')
        year = request.args.get('year')
        month = request.args.get('month')

    test_result = make_result(str(region), slice_list(str(region)), int(year), int(month))
    make_map(test_result, image, year, month)

    return render_template("map.html", title=title, region=region, year=year, month=month, image=image)

@app.route('/load', methods=["POST"])
def load():
    title = "地方別の過去の平均気温との有意さのマッピング"

    return render_template()

@app.route('/visual', methods=["POST"])
def visual():
    title = "地方別の過去の平均気温のデータ可視化"

    return render_template("visual.html")

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host="localhost", port=3000)