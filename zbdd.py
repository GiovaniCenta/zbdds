class ZBDDNode:
    def __init__(self, top, po, p1):
        self.top = top
        self.po = po
        self.p1 = p1

class ZBDD:
    def __init__(self):
        self.uniq_table = {}
        self.base_node = ZBDDNode(0, 1, 0)  # Add base_node to ZBDD class
    
    def getnode(self, top, po, p1):
        if p1 == 0: # node elimination
            return po
        p = (top, po, p1)
        if p in self.uniq_table: # node sharing
            return self.uniq_table[p]
        node = ZBDDNode(p, po, p1)
        self.uniq_table[p] = node
        return node
    
    def subset1(self, p, var):
        if not isinstance(p, ZBDDNode): # check if p is a ZBDDNode object
            return 0
        if p.top < var:
            return 0
        elif p.top == var:
            return p.p1
        elif p.top > var:
            po = self.subset1(p.po, var)
            p1 = self.subset1(p.p1, var)
            return self.getnode(p.top, po, p1)
    
    def subset0(self, p, var):
        if not isinstance(p, ZBDDNode): # check if p is a ZBDDNode object
            return 0
        if p.top < var:
            return p
        elif p.top == var:
            return p.po
        elif p.top > var:
            po = self.subset0(p.po, var)
            p1 = self.subset0(p.p1, var)
            return self.getnode(p.top, po, p1)
    
    def change(self, p, var):
        if p.top < var:
            return self.getnode(var, 0, p)
        elif p.top == var:
            return self.getnode(var, p.p1, p.po)
        elif p.top > var:
            po = self.change(p.po, var)
            p1 = self.change(p.p1, var)
            return self.getnode(p.top, po, p1)
        
    def union(self, p, q):
        if p == 0:
            return q
        elif q == 0:
            return p
        elif p == q:
            return p
        elif p.top > q.top:
            return self.getnode(p.top, self.union(p.po, q), p.p1)
        elif p.top < q.top:
            return self.getnode(q.top, self.union(p, q.po), q.p1)
        else:
            po = self.union(p.po, q.po)
            p1 = self.union(p.p1, q.p1)
            return self.getnode(p.top, po, p1)

    def intsec(self, p, q):
        if p == 0 or q == 0:
            return 0
        elif p == q:
            return p
        elif p.top > q.top:
            return self.intsec(p.po, q)
        elif p.top < q.top:
            return self.intsec(p, q.po)
        else:
            po = self.intsec(p.po, q.po)
            p1 = self.intsec(p.p1, q.p1)
            if po == 0 and p1 == 0:
                return 0
            else:
                return self.getnode(p.top, po, p1)

    def diff(self, p, q):
        if p == 0 or q == 0:
            return 0
        elif p == q:
            return 0
        elif p.top > q.top:
            return self.getnode(p.top, self.diff(p.po, q), p.p1)
        elif p.top < q.top:
            return self.diff(p, q.po)
        else:
            po = self.diff(p.po, q.po)
            p1 = self.diff(p.p1, q.p1)
            if po == 0 and p1 == 0:
                return 0
            else:
                return self.getnode(p.top, po, p1)

    def count(self, p):
        if p == 0:
            return 0
        elif p == self.base_node:
            return 1
        else:
            return self.count(p.po) + self.count(p.p1)
        


# Create a single ZBDD instance
zbdd = ZBDD()

# Create a ZBDD for the set {0, 2}
p = zbdd.getnode(2, zbdd.getnode(0, 1, 0), 0)

# Create a ZBDD for the set {1, 2}
q = zbdd.getnode(2, 0, zbdd.getnode(1, 1, 0))

# Test cases (remaining test cases unchanged)
assert zbdd.count(p) == 2
assert zbdd.count(q) == 2
