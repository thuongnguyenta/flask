

from flask import Flask,render_template, flash, redirect , url_for , session ,request, logging
from flask_mysqldb import MySQL
# from wtforms import Form, StringField , TextAreaField ,PasswordField , validators
# from passlib.hash import sha256_crypt
# from functools import wraps


app = Flask(__name__)
app.debug = True

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'thuong'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
# mysql.init_app(app)
# host='localhost'
# user = 'root'
# password = ''
# db = 'thuong'

@app.route('/update/<mail>',methods= ['GET','POST'])
def update(mail):
    if 'id' in session:
        cur =mysql.connection.cursor()
        username=request.form['name']
        number_phone =request.form['pn']
        cur.execute("UPDATE user SET user_name = %s, number_phone = %s WHERE mail = %s",(username,number_phone,mail)),
        mysql.connection.commit()
        return redirect(url_for('index'))
    return redirect(url_for('index'))




@app.route('/information/personal/<mail>')
def information(mail):
    if 'id' in session :
        cur =mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE mail=%s",[mail])
        rows = cur.fetchall()
        return    render_template('update.html',results=rows)
    return redirect(url_for('index'))


@app.route('/information/personal/changepass/<mail>')
def form(mail):
    if 'id' in session :
        cur =mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE mail=%s",[mail])
        # mysql.connection.commit()
        rows = cur.fetchall()
        return render_template('change_password.html',results=rows)


@app.route('/information/personal/changepassword/<mail>' ,methods= ['GET','POST'])
def change_password(mail):
    if 'id' in session :
        error=None
        cur =mysql.connection.cursor()
        old_pass=request.form['old_pass']
        new_pass =request.form['new_pass']
        confirm_new_pass =request.form['confirm_new_pass']
        cur.execute("SELECT * FROM user WHERE mail=%s",[mail])
        # mysql.connection.commit()
        rows = cur.fetchall()
        old_pass_database = rows[0]['password']
        if old_pass == old_pass_database and new_pass==confirm_new_pass :
            cur.execute("UPDATE user SET password = %s WHERE mail = %s",(new_pass,mail))
            mysql.connection.commit()
            
            return render_template('update.html',results=rows)
        else:
            error="Sai mk hoặc hai mật khẩu không trùng khớp"
            return render_template('change_password.html',results=rows,error=error)


@app.route('/')
def dashboard():
    return render_template('dashboard.html')

def is_login():
    if 'id' in session:
    #   username = session['username']
         return render_template('user.html')
    return render_template('login.html')
# def home():
#     return render_template('index.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')
# def chalamgi():
#     return render_template('index.html')


@app.route('/login',methods= ['GET','POST'])
def login():
    error=None
    if request.method == 'POST':
        
        email=request.form['tk']
            # username=request.form['username']
        password =request.form['mk']
        cur =mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE mail=%s and password=%s",(email,password))
        rows = cur.fetchall()
        if len(rows) ==0:
            error="Sai tai khoan hoac mat khau"
            return render_template('login.html',error=error)
        else:
            session['id'] = rows[0]['user_name']
            session['role'] = rows[0]['role']
            if int(session['role']) > 2 :
                return redirect(url_for('display_pr'))
            return redirect(url_for('manager_product'))
            # return "Login success !"
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.clear()
    # session.pop('id',None)
    # session.pop('role',None)
    return redirect(url_for('dashboard'))

# @app.route('/xtlogin', methods = [ 'POST','GET'])
# def xtlogin():
#    error = None
   
#    if request.method == 'POST':
#     #   if request.form['username'] != 'admin' or \
#     #      request.form['password'] != 'admin':
#     #      error = 'Invalid username or password. Please try again!'
#     #   else:
#     #     #  flash('You were successfully logged in')
#     #     #  return redirect(url_for('index'))
#     #     return "Done !"
    
#         email=request.form['tk']
#             # username=request.form['username']
#         password =request.form['mk']
#         cur =mysql.connection.cursor()
#         cur.execute("SELECT * FROM user WHERE mail=%s and password=%s",(email,password))
#         rows = cur.fetchall()
#         if len(rows) ==0:
#             error="Sai tai khoan hoac mat khau"
#             return render_template('login.html',error=error)
#         else : 
#             return "Done!"
			
#    return render_template('login.html', error = "không biết !")

@app.route('/index')
# @is_login
def index():
    
    if 'id' in session and int(session['role'])<3:

        cur =mysql.connection.cursor()
        cur.execute("SELECT * FROM user")
        rows = cur.fetchall()
        cur.close()
        return render_template('index.html',results=rows)
    return render_template('login.html')
        # return result


@app.route('/register',methods=['POST','GET'])
def register():
    error= None
    if request.method == 'POST':
        email=request.form['email']
        username=request.form['username']
        password =request.form['password']
        password_confirm =request.form['cppassword']
        if password != password_confirm :
            error= "Mat khau khong trung khop"
            return render_template('register.html',errors=error)
        cur =mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE mail=%s",(email,))
        rows = cur.fetchall()
        # return rows
        if len(rows) !=0 :
            error = "Email da ton tai"
            return render_template('register.html',errors=error)
        else:
            cur.execute('INSERT INTO user(mail,user_name,password,role,number_phone) VALUES(%s,%s,%s,%s,%s)',(email,username,password,3,123))
            mysql.connection.commit()
            # return render_template('login.html',email=email,password=password)
            return render_template('login.html',email=email,password=password)

# @app.route('/register')
# def regis() :
#     return render_template('register.html',errors=None)


@app.route('/regis')
def regis():
    return render_template('register.html')

@app.route('/delele/<mail>')
def delele(mail):
    if 'id' in session and int(session['role']) ==1:

        cur =mysql.connection.cursor()
        cur.execute("DELETE FROM user WHERE mail=%s",[mail])
        mysql.connection.commit()
        # rows = cur.fetchall()
        return redirect(url_for('index'))
    return "Bạn không có quyền"

@app.route('/update_infor/<mail>')
def update_infor(mail):
    if 'id' in session:
        cur =mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE mail=%s",[mail])
        # mysql.connection.commit()
        rows = cur.fetchall()
        return render_template('update.html',results=rows)


        



@app.route('/product')
def display_pr():
    
    cur =mysql.connection.cursor()
    cur.execute("SELECT * FROM product")
    rows = cur.fetchall()
    return    render_template('product.html',products=rows)

@app.route("/product/add")
def display_add():
    if 'id' in session and int(session['role']) ==1:
        cur =mysql.connection.cursor()
        cur.execute("SELECT * FROM catalogy")
        rows = cur.fetchall()
        return render_template('add_product.html', catalogy=rows)
    return redirect(url_for('display_pr'))

@app.route("/product/add_product_handle",methods=['POST','GET'])
def add_product_handle():
    if 'id' in session and int(session['role']) <3:
        cur =mysql.connection.cursor()
        product_name=request.form['product_name']
        product_cost =request.form['product_cost']
        product_quanlity=request.form['product_quanlity']
        product_catalogy =request.form['product_catalogy']
        cur.execute('INSERT INTO product(product_id,product_name,cost,quanlity,catalogy_id) VALUES(%s,%s,%s,%s,%s)',("NULL",product_name,product_cost,product_quanlity,product_catalogy))
        mysql.connection.commit()
        return redirect(url_for('display_pr'))
    return redirect(url_for('manager_product'))


@app.route('/product/manage_product')
def manager_product():
    if 'id' in session and int(session['role']) ==1:
        cur=mysql.connection.cursor()  
        cur.execute("SELECT * FROM product")
        rows = cur.fetchall()
        return    render_template('manage_product.html',products=rows)
@app.route('/product/detail/<product_id>')
def detail(product_id):
    cur =mysql.connection.cursor()
    cur.execute("SELECT * FROM product WHERE product_id =%s",[product_id]),
    rows = cur.fetchall()
    return    render_template('product_detail.html',product_detail=rows)


if __name__ == '__main__':
    # app.secret_key='secret134'
    app.run()
