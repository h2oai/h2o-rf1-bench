# Simple tree python module

class Tree(object):

    def __init__(self,num=None,rootNode=None,signL='<', signR='>='):
        self._num      = num
        self._rootNode = rootNode
        self._signL    = signL
        self._signR    = signR

    def pp(self,prefix=''):
        print("Random Tree")
        print("===========\n")
        self._rootNode.pp(prefix)
        print 
        print("Tree depth:  %s" % self.depth())
        print("Tree leaves: %s" % self.leaves())
        print

    def depth(self):
        return self._rootNode.depth()

    def leaves(self):
        return self._rootNode.leaves()


class TreeNode(object):
    def __init__(self, split_var=None, split_val=None, l=None, r=None):
        self._split_var = split_var
        self._split_val = split_val
        self._l = l
        self._r = r

    def setL(self,l):
        self._l = l

    def setR(self,r):
        self._r = r

    def getL(self):
        return self._l

    def getR(self):
        return self._r

    def pp(self, prefix):
	pass

    def _pp(self, prefix, signL, signR):
        if self._l.is_leaf():
            print("%s%s %s %s : %s" % (prefix,self._split_var, signL, self._split_val, self._l.to_string() ))
        else:
            print("%s%s %s %s" % (prefix,self._split_var, signL, self._split_val))
            self._l.pp(prefix+'|   ')

        if self._r.is_leaf():
            print("%s%s %s %s : %s" % (prefix,self._split_var, signR, self._split_val, self._r.to_string() ))
        else:
            print("%s%s %s %s" % (prefix,self._split_var, signR, self._split_val))
            self._r.pp(prefix+'|   ')

    def is_leaf(self):
        return False

    def leaves(self):
        return self._l.leaves() + self._r.leaves()

    def depth(self):
        return max(self._l.depth(), self._r.depth()) + 1

class SplitTreeNode(TreeNode):
    def __init__(self, split_var=None, split_val=None, l=None, r=None):
        super(SplitTreeNode, self).__init__(split_var, split_val, l, r)
    
    def pp(self, prefix):
	self._pp(prefix, "<=", ">")


class ExclusiveTreeNode(TreeNode):

    def __init__(self, split_var=None, split_val=None, l=None, r=None):
        super(ExclusiveTreeNode, self).__init__(split_var, split_val, l, r)
    
    def pp(self, prefix):
	self._pp(prefix, "==", "!=")


class TreeLeaf(TreeNode):
    def __init__(self, prediction, rows="NA"):
        self._prediction = prediction
        self._l = None
        self._r = None
	self._rows = rows

    def is_leaf(self):
        return True

    def pred(self):
        return self._prediction

    def rows(self):
        return self._rows

    def leaves(self):
        return 1

    def depth(self):
        return 0

    def to_string(self):
	return "%s [rows: %s]" % (self.pred(), self.rows())

