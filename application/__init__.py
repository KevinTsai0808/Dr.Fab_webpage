from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os

#  取得啟動文件資料夾路徑
dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# 密碼加密
bcrypt = Bcrypt(app)
login = LoginManager(app)
# 'login'是指router  
login.login_view = 'login'
# 修改@login_required的預設flash訊息
login.login_message =  "請先登入才能訪問此頁面"
# create database相關設置
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_RECORD_QUERIES"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  設置資料庫為sqlite3(到時候再設定成其他)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(dir, 'static/data/data_register.sqlite')
app.config['SECRET_KEY']='kevin0808'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
from  application.author import view