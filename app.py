from io import StringIO, BytesIO

import pandas as pd
from flask import Flask, render_template, request
from flask import send_file

import services

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        df = pd.read_csv(file)
        df_lat_lng = services.convert_csv_with_cep_to_latitude_longitude(df)
        proxyIO = StringIO()
        df_lat_lng.to_csv(proxyIO, index=False, encoding="utf-8")
        mem = BytesIO()
        mem.write(proxyIO.getvalue().encode("utf-8"))
        mem.seek(0)
        return send_file(
            mem,
            mimetype="text/csv",
            attachment_filename='cep-lat-lng',
            as_attachment=True,
            cache_timeout=0,
        )
    else:
        print('No file to process! Please upload a file to process.')
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
