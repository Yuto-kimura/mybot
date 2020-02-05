from flask import Flask, request, render_template, redirect, url_for, jsonify, abort
from datetime import datetime
import ipaddress, os, sys, traceback, json
from werkzeug.datastructures import ImmutableMultiDict

# from sql import exec_get_sql, exec_post_sql
from sql import exec_post_sql
from sql import SQLExceptionError
# from api import exec_api
# from api import APIExceptionError


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# config = configparser.ConfigParser()
# config.read('config.ini')

# def get_request(keyword):
#     try:
#         response = exec_get_sql(keyword)
#         return response
#     except ValueError as e:
#         t, v, tb = sys.exc_info()
#         print(str(traceback.format_exception(t,v,tb)))
#         print(str(traceback.format_tb(e.__traceback__)))
#         abort(400, e)

### >>> data = request.data(dict)
def post_request(data):
    try:
        response = exec_post_sql(data)
        return response
    except ValueError as e:
        t, v, tb = sys.exc_info()
        print(str(traceback.format_exception(t,v,tb)))
        print(str(traceback.format_tb(e.__traceback__)))
        abort(400, e)


### エラーハンドリング
@app.errorhandler(400)
def error_bad_request(error):
    response = {
        'type':str(error),
        'msg':"不正なリクエストです. 再度入力した情報をご確認ください."
    }
    return render_template('access_failed.html', msg=response), 400

@app.errorhandler(404)
def error_not_found(error):
    response = {
        'type':str(error),
        'msg':"ページが見つかりませんでした. URLを再度ご確認ください."
    }
    return render_template('access_failed.html', msg=response), 404

### メインページ
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/yurubot/api/post', methods=['POST'])
def post_api_request():
    if request.method == 'POST':
        ### binary -> dict
        data = request.data.decode('utf-8')
        response = post_request(json.loads(data))
        return response
    else:
        abort(400, 'Unexpected request method.')

# @app.route('/yurubot/api/get/<keyword>', methods=['GET'])
# def get_api_request(keyword):
#     print("############# "+str(keyword))
#     if request.method == 'GET':
#         response = dict(get_request(keyword))
#         return response
#     else:
#         abort(400, 'Unexpected request method.')

def main():
    app.run()

if __name__ == "__main__":
    main()
