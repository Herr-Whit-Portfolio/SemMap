import numpy as np
import svgwrite as svgw
import json
from svgwrite import shapes as sh
import math

def draw(n):
    with open('netOut.json', 'r') as f:
        graph = json.load(f)

    to_remove = [i for i in range(len(graph['nodes']))]
    for edge in graph['edges']:
        if edge['source'] in to_remove:
            to_remove.remove(edge['source'])
        elif edge['target'] in to_remove:
            to_remove.remove(edge['target'])
    for i in to_remove:
        graph['edges'].pop(i)



    num_iter = 200

    num_nodes = len(graph['nodes'])

    pos = np.random.normal(0, 1, (num_nodes, 2))
    velocity = np.zeros((num_nodes, 2))
    # acc = np.zeros((num_nodes, 2))

    for it in range(num_iter):
        # Concentric force
        acc = -pos * 4

        for i in range(num_nodes):
            # Repelling Force
            acc[i] += 20 * np.mean(1 / 5 * (pos[i] - pos), axis=0)
        for edge in graph['edges']:
            # Spring Force
            spring = 0.1 * (pos[edge['source']] - pos[edge['target']])
            acc[edge['source']] -= spring
            acc[edge['target']] += spring
        velocity *= 0.8
        velocity += acc * 0.1
        pos += velocity * 0.2
    print(pos[i])
    # print(pos / np.argmax(np.abs(pos)))
    pos = pos / np.argmax(np.abs(pos))
    factor = 1000000
    pos = np.tanh(pos * 100) * factor
    sd = np.std(pos) * 0.8
    chatmap = svgw.Drawing('chatmap' + str(n) + '.svg')
    for node in graph['nodes']:
        if min(abs(pos[node['id']]) < sd):
            chatmap.add(sh.Circle(pos[node['id']], np.sqrt(node['count']) * 0.0005 * factor, fill='orange'))
    for edge in graph['edges']:
        if min(abs(pos[edge['source']]) < sd) and min(abs(pos[edge['target']]) < sd):
            chatmap.add(sh.Line(pos[edge['source']], pos[edge['target']], fill='orange', style="stroke:orange;stroke-width:" + str(0.11 * edge['value']) + ';opacity:' + str(1 - 1/ edge['value'])))
    chatmap.save()

    print('CM' + str(n) + 'saved')


def main():
    for i in range(10):
        draw(i)
    exit(0)
if __name__ == '__main__':
    main()