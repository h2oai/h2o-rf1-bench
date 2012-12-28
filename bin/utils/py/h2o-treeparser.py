#!/usr/bin/python

import argparse
import stree

def main():
    parser = argparse.ArgumentParser(description="R RandomForest parse" )
    parser.add_argument('--file','-f', help="Parse given file",type=str,required=True)

    args = parser.parse_args()
    
    parseFile(args.file)

def parseFile(fname):
    with open(fname) as f:
        for line in f:
            if line.lstrip() == "":
                continue

            if line.lstrip().startswith('Tree :'):
                tree = parseTreeLine(line.replace('Tree :', ''))
                tree.pp('')

def parseTreeLine(line):
    (num, depth, leaves, treeStr) = line.strip().split(None,3)
    tree = stree.Tree(num, parseTree(treeStr),'<=','>')

    return tree

def parseTree(treeStr):

    node = None
    
    if treeStr.startswith('['):
        node = stree.TreeLeaf(treeStr.lstrip('[').rstrip(']'))
    else:
        (splitExp, kids) = treeStr.split(None,1)
        
        if "<=" in splitExp:
            (splitVar,splitVal) = splitExp.split("<=")
            node = stree.TreeNode(split_var=splitVar, split_val=splitVal)
        else:
            (splitVar,splitVal) = splitExp.split("==")
            node = stree.ExclusiveTreeNode(split_var=splitVar, split_val=splitVal)

        (l,r) = splitKids(kids.lstrip('(').rstrip(')'))
        node.setL( parseTree(l) )
        node.setR( parseTree(r) )

    return node

def splitKids(kidsStr):
    opened = 0 # opened braces
    for i,c in enumerate(kidsStr):
        if c == '(':
            opened = opened + 1
        elif c == ')':
            opened = opened - 1
        elif c == ',' and opened == 0:
            return (kidsStr[:i], kidsStr[i+1:])

if __name__ == '__main__':
    main()


