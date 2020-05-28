import pandas as pd
import networkx as nx
import os
import collections

# The script in front of you does 2 things:
#       a) Generate a file in gexf format with a list of edges.
#       b) generate a table of nodes in xlsx format that you can import into gephi.
# Both documents share the element "id", so Gephi is able to associate the nodes
# generated from the aristar document,  and the node table with the set of attributes.

def grapher():
    files = os.listdir("data/")                                  # Open All files in directory "data" and list them
    frames = []                                                  # Create an empty list to append data

    for file in files:                                           # Loop over files
        df = pd.read_csv("data/canada/"+file, decimal=",")       # Transform csv content into a Dataframe
        frames.append(df)                                        # Now we have a list of Dataframes

    all_data = pd.concat(frames)                                 # Concatenate all Dataframes to a single Dataset

    all_data["target"] = all_data['URL'].str.split('//', 1).str[1].str.split("/").str[0]  # Split "URL" col to "target".

    graph = nx.from_pandas_edgelist(all_data, source="Keyword", target="target")          # NX Function generate edges

    # EXPORT THE EDGES GEXF FILE
    nx.write_gexf(graph, "edgest_table.gexf", encoding='utf-8', prettyprint=True)

    # EXPORT FULL DATASET (You can comment the line below, if you don't need this file
    all_data.to_excel("final_frame.xlsx")

    # Generate a Nodes Table with attributes

    # First, generate table with SITES attributes
    unique_sites = collections.Counter(all_data["target"]) # How many unique sites are in dataset?
    sites_dataset = pd.DataFrame.from_dict(unique_sites, orient="index", columns=["frequency"]).reset_index()
    sites_dataset["id"] = sites_dataset["index"]
    sites_dataset["Type"] = "landing"
    sites_dataset.drop(["index"], inplace=True, axis=1)

    # Then, generate a table with keywords attributes
    keywords_dataset = all_data.drop_duplicates(["Keyword"]).reset_index()
    keywords_dataset["id"] = keywords_dataset["Keyword"]

    # DROP columns! (you can include or exclude columns here
    keywords_dataset.drop(["Keyword", "index", "#", "Ads Title", "Last Update", "Block", "URL", "target", "Ads URL", "Ads Title", "Ads Description"], inplace=True, axis=1)
    keywords_dataset["Type"] = "keyword"

    # Concatenate both Datasets
    frames = [sites_dataset, keywords_dataset]
    nodes_table = pd.concat(frames)

    nodes_table.to_excel("nodes_table.xlsx")
    print("boilá!")

grapher()



