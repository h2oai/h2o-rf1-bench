#!/usr/bin/python

import argparse
import stree

def main():
    parser = argparse.ArgumentParser(description="R RandomForest parse" )
    parser.add_argument('--file','-f', help="Parse given file",type=str,required=True)

    args = parser.parse_args()
    
    parseFile(args.file)

def norm(v):
    if v == "<NA>":
        v = None
    return v

def norm_ref(n):
    if n == "0":
        n = None
    return n

def parseFile(fname):
    with open(fname) as f:
        nodes = {}
        treeCnt = 0
        for line in f:
            # skip empty lines
            if line.lstrip() == "":
                continue

            if line.lstrip().startswith('left'):
                if len(nodes) > 0:
                    treeCnt = treeCnt + 1
                    tree = buildTree(treeCnt, nodes)
                    tree.pp()
                    nodes = {}
            else:
                (num,l,r,var,val,status,prediction) = line.split()
                var = norm(var)
                val = norm(val)
                prediction = norm(prediction)
                l = norm_ref(l)
                r = norm_ref(r)

                if status == '-1':
                    node = stree.TreeLeaf(prediction)
                else:
                    node= stree.TreeNode(var,val,l,r)
                nodes[num] = node

def buildTree(num, nodes):
    for idx in nodes:
        node = nodes[idx]
        if node.getL() is not None:
            node.setL( nodes[node.getL()] )

        if node.getR() is not None:
            node.setR( nodes[node.getR()] )

    tree = stree.Tree(num, nodes['1'])

    return tree


if __name__ == '__main__':
    main()



