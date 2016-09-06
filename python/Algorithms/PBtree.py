'''
binary search tree
randomly build search tree
BSTS

balace tree  good
'''

'''
BST sort(A)

T <- NULL
    for i <- 1 to n 
        do insert_tree(T, A[i])
    in_order_tree_walk(root(T))
    
'''

class bnode:
    def __init__(self, data=None, lchild=None, rchild=None):
        self.lchild = lchild
        self.rchild = rchild
        self.data = data
        self.root = False
        
    def addLchild(self, lchild):
        self.lchild = lchild
    
    def delLchild(self):
        self.lchild = None
        
    def addRchild(self, rchild):
        self.rchild = rchild
    
    def delRchild(self):
        self.rchild = None
        
        
class bTree:
    def __init__(self):
        self.node = bnode()
        self.node.root = True
        
    def walk(self):
        _inorderWalk(self.node)
    
    def clear(self):
        self.node = bnode()
        self.node.root = True
    
    def insert(self, data):
        if self.node.data == None:
            self.node.data = data
            self.node.root = True
        else:
            insertnode = bnode(data)
            self._insert(insertnode, self.node)
       
    def _insert(self, insertnode, node):
        if insertnode.data < node.data:
            if node.lchild == None:
                node.addLchild(insertnode)
            else:
                self._insert(insertnode, node.lchild)
        else:
            if node.rchild == None:
                node.addRchild(insertnode)
            else:
                self._insert(insertnode, node.rchild)
                
        
    def hasdata(self, data):
        return self._find(data, self.node)
    
    def _find(self, data, node):
        if(data == node.data):
            return True
        if(data < node.data):
            if(node.lchild == None):
                return False
            else:
                return self._find(data, node.lchild)
        else:
            if(node.rchild == None):
                return False
            else:
                return self._find(data, node.rchild)
                

    def delete(self, data):
        self._delete(data, self.node)
        pass
        
    def _delete(self, data, node):
        if(data == node.data):
            oldnode = node
            if(oldnode.rchild == None and oldnode.lchild == None):
                self.node = bnode()
                return
            elif (oldnode.rchild != None):
                    self.node = node.rchild
                    if(oldnode.lchild != None):
                        self._insert(oldnode.lchild, self.node)
            
            elif (oldnode.lchild != None):
                    self.node = oldnode.lchild
                    if(oldnode.rchild != None):
                        self._insert(oldnode.rchild, self.node)
            return          
        elif(data < node.data):
            if(node.lchild == None):
                print("No data remove.")
                return
            elif(data == node.lchild.data):
                oldnode = node.lchild
                node.lchild = None
                if(oldnode.rchild != None): self._insert(old.rchild, self.node)
                if(oldnode.lchild != None): self._insert(old.lchild, self.node)
                return
            self._delete(data, node.lchild)
        else:
            if(node.rchild == None):
                print("No data remove.")
                return
            elif(data == node.rchild.data):
                oldnode = node.rchild
                node.rchild = None
                if(oldnode.rchild != None): self._insert(old.rchild, self.node)
                if(oldnode.lchild != None): self._insert(old.lchild, self.node)
                return  
            self._delete(data, node.rchild)             
        
def checknodeisroot(func):
    def wrapper(arg):
        #if arg.root == True:
        return func(arg)
        #print("node should be a root node!")
        #return
    return wrapper
        
@checknodeisroot
def _preorderWalk(node):
    if node != None:
        _preorderWalk(node.lchild)
        _preorderWalk(node.rchild)
        print(node.data)

@checknodeisroot
def _inorderWalk(node):
    if node != None:
        _inorderWalk(node.lchild)
        print(node.data)
        _inorderWalk(node.rchild)
        

'''        
AVL tree
2-3 tree
2-3-4 tree
B tree
Red Black tree
skip list
treaps
'''
''' 
Red black tree
BST structure
with extra color field for each node satisfied
1,each node is either red or black
2,the root and leaves are black
3,each red node has black parent
4,all simple path from a node x to a descendant leaves x have same #number of black.
RB_Insert(T, x)
    Tree_Insert(T,x)
    color[x] <- RED
    while x not equal root[T] and color[x] = RED
     do if p[x] = left p[p[x]]                                 // category A
         then y <- right p[p[x]]
             if color[y] = RED
             then <case 1>
             else if x = right[p[x]]
             then <case 2>
             jiezhedo  <case 3>
         
         else same as case A but reverse the left and right    // category B
   color[root[T]] = BLACK
   
All 3 cases:

<case1>
change grandparent RED and change grandparen's children BLACK
X <- grandparent
<case2>
rotate[parentA] left
x <- stay the same position
<case3>
rotate[grandpatent] right  and change color[x] = BLACK and change x's children RED
'''           