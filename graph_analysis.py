from graphing.news_graph import NewsGraph
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities


if __name__ == "__main__":
    ng = NewsGraph()
    G = ng.graph
    
#     Basic Graph Analysis
# Node and Edge Count: Count the number of nodes and edges in a graph.
    print(G)
    
    eccentricity = nx.eccentricity(G)
    print("Eccentricity:", eccentricity)
    diameter = nx.diameter(G)
    print("Diameter:", diameter)
    
    # Compute radius
    radius = nx.radius(G)
    print("Radius:", radius)
    
    center = nx.center(G)
    print("Center:", center)

#     Centrality Analysis
# Degree Centrality: Measures the importance of a node based on its degree.
# Betweenness Centrality: Measures the number of times a node acts as a bridge.
# Centrality measures
    # print("____________CENTRALITY__________________________")
    # degree_centrality = nx.degree_centrality(G)
    # betweenness_centrality = nx.betweenness_centrality(G)

    # print("Degree Centrality:", degree_centrality)
    # print("Betweenness Centrality:", betweenness_centrality)

# Community Detection
# Detect clusters or groups in the graph (e.g., using modularity).
    # print("____________COMMUNITIES__________________________")

    # communities = list(greedy_modularity_communities(G))
    # print("Communities:", len([list(community) for community in communities]))
    



    
    