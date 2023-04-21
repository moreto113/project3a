from flask import Flask, render_template, request, url_for, flash, redirect, abort
import stockVisualizer
import symbols
from datetime import datetime


# make a Flask application object called app
app = Flask(__name__)
app.config['DEBUG'] = True


#flash the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

# route for the stock user input form
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == "GET":
        sp500_symbols = symbols.getSP500SymbolsFromWiki()

        return render_template('stocks.html', sp500_symbols=sp500_symbols)

    if request.method == "POST":

        symbol = request.form["symbol"]
        chart_type = request.form["chart_type"]
        time_series = request.form["time_series"]
        date_format = "%Y-%m-%d"
        start_date_str = request.form.get("start_date")
        start_date = datetime.strptime(start_date_str, date_format) if start_date_str else None
        end_date_str = request.form.get("end_date")
        end_date = datetime.strptime(end_date_str, date_format) if end_date_str else None
        #If form is empty, flash error
        if symbol == "":
            flash("Symbol is required.")
        elif(chart_type == ""):
            flash("Chart Type is required.")
        elif(time_series == ""):
            flash("Time Series is required.")
        elif(start_date is None):
            flash("Start Date is required.")
        elif(end_date is None):
            flash("End Date is required.")
        elif(end_date <= start_date):
            flash("End Date must be after Start Date.")
        else:
            sp500_symbols = symbols.getSP500SymbolsFromWiki()
            stocksData = stockVisualizer.getData(time_series, symbol)
            graph = stockVisualizer.generateGraph(symbol, time_series, chart_type, stocksData, start_date, end_date)
            graph_svg = graph.render().decode('utf-8').strip()
            return render_template('stocks.html', sp500_symbols=sp500_symbols, graph_svg=graph_svg)
        sp500_symbols = symbols.getSP500SymbolsFromWiki()
        return render_template('stocks.html', sp500_symbols=sp500_symbols)
    return render_template('stocks.html')
app.run(host="0.0.0.0")