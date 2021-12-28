Readme – object oriented graph

The problem:
We have a text file in json that represents a graph with a list of edges and nodes. We need to transform the graph to a code format, visualize it, and edit it in various ways.

The solution/planning:
We will take the data written in the text file and transform it to objects, so we can work with it more conveniently. 

#### EdgeData:
A class that represents a singular edge between 2 nodes.
As an object that represents an edge, it will need to have attributes that represent an edge in a graph.
An edge has a direction, and it comes out of a node, and goes into a node. In addition an edge has length/weight.
EdgeDataClass object will have the attributes of: src – the source of the edge,
dest – the destination of the edge, and w – the weight/length of the edge.

#### NodeData:
A class that represents a singular node in the graph.
As an object that represents a node, it will need to have an attribute to identify the specific node, 
an attribute/s of it’s location.
NodeData object will have the attributes of: id – the id of the node(number),
pos – a tuple of its x and y coordinates.

### DiGraph:
A class that represents a graph. the graph has a dictionary of nodes, using the nodes' ids as keys to the NodeData objects. a list of all edges in the graph and two dictionaries,
one dictionary holds for each node all the edges that go from it to other nodes. the other does the opposite, holds all the edges that go into the node from other nodes.
the important functions in the class are the add\remove node\edge functions.

## GraphAlgo:
A class that lets us run algorithms on a graph.
#### shortest path:
recieves wto id numbers of two nodes and returns the shortest path between them and the total weight of the journey.
we used Dijkstra's Algorithm to write this function. we start with the source node and visit all its neighbours and 
caculate weight of the path, we keep doing that for every unvisited node until we visit all nodes on the graph. Dijkstra's
algorithm gives all shortest paths from the source node to each other node, so we take the one ending at our destination node.

#### center_point
this function returns the node which has the minimal path weight between itself and the node furthest away from it, making it the center of the graph.
to find this node we use a function similar to the shortest path sunction, longest path. it returns the longest path out of the shortest path from this node to any of the others.
center_point runs the longest path function on each node and compares the path it returns, the node with the shortest longest path is the center and
the function returns its id and the weight of its longest shortest path.

#### TSP
this function recieves a list of node ids and return the shortest path that passes through all those points.
to find this path we first of all try to find if there's a path that comes out of the shortest path function that contains all the nodes we 
must pass, which will be the ideal path. we do this by going over all combinations of src node out of those nodes and destination node out of them. 
for each of these combinations we check if the shortest path function returns a path containing all the "must pass" nodes, if it does, that's the best path
and we return it with the total weight of the journey, if it doesn't, for each node we create a path and each time we add its closest neighbour. at the end we take the shortest 
path out of those. if there isn't a path, we return: None and the max vlaue of float.

#### plot_graph
draws the graph on screen using python tkinter. draw all the nodes as circles and the edges as lines with arrows that indicate their source and destination.
each time the user changes the graph this functions is called and redraws the new graph. in this function we also implement a way to give nodes without a position
a random position that makes sense. if there are a couple of nodes without a position we get a random number between 1 and the amount of nodes in the graph, lets say the 
number is n, and thats the amount of nodes we are going to pick to get the x position we take n random nodes that have a position and get the average of their x coordinate.
we do the same with different random numbers for the y coordinate. if all of the nodes dont have a position we give them all a random x and y between 0 and 1 and nultiply
it by the size of the screen. the GUI is very easy to use, the menu contains named buttons for each function you can run on the graph and specifies the right way to enter 
your input.
