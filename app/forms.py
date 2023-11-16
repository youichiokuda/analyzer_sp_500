from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired

class StockForm(FlaskForm):
    days = IntegerField('何日さかのぼる?', validators=[DataRequired()])
    drop = IntegerField('下落率は？', validators=[DataRequired()])
    jump = IntegerField('上昇率は?', validators=[DataRequired()])
    pernumber = IntegerField('PERは幾つ以下にする？', validators=[DataRequired()])
    submit = SubmitField('分析')
