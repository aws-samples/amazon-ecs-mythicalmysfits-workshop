from flask import Flask, jsonify, json, Response, request
from flask_cors import CORS
import mysfitsTableClient
import os

app = Flask(__name__)
CORS(app)

# The service basepath has a short response just to ensure that healthchecks
# sent to the service root will receive a healthy response.
@app.route("/")
def healthCheckResponse():
    flaskResponse = Response(response='{"message" : "Nothing here, used for health check. Try /mysfits instead."}', status=200)
    flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse

# Retrive mysfits from DynamoDB based on provided querystring params, or all
# mysfits if no querystring is present.
@app.route("/mysfits", methods=['GET'])
def getMysfits():

    filterCategory = request.args.get('filter')
    if filterCategory:
        filterValue = request.args.get('value')
        queryParam = {
            'filter': filterCategory,
            'value': filterValue
        }
        serviceResponse = mysfitsTableClient.queryMysfits(queryParam)
    else:
        serviceResponse = mysfitsTableClient.getAllMysfits()

    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse

def process_like_request():
    print('Like processed.')

# retrieve the full details for a specific mysfit with their provided path
# parameter as their ID.
@app.route("/mysfits/<mysfit_id>", methods=['GET'])
def getMysfit(mysfit_id):
    serviceResponse = mysfitsTableClient.getMysfit(mysfit_id)

    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse

# increment the number of likes for the provided mysfit.
@app.route("/mysfits/<mysfit_id>/like", methods=['POST'])
def likeMysfit(mysfit_id):
    serviceResponse = mysfitsTableClient.likeMysfit(mysfit_id)
    process_like_request()
    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"
    return flaskResponse

# @app.route("/mysfits/<mysfit_id>/fulfill-like", methods=['POST'])
# def likeMysfit(mysfit_id):
#     serviceResponse = mysfitsTableClient.likeMysfit(mysfit_id)
#     flaskResponse = Response(serviceResponse)
#     flaskResponse.headers["Content-Type"] = "application/json"
#     return flaskResponse

# indicate that the provided mysfit should be marked as adopted.
@app.route("/mysfits/<mysfit_id>/adopt", methods=['POST'])
def adoptMysfit(mysfit_id):
    serviceResponse = mysfitsTableClient.adoptMysfit(mysfit_id)

    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse

# Run the service on the local server it has been deployed to,
# listening on port 8080.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
