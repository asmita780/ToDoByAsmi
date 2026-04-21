from flask_wtf import FlaskForm #used to simplie web forms

from wtforms import StringField,PasswordField,SubmitField

from wtforms.validators import DataRequired,Email,ValidationError
from others_mod.con import get_connection



class RegisterForm(FlaskForm):
    name = StringField("Name", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired(),Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField("Signup")

    def validate_email(self,field):

        con = get_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s",(field.data,))
        user = cursor.fetchone()

        con.close()
        cursor.close()

        if user:
            raise ValidationError("Email is already taken.")


class LoginForm(FlaskForm):
    email = StringField("Email",validators = [DataRequired(),Email()])
    password = PasswordField("Password",validators = [DataRequired()])
    submit = SubmitField("Login")

class TaskForm(FlaskForm):
    title = StringField("Title",validators = [DataRequired()])
    submit = SubmitField("Add")