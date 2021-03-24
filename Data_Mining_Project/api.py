from SPARQLWrapper import SPARQLWrapper,JSON
from flask import Flask, render_template
from flask_bootstrap import Bootstrap



#opening the queries we have definded previously 
query_lyon = open("./Query/Query_Lyon.txt",'r').read()
query_rennes = open("./Query/Query_Rennes.txt",'r').read()
query_mtp = open("./Query/Query_Montpellier.txt",'r').read()

app = Flask(__name__)
Bootstrap(app)

@app.route("/",methods=["GET","POST"])
def Hello():
    return render_template('welcome.html') 

@app.route("/lyon",methods = ["GET","POST"])
def lyon():
    return render_template('map.html',name = 'Lyon',datas = grab_query(send_query(query_lyon)),center = (45.759060, 4.847331))

@app.route("/rennes",methods = ["GET","POST"])
def rennes():
    return render_template('map.html',name = 'Rennes',datas = grab_query(send_query(query_rennes)))
@app.route("/mtp",methods = ["GET","POST"])
def mtp():
    return render_template('map.html',name = 'Montpellier',datas = grab_query(send_query(query_mtp)))

def send_query(query):
    sparql = SPARQLWrapper('http://localhost:3030/Bike_stands')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def grab_query(query):
    res = list()
    for element in query['results']['bindings']:
        temp = list()
        temp.append(element['ville']['value'])
        temp.append(element['name']['value'])
        temp.append(element['available_bikes']['value'])
        temp.append(element['available_bikes_stands']['value'])
        temp.append(element['bike_stands']['value'])
        
        res.append(temp)
        
        
    return res
       

if __name__ == '__main__':
    #print((grab_query(send_query(query_mtp))))
    app.run(port=3000)
    