# Force Directed Semantic Map
The aim of this project is to transform a whatsapp history, which you can easily download as text on your phone and create a graph which reflects the relationships of different subjects, which occur in the conversation. I chose a force directed graph for this purpose, which may be construed as a network of springs, whith varying tension. Each word is represented by a node and the size of that node depends on the frequency of that word in the conversation. Words which happen to occur in the same context are linked together by an edge (or line). The more often words couccur the thicker the line will be and the closer the nodes will be represented in the graph.
The process has two major stages:

1. ForceSem.py The python script does most of the natural language processing and creates a graph representation of the chat: The text will be parsed and "stop words", which do not carry meaning independently will be filtered out according to the dictionaries in the "forbidden" text files. For now there is support for English and German only. Then this information will be converted into network information using nodes and edges and finally exported in a JSON file.

2. Visualize.py takes the graph representation and produces a 2d embedding by simulating edges with physical string properties as well as a general repelling force between nodes and a central attractive force. This configuration will update iteratively until a equilibrium constellation is found. 

Example: 
![alt text](https://github.com/Herr-Whit/SemMap/blob/master/ForceDirectedSemanticMap.png)
