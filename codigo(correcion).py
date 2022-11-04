import folium
from folium.plugins import MiniMap
import pandas as pd
import networkx as nx

points = []

class configData:
    def __init__(self,file,sep=";"):
        self._data=""
        if file[-4:]==".csv":
            self._data = pd.read_csv(file,sep=";")
        if file[-5:]==".json":
            self._data = pd.read_json(file)
    def getData(self):
        return self._data

class graphX():
    """
    create graph with pandas data
    """
    def __init__(self,data):
        self.graph=nx.Graph()
        for i in range(len(data)):
            node=data["node"][i]
            weight=(data["harassmentRisk"][i]+0.5)*data["length"][i]
            #weight=(data["length"][i])
            self.graph.add_edge(str(data["edges"][i][0]),str(data["edges"][i][1]),weight=weight)
            self.graph.add_node(str(node))

class pathsX(graphX):
    def __init__(self,data,source,target,graphtype):
        super().__init__(data)
        self._source=source
        self._target=target
    def dijkstra(self):
        self._nodes=nx.dijkstra_path(self.graph, self._source, self._target, weight='weight')
    def getData(self):
        """
        return data from shorts path algoritms
        """
        #pathdf=pd.DataFrame([{"name":"path","path":[eval(i) for i in self._nodes]}])
        #print(self._nodes)
        nodesNew=[]
        for i in self._nodes:
            iarr=eval(i)
            nodesNew.append([iarr[1],iarr[0]])
        return nodesNew


def validData(txt:str,dicts:list)-> bool:
 
  tmp=False
  for i in txt:
    if not i in dicts:
      tmp=False
      break
    else:
      tmp=True
  return tmp

data=configData("https://raw.githubusercontent.com/jero98772/AlOtroLado/main/core/data/medellin_data.json").getData()
validateTxt="1234567890.,- []'"
source=input("de donde va(ejemplo:[-75.5764695, 6.2011545]):\n")#"[-75.5764695, 6.2011545]"
target=input("a donde va(ejemplo:[-75.5805063, 6.247958]):\n")#"[-75.5805063, 6.247958]"#
if target=="" or source=="" or  not (validData(target,validateTxt) and  validData(source,validateTxt)):
    print("Datos invalidos")
else:
    newPath=pathsX(data,str(source), str(target),graphX)
    newPath.dijkstra()
    nodesData=newPath.getData()
    #print(nodesData)
    FormatData= tuple(map(tuple, nodesData))
    #print(FormatData)
    points = list(FormatData)
    
print(points)
    
mapaentero=folium.Map(location=[6.256405968932449, -75.59835591123756],zoom_start=13)
folium.PolyLine(points).add_to(mapaentero)
mapaentero
