import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    # used for controlling the input argument from the api request.
    # it allows only required arg to pass through.
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help="This field cannot be left blank!")
    parser.add_argument('quantity',type=str,required=True,help="This field cannot be left blank!")


    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.Connection("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()

        if row:
            return{'item':{'name':row[0],'price':row[1],'quantity':row[2]}}

    # require authentication inorder to continue with the below request.
    @jwt_required()
    def get(self,name):
        item = self.find_by_name(name)
        if item:
            return item
        return{'message':"Item not found"},404
    
    
    def post(self,name):

        if self.find_by_name(name):
            return {'Message':f"This item {name} is already exist"},400

        requestData = Item.parser.parse_args()
        newItem = {
            'name'  : name,
            'price' : requestData['price'],
            'quantity' : requestData['quantity']
        }
        try:
            self.insert(newItem)
        except:
            return {"message":"An error occured while trying to insert an item in DB"},500
        return f"{newItem} is successfully added to the list",201

    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?,?,?)"
        cursor.execute(query,(item['name'],item['price'],item['quantity']))

        connection.commit()
        connection.close()


    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))

        connection.commit()
        connection.close()
        
        return f"Item {name} is deleted from DB"

    def put(self,name):
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item={"name":name,"price":data['price'],"quantity":data['quantity']}
        if item is None :
            try:
                self.insert(updated_item)
            except:
                return {"message":"Error while trying to insert data into DB"},500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message":"Error while trying to update data into DB"},500

        return updated_item

    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=?,quantity=? WHERE name=?"
        cursor.execute(query,(item['price'],item['quantity'],item['name']))

        connection.commit()
        connection.close()



class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        item = []
        for row in result:
            item.append({"name":row[0],"price":row[1],"quantity":row[2]})

        connection.close()
        return {"item":item}

        