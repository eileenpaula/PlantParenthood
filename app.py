from flask import Flask, render_template
app = Flask('FullCalendar Demo')

events = [
    {
        'plant': 'plant1',
        'todo': 'TBA TBA TBA TBA TBA TBA',
        'date': '2023-07-26',
    },
    {
        'plant': 'plant2',
        'todo': 'TBA',
        'date': '2023-07-28',
    },
]

@app.route('/')
def calendar():
    return render_template('calendar.html', events=events)