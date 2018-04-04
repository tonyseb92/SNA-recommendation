# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 10:29:32 2016

@author: hina
"""
print ()

import networkx
from operator import itemgetter
import matplotlib.pyplot

# Read the data from the amazon-books.txt;
# populate amazonProducts nested dicitonary;
# key = ASIN; value = MetaData associated with ASIN
fhr = open('./amazon-books.txt', 'r', encoding='utf-8', errors='ignore')
amazonBooks = {}
fhr.readline()
for line in fhr:
    cell = line.split('\t')
    MetaData = {}
    MetaData['Id'] = cell[0].strip() 
    ASIN = cell[1].strip()
    MetaData['Title'] = cell[2].strip()
    MetaData['Categories'] = cell[3].strip()
    MetaData['Group'] = cell[4].strip()
    MetaData['SalesRank'] = int(cell[5].strip())
    MetaData['TotalReviews'] = int(cell[6].strip())
    MetaData['AvgRating'] = float(cell[7].strip())
    MetaData['DegreeCentrality'] = int(cell[8].strip())
    MetaData['ClusteringCoeff'] = float(cell[9].strip())
    amazonBooks[ASIN] = MetaData
fhr.close()

# Read the data from amazon-books-copurchase.adjlist;
# assign it to copurchaseGraph weighted Graph;
# node = ASIN, edge= copurchase, edge weight = category similarity
fhr=open("amazon-books-copurchase.edgelist", 'rb')
copurchaseGraph=networkx.read_weighted_edgelist(fhr)
fhr.close()

# Now let's assume a person is considering buying the following book;
# what else can we recommend to them based on copurchase behavior 
# we've seen from other users?
print ("Looking for Recommendations for Customer Purchasing this Book:")
print ("--------------------------------------------------------------")
purchasedAsin = '0805047905'

# Let's first get some metadata associated with this book
print ("ASIN = ", purchasedAsin) 
print ("Title = ", amazonBooks[purchasedAsin]['Title'])
print ("SalesRank = ", amazonBooks[purchasedAsin]['SalesRank'])
print ("TotalReviews = ", amazonBooks[purchasedAsin]['TotalReviews'])
print ("AvgRating = ", amazonBooks[purchasedAsin]['AvgRating'])
print ("DegreeCentrality = ", amazonBooks[purchasedAsin]['DegreeCentrality'])
print ("ClusteringCoeff = ", amazonBooks[purchasedAsin]['ClusteringCoeff'])
    
# Now let's look at the ego network associated with purchasedAsin in the
# copurchaseGraph - which is esentially comprised of all the books 
# that have been copurchased with this book in the past
# (1) YOUR CODE HERE: 
#     Get the depth-1 ego network of purchasedAsin from copurchaseGraph,
#     and assign the resulting graph to purchasedAsinEgoGraph.
purchasedAsinEgoGraph = networkx.ego_graph(copurchaseGraph, purchasedAsin, radius = 1 )


# Next, recall that the edge weights in the copurchaseGraph is a measure of
# the similarity between the books connected by the edge. So we can use the 
# island method to only retain those books that are highly simialr to the 
# purchasedAsin
# (2) YOUR CODE HERE: 
#     Use the island method on purchasedAsinEgoGraph to only retain edges with 
#     threshold >= 0.5, and assign resulting graph to purchasedAsinEgoTrimGraph
threshold = 0.5
purchasedAsinEgoTrimGraph = networkx.Graph()
for f, t, e in purchasedAsinEgoGraph.edges(data = True):
    if e['weight'] >= threshold:
        purchasedAsinEgoTrimGraph.add_edge(f,t,e)

# Next, recall that given the purchasedAsinEgoTrimGraph you constructed above, 
# you can get at the list of nodes connected to the purchasedAsin by a single 
# hop (called the neighbors of the purchasedAsin) 
# (3) YOUR CODE HERE: 
#     Find the list of neighbors of the purchasedAsin in the 
#     purchasedAsinEgoTrimGraph, and assign it to purchasedAsinNeighbors
purchasedAsinNeighbors = purchasedAsinEgoTrimGraph.neighbors(purchasedAsin)

# Next, let's pick the Top Five book recommendations from among the 
# purchasedAsinNeighbors based on one or more of the following data of the 
# neighboring nodes: SalesRank, AvgRating, TotalReviews, DegreeCentrality, 
# and ClusteringCoeff
# (4) YOUR CODE HERE: 
#     Note that, given an asin, you can get at the metadata associated with  
#     it using amazonBooks (similar to lines 49-56 above).
#     Now, come up with a composite measure to make Top Five book 
#     recommendations based on one or more of the following metrics associated 
#     with nodes in purchasedAsinNeighbors: SalesRank, AvgRating, 
#     TotalReviews, DegreeCentrality, and ClusteringCoeff 

salesrank = {}
totalreviews = {}
avgratings = {}
dc =  {}
#clusteringcoefflist = {}

for asin in purchasedAsinNeighbors:
    salesrank[asin] = amazonBooks[asin]['SalesRank']
    totalreviews[asin] = amazonBooks[asin]['TotalReviews']
    avgratings[asin] = amazonBooks[asin]['AvgRating']
    dc[asin] = amazonBooks[asin]['DegreeCentrality']
#    clusteringcoefflist.append(amazonBooks[asin]['ClusteringCoeff'])

#here we adjust/normalize the scales for sales rank, number of reviews, and degree of centrality

normsalesrank = {}
for asin,v in salesrank.items():
    normsalesrank[asin] = 6-(5*v+20000)/(v+20000)
    
normtotalreviews = {}
for asin,v in totalreviews.items():
    normtotalreviews[asin] = (5*v+2)/(v+2)

normdc = {}
for asin,v in dc.items():
    normdc[asin] = (5*v+5)/(v+5)

weighted = {}
for asin in purchasedAsinNeighbors:
    weighted[asin] = round(normsalesrank[asin]*0.3 + normtotalreviews[asin]*0.2 + avgratings[asin]*0.4 + normdc[asin]*0.1,2)

weightedlist = []
for k,v in weighted.items():
    weightedtup = (k,v)
    weightedlist.append(weightedtup)

weightedlist = sorted(weightedlist, key=itemgetter(1), reverse = True)

# Print Top 5 recommendations (ASIN, and associated Title, Sales Rank, 
# TotalReviews, AvgRating, DegreeCentrality, ClusteringCoeff)
# (5) YOUR CODE HERE:  

top5asin = []
top5 = {}
for n in range(5):
    top5asin.append(weightedlist[n][0])
for asin in top5asin:
    innerdic = {}
    innerdic['Title'] = amazonBooks[asin]['Title']
    innerdic['SalesRank'] = amazonBooks[asin]['SalesRank']
    innerdic['TotalReviews'] = amazonBooks[asin]['TotalReviews']
    innerdic['AvgRating'] = amazonBooks[asin]['AvgRating']
    innerdic['DegreeCentrality'] = amazonBooks[asin]['DegreeCentrality']
    innerdic['ClusteringCoeff'] = amazonBooks[asin]['ClusteringCoeff']
    
    top5[asin] = innerdic
    
print("--------------------------------------------------------------")
print("The top 5 recommendations are:")
print()
print(top5)
