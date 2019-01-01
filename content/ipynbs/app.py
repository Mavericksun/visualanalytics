
from UTCDAL.Utilities.Math import gma
from UTCDAL.Deploy.WebService.json_relate import api_function 

from flask import Flask, render_template, url_for, request, session
import os

app = Flask(__name__)
app.secret_key = 'F12Zr47j3yXR~X@H!jLwf/T'

@app.route('/', methods=['GET','POST'])
@api_function
def gma_(**input_):
    return gma(**input_)

@app.after_request
def add_header(r):
    '''
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    '''
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
