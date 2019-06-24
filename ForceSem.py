import os
import re
import datetime as dt
import nltk
from googletrans import Translator
import json
import math

'''
ForceSem.py takes a Whatsapp chat history in German and/or English and converts it into a JSON file containing nodes and 
links (or edges), which may be used to create a force-directed graph layout. In the process it parses the text into 
author, time and content. Furthermore, non-natural language elements like ULRs are filtered out. To reduce the text to 
its more meaningful components, a number of words are filtered by type (e.g. articles, connectives) or on the basis of 
comparison of a list of forbidden words, so words, which in themselves carry little to no meaning or are simply very 
general.
'''


class message:
    def __init__(self, line):
        # We try to read a message, but leave it blank if the format is not accepted.
        try:
            # We want to separate the author, content and time of the message.
            self.time = dt.datetime.strptime(line[0:17], '%d/%m/%Y, %H:%M')
            self.author = re.findall(r"[A-Za-zäöüÖÄÜß]+:", line[17:])
            str = re.findall(r'(?<=[a-zA-ZäöüÖÄÜß]: )(.*)', line)

            # URLs include random character sequences, we want to remove them before parsing the message.
            urls = re.findall(r"http\S+", str[0])
            print("url:", urls)
            if urls != None:
                for url in urls:
                    str.remove(url)
                    print(url)
            if str:
                # We store the message. --We could include a translation here, to make further processing easier. Using
                # google tranlate might introduce privacy and security issues, though.
                self.words = re.findall(r'([A-Za-zäöüÖÄÜß]{2,})', str[0].lower())
            else:
                self.words = []
        except:
            self.time = []
            self.author = []
            self.words = []

    def print(self):
        print(self.time, self.author)
        print(self.words)


class whatsApp:
    def __init__(self, txtFile, forbidWord, forbidGer, forbidType):
        # We initialize this object by feeding in the relevant reference files.
        inFile = open(txtFile, 'r')
        self.textL = inFile.read().splitlines()
        inFile.close()
        inFile = open(forbidWord, 'r')
        self.forbidW = inFile.read().splitlines()
        inFile.close()
        inFile = open(forbidGer, 'r')
        self.forbidWger = re.findall(r"[A-Za-zäöüÖÄÜß]+", inFile.read())
        inFile.close()

        inFile = open(forbidType, 'r')
        self.forbidT = inFile.read().splitlines()
        inFile.close()

    def parse(self):
        self.msg = []
        for line in self.textL:
            temp = message(line)
            self.msg.append(temp)

    def label(self):
        # The natural language toolkit determines the type of word in order to filter out specific types later.
        for msg in self.msg:
            msg.words = nltk.pos_tag(msg.words)

    def clean(self):
        # The Message will be filtered to only contain words, which carry meaning independently of context.
        self.label()
        toRemove = []
        print(self.forbidW)
        print(self.forbidWger)
        for msg in self.msg:
            for word in msg.words:
                if word[1] in self.forbidT:
                    toRemove.append(word)
                else:
                    if word[0].lower() in self.forbidW or word[0].lower() in self.forbidWger:
                        toRemove.append(word)
            for rm in toRemove:
                if rm in msg.words:
                    msg.words.remove(rm)


def main():
    # There is a auditory cue for starting and stopping, as the program may run for extended periods of time.
    # As the program repeatedly needs to compare multiple lists, I estimate the time complexity somewhere between being
    # related to the length of conversation to the power of two or three.

    # Specifying some parameters to tweak for the adjustment of the semantic map.

    # Only include words, which occur at least some number of times in the text.
    minCount = 0
    # Only relate word to each other, which occur in a specified timeframe (or lag).
    lag = dt.timedelta(minutes=10)
    # Choose a function to modulate the distribution of the link strength.
    modulate = lambda x: math.sqrt(math.sqrt(x))

    print("Loading Language Processor...")
    #nltk.download('averaged_perceptron_tagger')

    print("Loading chat history and forbidden files...")
    chat = whatsApp('./debsTest.txt', './forbiddenWord.txt', './forbiddenWGer.txt', './forbiddenType.txt')
    print("processing")

    print(chat.textL)
    print(chat.forbidW)
    print(chat.forbidT)

    print("Parsing...\n")
    chat.parse()
    for msg in chat.msg:
        msg.print()
    print("Cleaning...\n")
    chat.clean()
    chat.msg = [item for item in chat.msg if item.words]
    for i, msg in enumerate(chat.msg):
        for j, word in enumerate(msg.words):
            chat.msg[i].words[j] = word[0]
        msg.print()

    # Now the words get counted and marked for removal, in case there are too few occurrences.
    nodes = []
    for msg in chat.msg:
        for word in msg.words:
            found = False
            for node in nodes:
                if node["id"] == word:
                    node['group'] += 1
                    found = True
            if not found:
                nodes.append({"id": word, "group": 1})

    toRemove = []
    for node in nodes:
        if node["group"] < minCount:
            toRemove.append(node)

    '''
    Now the edges are calculated. Each co-occurrence of two words in a message creates an edge with strength 2 or 
    increases the respective edge by two. Each co-occurrence of two words in different messages, which are sent in a 
    certain time frame (lag; std: 10 min) become connected by 1 or their connection increases by 1.
    This section still seems fairly un-pythonic to me. It seems to look a lot like C. Suggestions about how to make this
    a bit more elegant and readable would be appreciated.
    '''
    edges = []
    max = len(chat.msg)
    for i, line in enumerate(chat.msg):
        for word in line.words:
            j = i
            # We want to stay inside the time-frame here.
            while j < max and chat.msg[j].time - line.time <= lag:
                for other in line.words:
                    if word != other:
                        found = False
                        for edge in edges:
                            if (edge["source"] == word and edge["target"] == other) or (
                                    edge["target"] == word and edge["source"] == other):
                                edge["value"] += 1
                                found = True
                                break

                        if not found:
                            # We want to create a new edge, if it does not exist yet. First, we need to make sure the
                            # new node is not primed to be removed.
                            for rm in toRemove:
                                if word == rm["id"] or other == rm["id"]:
                                    found = True
                                    break
                            if not found:
                                edges.append({"source": word, "target": other, "value": 1})
                j += 1
        print("working on", line.time)

    #Now we remove the nodes, we marked earlier.
    for rm in toRemove:
        nodes.remove(rm)

    # Print the edges and apply a function to modulate the distribution of weights in order to achieve the optimal
    # graph.
    for node in nodes:
        print(node)
    for i, edge in enumerate(edges):
        print(edge)
        edges[i]["value"] = modulate(edges[i]["value"])

    # Save the result in JSON and notify the user.
    with open("netOut.json", "w") as out:
        json.dump({"nodes": nodes, "links": edges}, out)

if __name__ == "__main__":
    main()
