"""
The huginn.web.api module contain the api calls for the front-end
"""

from flask import jsonify, abort

from huginn.web import app
from huginn.http import WebClient

@app.route("/api/ins_data")
def ins_data():
    """Returns the inertial navigation system data"""
    web_client = WebClient(app.config["huginn_host"],
                           app.config["huginn_web_port"])

    try:
        ins_data = web_client.get_ins_data()
    except Exception:
        abort(500)

    return jsonify(ins_data)
