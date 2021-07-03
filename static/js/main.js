// initialize global variables.
var edges;
var nodes;
var network;
var container;
var options, data;

function parse_data(data) {
    nodes = []
    nn = data["Nodes"]
    for (var i = 0; i < nn.length; i++) {
        var n = { "id": nn[i], "label": nn[i], "shape": "dot", "size": 10 }
        nodes[i] = n
    }

    return [nodes, data["Edges"]]
}

// This method is responsible for drawing the graph, returns the drawn network
function drawGraph(nodes, edges) {
    var container = document.getElementById('mynetwork');

    nodes = new vis.DataSet(nodes)
    edges = new vis.DataSet(edges)

    data = { nodes: nodes, edges: edges };

    var options = {
        "autoResize":true,
        "configure": {
            "enabled": false,
        },
        "edges": {
            "color": {
                "inherit": true
            },
            "smooth": {
                "enabled": false,
                "type": "continuous"
            }
        },
        "interaction": {
            "dragNodes": true,
            "hideEdgesOnDrag": false,
            "hideNodesOnDrag": false,
            "navigationButtons": false,
            "selectable": true,
            "hover":true
        },
        "physics": {
            "enabled": true,
            "stabilization": {
                "enabled": true,
                "fit": true,
                "iterations": 1000,
                "onlyDynamicEdges": false,
                "updateInterval": 50
            }
        }
    };

    network = new vis.Network(container, data, options);
    network.on( 'click', function(properties) {
        var ids = properties.nodes;
        var clickedNodes = nodes.get(ids);
        if(clickedNodes[0]["label"]){
            //console.log(clickedNodes)
            document.getElementById("node_data").innerHTML = clickedNodes[0]["label"]
            //alert(clickedNodes[0]["label"]);
        }

});

    return network;

}
