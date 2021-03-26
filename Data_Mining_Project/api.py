from SPARQLWrapper import SPARQLWrapper,JSON
from flask import Flask, render_template
from flask_bootstrap import Bootstrap



#opening the queries we have definded previously 
query_lyon = open("./Query/Query_Lyon_final.txt",'r').read()
query_rennes = open("./Query/Query_Rennes_final.txt",'r').read()
query_mtp = open("./Query/Query_Montpellier_final.txt",'r').read()

app = Flask(__name__)
Bootstrap(app)

@app.route("/",methods=["GET","POST"])
def Hello():
    return render_template('welcome.html') 

@app.route("/lyon",methods = ["GET","POST"])
def lyon():
    return render_template('map_lyon.html',name = 'Lyon',datas = grab_query(send_query(query_lyon)))

@app.route("/rennes",methods = ["GET","POST"])
def rennes():
    return render_template('map_rennes.html',name = 'Rennes',datas = grab_query(send_query(query_rennes)))

@app.route("/mtp",methods = ["GET","POST"])
def mtp():
    return render_template('map_mtp.html',name = 'Montpellier',datas = grab_query(send_query(query_mtp)))

def send_query(query):
    sparql = SPARQLWrapper('http://localhost:3030/Final_Station_Bike')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def grab_query(query):
    res = list()
    for element in query['results']['bindings']:
        temp = list()
        temp.append(element['owlville']['value'])
        temp.append(element['owlname']['value'])
        temp.append(element['owlavailable_bikes']['value'])
        temp.append(element['owlavailable_bikes_stands']['value'])
        temp.append(element['owlbike_stands']['value'])
        if query=="query_rennes":
            temp.append(float(element['owllat']['value'][0:-2])*10)
            temp.append(float(element['owllong']['value'][0:-2]))
        else:
            temp.append(float(element['owllat']['value'][0:-2]))
            temp.append(float(element['owllong']['value'][0:-2]))
        res.append(temp)
        
        
    return res
       

if __name__ == '__main__':
    #   f = open('/Users/Arthur/Desktop/Projets/DataMiningStands/Data_Mining_Project/Data/q.txt','w')
    #   l = grab_query(send_query(query_rennes))
    #   f.write(str(l))
    #   f.close()
    #app.run(port=3000)
    print(grab_query(send_query(query_mtp)))
    
    