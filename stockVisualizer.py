from flask import Flask, render_template, request, flash
import pygal, requests
from datetime import datetime

def getData(timeSeries, symbol):
    # populate the query parameters
    queryData = {'function': '', 'symbol': '', 'interval': '', 'apikey': ''}
    queryData['function'] = timeSeries
    queryData['symbol'] = symbol
    queryData['apikey'] = "QY73AL7RJZDQESXX"
    if (timeSeries == "TIME_SERIES_INTRADAY"):
        queryData['interval'] = "15min"

    alphavantageRequest = requests.get('https://www.alphavantage.co/query', params=queryData)
    if alphavantageRequest.status_code == 200:
        stocksDictionary = alphavantageRequest.json()
        return stocksDictionary
    else:
        flash("Error: Request failed")

def generateGraph(symbol, timeSeries, chart, stocksDictionary, startDate, endDate):
    timeSeriesKeys = list(stocksDictionary.keys())
    if len(timeSeriesKeys) > 1:
        timeSeriesName = list(stocksDictionary)[1]
        timeSeriesData = stocksDictionary[timeSeriesName]

        displayStartDate = startDate.strftime("%Y/%m/%d")
        displayEndDate = endDate.strftime("%Y/%m/%d")
        graphTitle = f"Stock Data for {symbol}: {displayStartDate} to {displayEndDate}"

        if (chart == "Line"):
            finalGraph = generateLineGraph(timeSeries, timeSeriesData, startDate, endDate, graphTitle)
            return finalGraph
        if (chart == "Bar"):
            finalGraph = generateBarChart(timeSeries, timeSeriesData, startDate, endDate, graphTitle)
            return finalGraph
    else:
        flash("Error: No data in the stocksDictionary")

def generateLineGraph(timeSeries, timeSeriesData, startDate, endDate, graphTitle):
    graphLines = ["1. open", "2. high", "3. low", "4. close"]

    lineGraph = pygal.Line(title=graphTitle, x_label_rotation=45, x_value_formatter=lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S'))

    for line in graphLines:
        dataPoints = list()
        x_labels = list()
        for date, values in timeSeriesData.items():
            if (timeSeries == "TIME_SERIES_INTRADAY"):
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            else:
                date = datetime.strptime(date, "%Y-%m-%d")
            if date > startDate and date < endDate:
                if (timeSeries == "TIME_SERIES_INTRADAY"):
                    x_labels.insert(0, date.strftime("%Y/%m/%d %H:%M:%S"))
                else:
                    x_labels.insert(0, date.strftime("%Y/%m/%d"))
                y = float(values[line])
                dataPoints.append(y)
        lineGraph.add(line, dataPoints)
    lineGraph.x_labels = x_labels

    return lineGraph

def generateBarChart(timeSeries, timeSeriesData, startDate, endDate, graphTitle):
    chartLabels = ["1. open", "2. high", "3. low", "4. close"]
    barChart = pygal.Bar(title=graphTitle, x_label_rotation=45)

    for label in chartLabels:
        x_labels = list() 
        dataPoints = list() 
        for date, values in timeSeriesData.items():
           
            if (timeSeries == "TIME_SERIES_INTRADAY"):
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            else:
                date = datetime.strptime(date, "%Y-%m-%d")
          
            if date > startDate and date < endDate: 
                if (timeSeries == "TIME_SERIES_INTRADAY"):
                    x_labels.insert(0, date.strftime("%Y/%m/%d %H:%M:%S"))
                else:
                    x_labels.insert(0, date.strftime("%Y/%m/%d"))
                y = float(values[label])
                dataPoints.append(y)
        barChart.add(label, dataPoints)
    barChart.x_labels = x_labels
    
    return barChart