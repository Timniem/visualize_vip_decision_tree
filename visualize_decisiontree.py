import json
import graphviz
import argparse

def create_flowchart(json_data, bottom_nodes=[]):
    dot = graphviz.Digraph(
        graph_attr={'fontname':"Avenir"},
        node_attr={"shape":"box", "color":'black', "style":'filled', "fontcolor":'white', "fontsize":"40", 'fontname':"Avenir"},
        edge_attr={"fontsize":"30", 'fontname':"Avenir", "arrowhead":'none', "color":"grey", "penwidth":"10" } )
    node_ids = []
    
    # Iterate through nodes and add to graph
    for node_id, node in json_data["nodes"].items():
        node_ids.append(node_id)
        label = f"{node_id}\n({node['description']})"
        dot.node(node_id, label)
        
    # Iterate through nodes again to create edges
    for node_id, node in json_data["nodes"].items():
        if 'outcomeTrue' in node:
            dot.edge(node_id, node['outcomeTrue']['nextNode'], label="True")
        if 'outcomeFalse' in node:
            dot.edge(node_id, node['outcomeFalse']['nextNode'], label="False")
        if 'outcomeMissing' in node:
            dot.edge(node_id, node['outcomeMissing']['nextNode'], label="Missing")
        if 'outcomeMap' in node:
            for outcome, details in node['outcomeMap'].items():
                dot.edge(node_id, details['nextNode'], label=outcome)
        if 'outcomes' in node:
            for outcome in node['outcomes']:
                if 'outcomeTrue' in outcome:
                    dot.edge(node_id, outcome['outcomeTrue']['nextNode'], label=outcome['description'])
        if 'outcomeDefault' in node:
            dot.edge(node_id, node['outcomeDefault']['nextNode'], label="Default")

    if exit_classes:
        with dot.subgraph() as s:
            s.attr(rank="max")
            for node in bottom_nodes:
                if node in node_ids:  # Only add if node exists
                    s.node(node, shape='rect', fontsize='50', width='20')
    return dot


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='VIP decision_tree visualizer')
    parser.add_argument('-i','--input', help='Path to decision_tree.json', required=True)
    parser.add_argument('-o','--output', help='Path to output_file.png', required=False)
    parser.add_argument('-e','--exit_classes', help='Exit classes comma separated e.g. "exit_vus,exit_lb,exit_p" ', required=False)
    args = vars(parser.parse_args())


    path_input = args["input"]

    if args["output"]:
        path_output = args["output"] 
    else:
        path_output = f"{path_input.split('/')[-1].split('.')[0]}"

    if args["exit_classes"]:
        exit_classes = args["exit_classes"].split(',')
    else:
        exit_classes = None

    # Load JSON data
    with open(path_input) as json_file:
        data = json.load(json_file)

    # Create and render the flowchart
    flowchart = create_flowchart(data, exit_classes)
    flowchart.attr(nodesep="1", ranksep="3",splines="compound", bgcolor='white')
    flowchart.render(path_output, format="png")