class ZBDDNode:
    def __init__(self, top, po, p1):
        self.top = top
        self.po = po
        self.p1 = p1
    def __str__(self):
        return "(top = %s, p0 = %s, p1 = %s)" % (self.top, self.po, self.p1)


class ZBDD:
    def __init__(self):
        self.uniq_table = []
        
        
        self.base_node = ZBDDNode(-1, 0, 0)
        self.uniq_table.append(self.base_node)
        self.uniq_table.append(self.base_node)
        
    def getnode(self, top, po, p1):
        if p1 == 0:  # node elimination
            return po
        
        p = ZBDDNode(top, po, p1)
        #if node in table
        for i, j in enumerate(self.uniq_table):
            if j.top == p.top and j.po == p.po and j.p1 == p.p1:
                return i
        self.uniq_table.append(p)
        return self.uniq_table.index(p)
    def subset1(self, p, var):
        
        p = self.uniq_table[p]
         
        if p.top < var:
            return 0
        
        elif p.top == var:
            return p.p1
        
        elif p.top > var:
            po = self.subset1(p.po, var)
            p1 = self.subset1(p.p1, var)
            return self.getnode(p.top, po, p1)
    
    def subset0(self, p, var):
        p = self.uniq_table[p]
        
        if p.top < var:
            return p
        elif p.top == var:
            return p.po
        elif p.top > var:
            po = self.subset0(p.po, var)
            p1 = self.subset0(p.p1, var)
            return self.getnode(p.top, po, p1)
    
    def change(self, P, var):
        
        p = self.uniq_table[P]
            
        
        if p.top < var:
            return self.getnode(var, 0, P)
        elif p.top == var:
            return self.getnode(var, p.p1, p.po)
        elif p.top > var:
            po = self.change(p.po, var)
            p1 = self.change(p.p1, var)
            return self.getnode(p.top, po, p1)
        
    def union(self, indexP, indexQ):
        p = self.uniq_table[indexP]
        q = self.uniq_table[indexQ]
         
        
        if indexP == 0:
            return indexQ
        elif indexQ == 0:
            return indexP
        elif indexP == indexQ:
            return indexP
        
        elif p.top > q.top:
            return self.getnode(p.top, self.union(p.po, indexQ), p.p1)
        elif p.top < q.top:
            return self.getnode(q.top, self.union(indexP, q.po), q.p1)
        else:
            po = self.union(p.po, q.po)
            p1 = self.union(p.p1, q.p1)
            return self.getnode(p.top, po, p1)

    def intsec(self, indexp, indexq):
        
        p = self.uniq_table[indexp]
        q = self.uniq_table[indexq]
        
        if indexp == 0 or indexq == 0:
            return 0
        elif indexp == indexq:
            return indexp
        elif p.top > q.top:
            return self.intsec(p.po, indexq)
        elif p.top < q.top:
            return self.intsec(indexp, q.po)
        else:
            po = self.intsec(p.po, q.po)
            p1 = self.intsec(p.p1, q.p1)
            if po == 0 and p1 == 0:
                return 0
            else:
                return self.getnode(p.top, po, p1)

    def diff(self, indexP, indexQ):
        p = self.uniq_table[indexP]
        q = self.uniq_table[indexQ]
         
        
       
        if indexP == 0 or indexQ == indexP:
            return 0
        
        elif indexQ == 0 :
            return indexP
        
        
        
        elif p.top > q.top:
            return self.getnode(p.top, self.diff(p.po, indexQ), p.p1)
        elif p.top < q.top:
            return self.diff(indexP, q.po)
        else:
            po = self.diff(p.po, q.po)
            p1 = self.diff(p.p1, q.p1)
            if po == 0 and p1 == 0:
                return 0
            else:
                return self.getnode(p.top, po, p1)

    def count(self, p):
        if not isinstance(p, ZBDDNode):  # Check if p is a ZBDDNode object
            return 0
        if p.top == -1:
            return 1
        if p.po == 0 and p.p1 == 0:
            return 0
        return self.count(p.po) + self.count(p.p1)
    
    def print_zbdd(self, p, level=0):
        if not isinstance(p, ZBDDNode):
            return ' ' * level + str(p)

        return (
            ' |' * level
            + str(p)
            + '\n'
            + self.print_zbdd(p.po, level + 2)
            + '\n'
            + self.print_zbdd(p.p1, level + 2)
        )

zbdd = ZBDD()

"""
p = zbdd.getnode(2, zbdd.getnode(0, 1, 1), 0)

print("p")
print(p)

q = zbdd.getnode(2, 0, zbdd.getnode(1, 1, 1))

print("q")
print(q)

# Test case 1: ZBDD for the set {0, 1}
r = zbdd.getnode(1, zbdd.getnode(0, 1, 1), 0)

print("r")
print(r)

print("change r")
print(zbdd.change(r, 4))

print("união p e q")
print(zbdd.union(p, q))

print("intersecção p e q")
print(zbdd.intsec(p, q))

print("diferença p e q")
print(zbdd.diff(p, q))

print("subset0 p")
print(zbdd.subset0(p, 2))

print("subset0 q")
print(zbdd.subset0(q, 2))

print("count p")
print(zbdd.count(p))
"""

print("change a: ")
a  = zbdd.change(1,0)
print("node: "  + str(a) + " | value: " + str(zbdd.uniq_table[a]))

print("change b: ")
b = zbdd.change(1,1)
print("node: "  + str(b) + " | value: " + str(zbdd.uniq_table[b]))

print("union a,b: ")
unionab = zbdd.union(a,b)
print("node: "  + str(unionab) + " | value: " + str(zbdd.uniq_table[unionab]))

print("union (unionab,1): ")
unionab1 = zbdd.union(unionab,1)
print("node: "  + str(unionab1) + " | value: " + str(zbdd.uniq_table[unionab1]))

print("diff (unionab,a): ")
diffunionabb = zbdd.diff(unionab,a)
print("node: "  + str(diffunionabb) + " | value: " + str(zbdd.uniq_table[diffunionabb]))


print("diff union (unionab,1),a: ")
diffunionaba = zbdd.diff(unionab1,a)
print("node: "  + str(diffunionaba) + " | value: " + str(zbdd.uniq_table[diffunionaba]))










