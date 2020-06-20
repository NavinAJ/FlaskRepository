from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT,jwt_required
from user import UserRegister
from item import Item, ItemList

from security import authenticate,identity

app = Flask(__name__)
app.secret_key = "FalconDZ"
api = Api(app)

jwt = JWT(app,authenticate,identity) #/auth



api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    app.run(debug=True,port=5000)