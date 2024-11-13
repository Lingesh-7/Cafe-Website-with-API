from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class AddCafe(FlaskForm):
    name=StringField("Cafe Name:",validators=[DataRequired()])
    map_url=StringField("Cafe Location URL",validators=[DataRequired(),URL()])
    img_url=StringField("Cafe Image URL",validators=[DataRequired(),URL()])
    location=StringField("Location Place",validators=[DataRequired()])
    wifi=StringField("Wifi Availabel?T/F",validators=[DataRequired()])
    sockets=StringField("Sockets is there or not?T/F",validators=[DataRequired()])
    toilets=StringField("Toilet is there or not?T/F",validators=[DataRequired()])
    call=StringField("Can we take calls or not?T/F",validators=[DataRequired()])
    seats=StringField("No.of Seats",validators=[DataRequired()])
    price=StringField("Price of Coffee",validators=[DataRequired()])
    submit=SubmitField("Submit")



class UpdateForm(FlaskForm):
    creditenls=StringField("Enter Cafe Id:",validators=[DataRequired()])
    price=StringField("Price of Coffee",validators=[DataRequired()])
    submit=SubmitField("Update")



class DeleteForm(FlaskForm):
    ids=StringField("Cafe Id:",validators=[DataRequired()])
    creditals=StringField("Enter Creditals:",validators=[DataRequired()])
    submit=SubmitField("Delete")

class Search(FlaskForm):
    serach=StringField(validators=[DataRequired()])
    submit=SubmitField("search")