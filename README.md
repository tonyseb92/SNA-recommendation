# SNA-recommendation

In this project, I used Amazon product co-purchase data to make book recommendations using Social Network Analysis in Python. The recommendations are chosen based on their scores in a composite measure of four metrics (Sales Rank, Total Reviews, Average Rating, DegreeCentrality - although Clustering Coefficient is also available, I have not considered this metric in the composite measure), using the networkx package.
I used the Amazon Meta-Data Set maintained on the SNAP site. This data set is comprised of product and review metdata on 548,552 different products. The data was collected in 2006 by crawling the Amazon website. 

The first step we have to perform is read, preprocess, and format this data for further analysis. The Python script called PreprocessAmazonBooks.py (created by Dr. Hina Arora at ASU) takes the “amazon-meta.txt” file as input, and performs the following steps:

•	Parse the amazon-meta.txt file

•	Preprocess the metadata for all ASINs, and write out the following fields into the amazonProducts Nested Dictionary (key = ASIN and value = MetaData Dictionary associated with ASIN):
o	Id: same as “Id” in amazon-meta.txt
o	ASIN: same as “ASIN” in amazon -meta.txt
o	Title: same as “title” in amazon-meta.txt
o	Categories: a transformed version of “categories” in amazon-meta.txt. Essentially, all categories associated with the ASIN are concatenated, and are then subject to the following Text Preprocessing steps: lowercase, stemming, remove digit/punctuation, remove stop words, retain only unique words. The resulting list of words is then placed into “Categories”.
o	Copurchased: a transformed version of “similar” in amazon-meta.txt. Essentially, the copurchased ASINs in the “similar” field are filtered down to only those ASINs that have metadata associated with it. The resulting list of ASINs is then placed into “Copurchased”.
o	SalesRank: same as “salesrank” in amazon-meta.txt
o	TotalReviews: same as total number of reviews under “reviews” in amazon-meta.txt
o	AvgRating: same as average rating under “reviews” in amazon-meta.txt

•	Filter amazonProducts Dictionary down to only Group=Book, and write filtered data to amazonBooks Dictionary

•	Use the co-purchase data in amazonBooks Dictionary to create the copurchaseGraph Structure as follows:
o	Nodes: the ASINs are Nodes in the Graph
o	Edges: an Edge exists between two Nodes (ASINs) if the two ASINs were co-purchased
o	Edge Weight (based on Category Similarity): since we are attempting to make book recommendations based on co-purchase information, it would be nice to have some measure of Similarity for each ASIN (Node) pair that was co-purchased (existence of Edge between the Nodes). We can then use the Similarity measure as the Edge Weight between the Node pair that was co-purchased. We can potentially create such a Similarity measure by using the “Categories” data, where the Similarity measure between any two ASINs that were co-purchased is calculated as follows:
Similarity = (Number of words that are common between Categories of connected Nodes)/
		(Total Number of words in both Categories of connected Nodes)
The Similarity ranges from 0 (most dissimilar) to 1 (most similar).

•	Add the following graph-related measures for each ASIN to the amazonBooks Dictionary:
o	DegreeCentrality: associated with each Node (ASIN)
o	ClusteringCoeff: associated with each Node (ASIN)

•	Write out the amazonBooks data to the amazon-books.txt file (all except copurchase data – because that data is now in the copurchase graph)

•	Write out the copurchaseGraph data to the amazon-books-copurchase.edgelist file
