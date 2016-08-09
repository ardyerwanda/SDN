from multiprocessing import Lock #multi procecing pembuatan thred
from pyretic.lib.query import *
from pyretic.core import *
from pyretic.lib.corelib import *
from pyretic.lib.std import *

def build_dic(sip,dip,path):#tetep bro
    dic={}
    dic[sip]={dip:path}
    return dic

class  build_path():
    def __init__(self,topology,switch,dstswitch,dstport,wG=None):
        self.topology=topology
        self.srcswitch=switch
        self.dstswitch = dstswitch
        self.dstport = dstport
        self.wG = wG
	print "<<<>>>"
	print self.topology
	print self.srcswitch
	print self.dstswitch
	print self.dstport
	print self.wG
	print "<<<>>>"
    def bellford_routing(self):
        pathlist=[]

        #print self.topology
        pred, totalcost = self.bellford_alg(self.topology,str(self.srcswitch),self.wG)
        if pred:
            v = self.dstswitch
            print "Asal  : Node ", self.srcswitch
            print "Tujuan: Node ", self.dstswitch
            while(v != self.srcswitch):
                pathlist.append(Location(pred[v],self.topology[pred[v]][v][pred[v]]))
                v = pred[v]
            print "pathlist <<switch[port]>>: "
            for a in reversed(pathlist):
                print a, "->",
            print Location(self.dstswitch,self.dstport)
            pathlist.append(Location(self.dstswitch,self.dstport))
            print "Total cost: ", totalcost

        return pathlist

    def bellford_alg(self,G,source,wG=None,huge=1e30000):#G:topology
        theClock0 = time.time()
        pred={}
        predIndic={}
        routeTable={}
        routeTable2={}
        route={}

        #print (G.edge)
        if wG == None:
            RT=0
            for RT in G.edge:
                routeTable[RT]={}
                for u in G.edge:
                    routeTable[RT][u]={}
                    route[u]={}
                    for v in G.edge:
                        #print type(v)
                        #print G.has_edge
                        if u==RT and G.has_edge(u,v):
                            route[u][v] = 1 #setting weight
                            route[u][u]=0
                        elif u==v and v==RT:
                            route[u][v]=0
                        else:
                            route[u][v]=huge
                        routeTable[RT][u][v]=route[u][v]
                print "table node",RT,": ", routeTable[RT]
                print " "
            routeTable2 = copy.deepcopy(routeTable) #backup
        else:
            routeTable  = copy.deepcopy(wG) #weightGraph
            routeTable2 = copy.deepcopy(wG) #backup
            for RT in G.edge:
                print "table node",RT,": ", routeTable[RT]

        for k in G.edge:
            predIndic[k] = huge #nilai awal yang besar agar dapat dibandiingakan dengan nilai yang lebih kecil

        sameTable = False # nilai awal  utk indikator bahwa tabel routing tdk sama
        while not sameTable: #checking table change, if any change, transfer table to neighbor 
            sameIndic = 0 #sering berubah #indikator penyamaan namun yg bukan tabel
            for x in G.edge: #
                for y in G.edge:
                    for z in G.edge:
                        if G.has_edge(x,y) and (routeTable[x][x][z] < routeTable[y][x][z]): #tetangga, bandingkan tabel asal dan tetangga

                            routeTable[y][x][z] = copy.deepcopy(routeTable[x][x][z]) # copy tabel yg kecil

                            routeTable[y][y][z] = min(routeTable[y][y][z],routeTable[y][y][x]+routeTable[y][x][z]) #rumus bro..

                            sameIndic = sameIndic + 1# peringan tabel dicek berapa kali, mengecek seluruh tabel dann melakukan update
            print "<<<<<<UPDATE>>>>>>>"
            for RT in G.edge: #monitoring update
                print "table node",RT,": "
                for RT2 in G.edge:
                    print RT2," to ",routeTable[RT][RT2]
                    print RT2," ke ",routeTable2[RT][RT2]
                    for RT3 in G.edge:
                        if RT3 == self.srcswitch and (routeTable[RT][RT2][RT3] + routeTable2[RT][RT][RT2])<predIndic[RT] and (RT != RT2):
                            pred[RT] = RT2 #update pred
                            predIndic[RT]=copy.deepcopy(routeTable[RT][RT2][RT3] + routeTable2[RT][RT][RT2])#nilai ttp  #menghitung jarak ke tetangga yang nnt dijumlahkn ke total cost
                        if RT == self.srcswitch and RT3 == self.dstswitch and RT == RT2:
                            totalcost = routeTable[RT][RT2][RT3] #menghitung total cost

                print " "
            if sameIndic == 0: sameTable = True# jika indikator same indic =0 maka same tabel benar atau sudah sama
        print pred
        print "Waktu Eksekusi: ",time.time() - theClock0
        return pred,totalcost

class build_flowtable(DynamicPolicy):

    def __init__(self,dic, weight = None):

        self.weight = weight
        self.switch = None
        self.port = None
        self.forward = drop
        self.dic=dic
        self.topology = drop
        super(build_flowtable,self).__init__()

    def set_network(self, network):
        if not network is None:
            for sip in self.dic.keys():
                for dip in self.dic[sip].keys():
                    for loc in self.dic[sip][dip]:
                        self.forward = if_(match(switch = loc.switch, srcip=sip,dstip=dip),fwd(loc.port_no),self.forward)
            self.policy = self.forward
            #print "policy ",
            #print self.policy

