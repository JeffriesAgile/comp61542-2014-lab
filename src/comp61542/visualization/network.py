__author__ = 'dumbastic'

import networkx as nx
import matplotlib.pyplot as plt


import json
from networkx.readwrite import json_graph

class PublicationNetwork():
    def generateNetwork(self):
        G=nx.random_geometric_graph(200,0.125)
        # position is stored as node attribute data for random_geometric_graph
        pos=nx.get_node_attributes(G,'pos')

        # find node near center (0.5,0.5)
        dmin=1
        ncenter=0
        for n in pos:
            x,y=pos[n]
            d=(x-0.5)**2+(y-0.5)**2
            if d<dmin:
                ncenter=n
                dmin=d

        # color by path length from node near center
        p=nx.single_source_shortest_path_length(G,ncenter)

        plt.figure(figsize=(8,8))
        nx.draw_networkx_edges(G,pos,nodelist=[ncenter],alpha=0.4)
        nx.draw_networkx_nodes(G,pos,nodelist=p.keys(),
                               node_size=50,
                               node_color=p.values(),
                               cmap=plt.cm.Reds_r)

        plt.xlim(-0.05,1.05)
        plt.ylim(-0.05,1.05)
        plt.axis('off')
        plt.savefig('comp61542/static/publication_network.png')

# import http_server

class D3JsonGraph():
    def __init__(self, G, filename):
        self.G = G
        # this d3 example uses the name attribute for the mouse-hover value,
        # so add a name to each node
        # write json formatted data
        d = json_graph.node_link_data(self.G) # node-link format to serialize
        # write json
        json.dump(d, open('../src/comp61542/static/js/' + filename + '.json','w'))
        print('Wrote node-link JSON data to js/' + filename + '.json')
        # open URL in running web browser
        # http_server.load_url('force/force.html')
        print('Or copy all files in force/ to webserver and load force/force.html')

        # pos=nx.spring_layout(G)
        # # nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
        # node_labels = nx.get_node_attributes(G,'name')
        # nx.draw(G,pos,node_color='#A0CBE2',node_size=0,font_size=16,labels=node_labels)
        # # nx.draw(G,pos,node_color='#A0CBE2',width=4,edge_cmap=plt.cm.Blues,with_labels=False)
        # plt.savefig('comp61542/static/images/' + filename + '.png')
        # # plt.show()


