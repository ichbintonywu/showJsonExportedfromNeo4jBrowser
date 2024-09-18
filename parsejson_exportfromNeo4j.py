

import json
import pandas as pd
import streamlit as st
from pathlib import Path
from streamlit_agraph import agraph, Node, Edge, Config
import random

st.set_page_config(
    page_title="Display JSON File",
    page_icon="🚀",
    layout="wide",
)

def get_random_color_name(color_names):
    return random.choice(color_names)

def display_Agraph(tuple_list,labels_list):
    nodes_color_names = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "brown", "cyan", "magenta", "gray"]
    rel_color_names = "blue"

    label_color_mapping = {}

    def get_color_for_label(label):
        return label_color_mapping.get(label, "red")

    for label in labels_list:
        if label not in label_color_mapping:
            label_color_mapping[label] = get_random_color_name(nodes_color_names)

    # print(label_color_mapping)
    nodes = []
    edges = []
    blacklist =[]

    config = Config(height=600,
                    width=1200, 
                    nodeHighlightBehavior=True,
                    highlightColor="#F7A7A6", 
                    directed=True, 
                    collapsible=True)
    for index, tpl in enumerate(tuple_list):
        start_node, end_node, relationship = tpl  
        start_id, start_labels = start_node      # Unpacking the start node tuple
        end_id, end_labels = end_node
        id0 = start_node
        id1 = end_node      
        if id0 not in blacklist:
            blacklist.append(id0)
            node1= Node(id=start_id,size=25, label=start_labels,title=start_labels,color=get_color_for_label(start_labels[0]))
            nodes.append(node1)
        if id1 not in blacklist:
            blacklist.append(id1)
            node2= Node(id=end_id,size=29, label=end_labels,title=end_labels,color=get_color_for_label(end_labels[0]))
            nodes.append(node2)
        rel = Edge(source=start_id,target=end_id,label=relationship,size=20,type="CURVE_SMOOTH",color=rel_color_names)
        edges.append(rel)

    agraph(nodes,edges,config)

def get_tuple_from_json(jsonfile):

    with open(jsonfile, 'r',encoding='utf-8-sig') as file:
        data = json.load(file)

        tuple_list = []

        labels_list = []           

        for item in data:
            path = item["path"]
            
            # Loop through each segment in the path
            for segment in path["segments"]:
                start_node = segment["start"]
                end_node = segment["end"]
                relationship = segment["relationship"]

                if start_node["labels"][0] not in labels_list:
                    labels_list.append(start_node["labels"][0])
                if end_node["labels"][0] not in labels_list:
                    labels_list.append(end_node["labels"][0])                    
                
                # Create a tuple with start node, end node, and relationship type
                tuple_list.append((
                    (start_node["identity"], start_node["labels"]),
                    (end_node["identity"], end_node["labels"]),
                    relationship["type"]
                ))

        return tuple_list, labels_list

st.title('DataFrame Display for the JSON file exported from Neo4j Browser')
st.markdown("**Please fill the below form :**")
with st.form(key="Choose a json file exported from Neo4j Browser", clear_on_submit = False):
    File = st.file_uploader(label = "Upload file", type=["json"])

    if st.form_submit_button("Upload the JSON File"):
            save_folder = './'
            save_path = Path(save_folder, File.name)
            with open(save_path, mode='wb') as w:
                w.write(File.getvalue())
            with open(File.name, 'r',encoding='utf-8-sig') as file:
                data = json.load(file)
                df = pd.DataFrame(data)
                pd.set_option('display.max_colwidth', None) 

                st.dataframe(df,use_container_width=True)

                tuple_list, labels_list = get_tuple_from_json(File.name)
                display_Agraph(tuple_list,labels_list) 

