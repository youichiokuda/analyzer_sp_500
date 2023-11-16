from flask import Blueprint, render_template, request
from .stock_analyzer import analyze_stock
from .forms import StockForm

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = StockForm()
    if form.validate_on_submit():
        results = analyze_stock(form.days.data, form.drop.data, form.jump.data, form.pernumber.data)
        return render_template('results.html', results=results)
    return render_template('index.html', form=form)
