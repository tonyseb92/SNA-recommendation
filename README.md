# SNA-recommendation

Used Amazon product co-purchase data to make book recommendations using Social Network Analysis in Python. The recommendations are chosen based on their scores in a composite measure of four metrics (Sales Rank, Total Reviews, Average Rating, DegreeCentrality - although Clustering Coefficient is also available, I have not considered this metric in the composite measure), using the networkx package.
