from flask import Blueprint,flash,render_template,redirect,url_for,session,request
from others_mod.forms import RegisterForm,LoginForm
from others_mod.con import get_connection
import bcrypt


auth_bp = Blueprint("auth",__name__) #name - help flask find recources like templates, static file

@auth_bp.route("/")
def index():

    user_login = session.get("user_id")

    if user_login:
        return redirect(url_for("task.view_task"))
        #show user profile
    return render_template("index.html")


# register
@auth_bp.route("/register",methods = ["POST","GET"])
def register():

    form = RegisterForm()

    if form.validate_on_submit(): #ensure the request is state-changing

        name = form.name.data
        email = form.email.data
        password = form.password.data

        con = get_connection()

        if con:
            try:
                cursor = con.cursor()

                hashpw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())   

                query = ("INSERT INTO users(name,email,password) VALUES(%s,%s,%s)")
                data = (name,email,hashpw)
                cursor.execute(query,data)
                con.commit()

                # add user id in session
                query = ("SELECT * FROM users WHERE email = %s")
                data = (email,)
                cursor.execute(query,data)
                user_data = cursor.fetchone()

                session["user_id"] = user_data[0]
                flash("You SignUp Successfuly!","success")

                
            finally:
                con.close()
                cursor.close()
                return redirect(url_for("task.view_task"))
            
        else:
            flash("connection Error", "alert")
            return render_template("register.html", form = form)
    print("else")
    return render_template("register.html",form = form)


# login
@auth_bp.route("/login", methods = ["POST","GET"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data

        con = get_connection()

        if con:
            try:
                cursor = con.cursor()
                query = ("SELECT * FROM users WHERE email = %s")
                data = (email,)
                cursor.execute(query,data)
                record = cursor.fetchone()

                if record and bcrypt.checkpw(password.encode('utf-8'),record[3].encode('utf-8')):

                    session["user_id"] = record[0]
                    
                    flash("Login Successfuly!", "success")

                    return redirect(url_for("task.view_task"))
                
                flash("Invalid credential.", "alert")
                return render_template("login.html",form = form)
                
            finally:
                con.close()
                cursor.close()
        else:
            flash("Connection Unavilable.","alert")
            # return
    else:
        return render_template("login.html",form = form)


# logout
@auth_bp.route("/logout")
def logout():
        session.pop("user_id",None)

        flash("Logged out successfuly.", "success")
        return redirect(url_for("auth.index"))
    

