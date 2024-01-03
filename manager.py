from application import app, db
# 建立資料庫
def create_app():
    with app.app_context():
        db.create_all()
create_app() 
app.debug = True
app.run()