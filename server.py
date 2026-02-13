from flask import Flask, request
import requests
from db import Reservations

app = Flask(__name__)

@app.route('/')
def hello():
    rows = list(Reservations.select().dicts())
    if not rows:
        return 'Hello, world!<br><br>No data.'
    html = 'Hello, world!<br><br><table border="1"><tr>'
    for col in rows[0]:
        html += f'<th>{col}</th>'
    html += '</tr>'
    for row in rows:
        html += '<tr>' + ''.join(f'<td>{v}</td>' for v in row.values()) + '</tr>'
    html += '</table>'
    return html

if __name__ == '__main__':
    app.run(debug=True, port=5003)