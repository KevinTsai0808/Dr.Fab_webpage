from flask import render_template, flash, redirect, request, url_for
from application import app, db
from application.author.model import UserRegister
from application.author.form import FormRegister, FormLogin
from flask_login import login_user, current_user, login_required, logout_user

@app.route('/register', methods=['GET', 'POST'])
# 註冊頁面（之後加上註冊成功後送出註冊信）
def register():
    form = FormRegister()
    if form.validate_on_submit():
        form.on_submit()
        flash('請至信箱完成註冊並獲取密碼')
        return render_template('index.html')
    return render_template('register.html', form=form)

@app.route('/verify_registration/<token>', methods=['GET'])
def verify_registration(token):
    user = UserRegister.query.filter_by(verification_token=token).first_or_404()
    if not user.verified:
        user.verified = True
        db.session.commit()
    flash('註冊已完成！')
    return redirect(url_for('login'))

@app.route('/')  
def index():  
    return render_template('index.html')  

# 登入頁面
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        #  當使用者按下login之後，先檢核帳號是否存在系統內以及是否驗證。
        user = UserRegister.query.filter_by(username=form.username.data).first()
        if user and user.verified:  
            #  當使用者存在資料庫內再核對密碼是否正確。
            if user.check_password(form.password.data):
                #  加入login_user，第二個參數是記得我的參數
                login_user(user, form.remember_me.data)
                next = request.args.get('next')
                #  自定義一個驗證的function來確認使用者是否確實有該url的權限
                if not next_is_valid(next):
                    #  如果使用者沒有該url權限，那就reject掉。
                    return 'Bad Boy!!'
                return redirect(next or url_for('index'))
            else:
                #  如果密碼驗證錯誤，就顯示錯誤訊息。
                flash('公司統編或密碼錯誤')
        else:
            #  如果資料庫無此帳號，就顯示錯誤訊息。
            flash('公司統編或密碼錯誤')
    return render_template('login.html', form=form)
  
def next_is_valid(url):
    return True


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已成功登出')
    return redirect(url_for('login'))  
  
  
@app.route('/userinfo')  
def userinfo():  
    return 'Here is UserINFO'



