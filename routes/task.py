from flask import Flask,Blueprint,flash,render_template,request,redirect,url_for,session
from others_mod.forms import TaskForm
from others_mod.con import get_connection
from others_mod.count import task_done

task_bp = Blueprint("task",__name__)

@task_bp.route("/view_task", methods = ["POST","GET"])
def view_task():
        
        user_id = session.get("user_id")
        if user_id:
                
            form = TaskForm()

            conx = get_connection()

            if conx:
                try:
                    cursor = conx.cursor()
                    cursor.execute("SELECT * FROM tasks")
                    all_task = cursor.fetchall()

                finally:
                    conx.close()
                    cursor.close()

                    if all_task:

                        count = task_done(all_task)
                        
                        return render_template("view_task.html",form = form,tasks=all_task, c = count)
                        
                    return render_template("view_task.html",form = form)
                    
            flash("Connection not avalible! data didn't saved.", "alert")
            return render_template("view_task.html",form = form)
        
        return redirect(url_for('auth.login'))

@task_bp.route("/add", methods = ["POST", "GET"])
def add():
    
    form = TaskForm()

    if form.validate_on_submit():
        
        title = form.title.data

        con = get_connection()

        if con:
            # try:
                cursor = con.cursor()

                query = ("INSERT INTO tasks(title,status) VALUES(%s,%s)")
                data = (title,"pandding")

                cursor.execute(query,data)
                con.commit()

            # finally: 
                cursor.close()
                con.close()
                return redirect(url_for("task.view_task"))

        flash("Connection not avalible","alert")

    return render_template("view_task.html",form = form)


@task_bp.route("/update_status/<int:task_id>", methods = ["POST", "GET"])
def update_status(task_id):

    if request.method == "POST":

        conx = get_connection()
    
        if conx:

            try:
                query = ("SELECT * FROM tasks WHERE task_id = %s")
                data = (task_id,)

                cursor = conx.cursor()
                cursor.execute(query,data)
                task = cursor.fetchone()

                if task[2] == "pandding":
                    status = "working"
                elif task[2] == "working":
                    status = "done"
                else:
                    status = "pandding"


                query = ("UPDATE tasks SET status = %s WHERE task_id = %s")
                data = (status,task_id)
                cursor.execute(query,data)
                conx.commit()

            finally:
                conx.close()
                cursor.close()

                return redirect(url_for("task.view_task"))
            
    return redirect(url_for("task.view_task"))


@task_bp.route("/clear_tasks", methods = ["POST","GET"])
def clear_tasks():
    if request.method == "POST":

        conx = get_connection()
        if conx:

            try:
                cursor = conx.cursor()
                cursor.execute("DELETE FROM tasks")
                conx.commit()

            finally:
                conx.close()
                cursor.close()

                flash("All tasks cleared", "success")
                return redirect(url_for("task.view_task"))
            
    return redirect(url_for("task.view_task"))


