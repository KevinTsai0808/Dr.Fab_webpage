from application import db, login, bcrypt
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
@login.user_loader  
def load_user(user_id):  
    return UserRegister.query.get(int(user_id))

class UserRegister(UserMixin, db.Model):
    """記錄使用者資料的資料表"""
    # tanlename沒設定會以類別名稱作為資料表名稱
    __tablename__ = 'UserRegister'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    verification_token = db.Column(db.String(100), unique=True)
    verified = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf8')
        
    def check_password(self, password):
        """
        密碼驗證，驗證使用者輸入的密碼跟資料庫內的加密密碼是否相符
        :param password: 使用者輸入的密碼
        :return: True/False
        """
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return 'username:%s, email:%s' % (self.username, self.email)