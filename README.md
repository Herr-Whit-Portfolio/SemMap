# Force Directed Semantic Map
The aim of this project is to transform a whatsapp history, which you can easily download as text on your phone and create a graph which reflects the relationships of different subjects, which occur in the conversation. I chose a force directed graph for this purpose, which may be construed as a network of springs, whith varying tension. Each word is represented by a node and the size of that node depends on the frequency of that word in the conversation. Words which happen to occur in the same context are linked together by an edge (or line). The more often words couccur the thicker the line will be and the closer the nodes will be represented in the graph.
The process has two major stages:

1. ForceSem.py The python script does most of the computational heavy lifting: The text will be parsed and words, which do not carry meaning independently will be filtered out according to the dictionaries in the "forbidden" text files. For now there is support for English and German only. Then this information will be converted into network information using nodes and edges and finally exported in a JSON file.

2. Graph.html This file constructs the visual layout of the graph based on the JSON file. I adaped it slightly from https://github.com/d3/d3-plugins "miserables" - Files belong to the original work and serve as a reference and help with a more intuitive understanding of the graph archetype. The original example is displaying the relationships of different character in the musical drama "Les miserables".

As I have incorporated 3rd party code, I have also copied the licence for now. As I have gone more public with my work as of recently, any advice on handling this more elegantly would be appreciated.
