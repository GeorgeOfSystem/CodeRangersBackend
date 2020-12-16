from flask import Flask, jsonify, request
from firebase import firebase
import json

firebase = firebase.FirebaseApplication("https://coderangersproject.firebaseio.com/", None)

app = Flask(__name__)

@app.route('/')
def index():
    return 'OPTIONS:<br><b>GET</b> <br> /formularios <br> /formularios/{ownerId}'

#GET
@app.route('/formularios/<string:oid>')
def getProductsByOwnerId(oid):
    forms = firebase.get('/formularios', '')
    result = []
    for f in forms:
        if forms[f]['ownerId'] == oid:
            result.append([f, forms[f]])
            
    if len(result) == 0:
        return jsonify({"message":"Usuario no existente"})
    return  jsonify(result)

@app.route('/formularios')
def getForms():
    return firebase.get('/formularios', '')
    
    
#POST    
@app.route('/formularios', methods = ['POST'])
def addForm():
    firebase.post('/formularios', request.json)
    return jsonify({"message":"Recieved"})

#PUT
@app.route('/formularios/<string:fid>', methods = ['PUT'])
def updateForm(fid):
    firebase.put('/formularios',fid, request.json)
    return jsonify({"message":"Updated"})

#DELETE
@app.route('/formularios/<string:fid>', methods = ['DELETE'])
def deleteForm(fid):
    firebase.delete('/formularios', fid)
    
    if fid != "":
        return jsonify({"message":"Deleted"})
    
    return jsonify({"message":"No Form Found"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)