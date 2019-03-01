
class Tree(object):
    def __init__(self):
        self.root=TreeNode(None)
        self.t=[]
    def add(self,val):
        treenode=TreeNode(val)
        if self.root.val==None:
            self.root=treenode
            self.t.append(self.root)
            return
        else:
            tree_exist_node=self.t[0]
            # print(self.t[0].val)
            if tree_exist_node.left==None:
                tree_exist_node.left=treenode
                self.t.append(tree_exist_node.left)
                return
            else:
                tree_exist_node.right=treenode
                self.t.append(tree_exist_node.right)
                self.t.pop(0)


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def isValidBST(root: TreeNode) -> bool:
    if root is None:
        return True

    # if root.left != None and root.right != None:
    #     if root.left.val > root.val or root.val > root.right.val:
    #         return False
    if root.left != None:
        if root.left.val > root.val :
            return False
    if root.right != None:
        if root.right.val < root.val :
            return False




t1=[1,1]
t= Tree()
for i in t1:
    t.add(i)

print(isValidBST(t.root))
