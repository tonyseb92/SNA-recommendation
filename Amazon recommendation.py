# -*- coding: utf-8 -*-

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

#Assuming the customer purchases a book with the following ASIN (adjustable)
print ("Looking for Recommendations for Customer Purchasing this Book:")
print ("--------------------------------------------------------------")
purchasedAsin = '0805047905'

# Getting metadata associated with this book
print ("ASIN = ", purchasedAsin) 
print ("Title = ", amazonBooks[purchasedAsin]['Title'])
print ("SalesRank = ", amazonBooks[purchasedAsin]['SalesRank'])
print ("TotalReviews = ", amazonBooks[purchasedAsin]['TotalReviews'])
print ("AvgRating = ", amazonBooks[purchasedAsin]['AvgRating'])
print ("DegreeCentrality = ", amazonBooks[purchasedAsin]['DegreeCentrality'])
print ("ClusteringCoeff = ", amazonBooks[purchasedAsin]['ClusteringCoeff'])
    
# Creating ego network associated with purchasedAsin in the
# copurchaseGraph - which is esentially comprised of all the books 
# that have been copurchased with this book in the past

purchasedAsinEgoGraph = networkx.ego_graph(copurchaseGraph, purchasedAsin, radius = 1 )


# Edge weights in the copurchaseGraph is a measure of
# the similarity between the books connected by the edge.
#Retaining only those books that are highly similar to the purchasedAsin

threshold = 0.5
purchasedAsinEgoTrimGraph = networkx.Graph()
for f, t, e in purchasedAsinEgoGraph.edges(data = True):
    if e['weight'] >= threshold:
        purchasedAsinEgoTrimGraph.add_edge(f,t,e)

# getting list of nodes connected to the purchasedAsin by a single 
# hop (called the neighbors of the purchasedAsin) 

purchasedAsinNeighbors = purchasedAsinEgoTrimGraph.neighbors(purchasedAsin)

# The Top Five book recommendations from among the 
# purchasedAsinNeighbors based on the following data of the 
# neighboring nodes: SalesRank, AvgRating, TotalReviews, and DegreeCentrality.
# (ClusteringCoeff not used in this project, and commented out)

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

# Here we adjust/normalize the scales for sales rank, number of reviews, and degree of centrality

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
