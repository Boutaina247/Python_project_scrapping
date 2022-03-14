import json
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource,request
import json
app = Flask(__name__)
api = Api(app)

import MySQLdb

class Dbconnect(object):

    def __init__(self):

        self.dbconection = MySQLdb.connect(host='localhost',
                                           port=3306,
                                           user='root',
                                           passwd='boutaina',
                                           db='librarydb')
        self.dbcursor = self.dbconection.cursor()

    def commit_db(self):
        self.dbconection.commit()

    def close_db(self):
        self.dbcursor.close()
        self.dbconection.close()

db = Dbconnect()


class HelloWorld(Resource):
    def get(self,_id):
        db = Dbconnect()
        req = f'select * from librarydb.library where id = {_id}'
        print(req)
        db.dbcursor.execute(req)
        results = db.dbcursor.fetchall()
        results = results[0]
        return {"index":results[0],"titles":results[1],"notations":results[2],"pieces":results[3],"availability":results[4]}
    
    def delete(self,_id):
        #lib.query.filter(lib.id == 2).delete()
        req = f'delete from librarydb.library where id ={_id}'
        db.dbcursor.execute(req)
        db.commit_db()
        
    def post(self, _id):
        val = request.json
        print(val)
        req = f'insert into librarydb.library (titles, notations, prices, availability) values("{val["titles"]}","{val["notations"]}",{val["prices"]},"{val["availability"]}")'
        db.dbcursor.execute(req)
        db.commit_db()

    def put(self,_id):
        vid= request.json
        print(type(vid))
        print(_id)
        # print(request.json)
        print(vid)
        req = f'Update librarydb.library SET titles = "{vid["titles"]}", notations = "{vid["notations"]}", prices = {vid["prices"]}, availability = "{vid["availability"]}" WHERE id = {int(_id)}'
        db.dbcursor.execute(req)
        db.commit_db()
         

    def apropos(self):
        return("ceci est streamlit fait appartir dun script capable d interroger l api de la base de données pour afficher les données sur un  Dashboard type streamlit. Link : https://books.toscrape.com/")   

         
api.add_resource(HelloWorld, '/record/<_id>')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)