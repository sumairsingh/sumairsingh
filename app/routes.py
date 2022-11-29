from operator import eq
from optparse import Values
from textwrap import indent
from flask import render_template, redirect, url_for, request
from app import app
from app.forms import SearchForm
import requests
import json


@app.route('/search', methods=['POST', 'GET'])
def search():
    form = SearchForm()
    token = request.args["token"]

    headers = {"Authorization": "Bearer "+token,
               "Ocp-Apim-Subscription-Key": "3d6ae2f7ea11414680fdc693433ddb8c"}
    if form.validate_on_submit():
        body = {"guid": form.search.data}
        response = requests.get(
            url="https://gif-apim-sandbox.glblint.pwcinternal.com/concourse-search-qa/v2/getusercontext", params=body, headers=headers)
        if response.status_code == 401:
            return redirect("/index")
        values = response.json()
        # modifying the code from here
        json_data = [
            {'enablingtechnology': i['enablingtechnology'], 'guid': i['guid'], 'integratedsolution': i['integratedsolution'], 'los': i['los'], 'platform': i['platform'], 'role': i['role'], 'staffclass': i['staffclass']} for i in values]

        return render_template('kms.html', form=form, results=values)
        # return redirect(url_for("results", results=values))
    return render_template('kms.html', form=form)


@app.route('/')
@app.route('/index')
def index():
    body = {"client_id": "US_Leap_Dev",
            "client_secret": "pwc12345",
            "username": "US_adv_Leap_s001",
            "password": "12E11g21111L8rD81WkQ",
            "grant_type": "password",
            "scope": "openid email profile",
            "auth_chain": "oauthServiceAccount"
            }

    headers = {"Content-type": "application/x-www-form-urlencoded"}
    response = requests.post(
        url="https://login-stg.pwc.com/openam/oauth2/access_token", headers=headers, data=body)
    token = response.json()["access_token"]
    return redirect(url_for("search", token=token))


@app.route('/results', methods=['POST', 'GET'])
def results():

    results = request.args["results"]
