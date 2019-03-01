# 构造tree https://blog.csdn.net/memoryjdch/article/details/79161839?utm_source=blogxgwz7

#树节点 节点值 左右节点
class TreeNode(object):
    def __init__(self,x):
        self.val=x
        self.left=None
        self.right=None

# 构造思路：init()方法，初始化一棵树，这棵树包含了root根结点和一个t队列，存储树的节点顺序。
#     先判断树是不是为空（即判断根结点是不是为None），如果是，则把现在传入的这个节点treenode当作树的根。
#     如果树不为空，则先读入目前的根节点self.t[0]，如果目前的根结点的左子树为空，则把现在传入的treenode赋上去。
#     如果树不为空，则先读入目前的根节点self.t[0]，如果目前的根结点的左子树不为空，右子树为空，则把现在传入的treenode赋上去。
#     如果一个节点的左右子树都赋过值了，就将它从t中弹出（用pop操作）。一定要弹出左右子树都满了的节点，这样，下一次读入self.t[0]的时候才能切换成后面的节点。否则一直都只有三个节点，这个树是构建不起来的。即tree_exist_node=self.t[0]和self.t.pop(0)是一对呼应的语句，缺一不可。

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

    #树的最大深度  递归
    def maxdepth(self,root):
        if root is None:
            return 0
        left = self.maxdepth(root.left) + 1
        right = self.maxdepth(root.right) + 1
        return max(left, right)


    # 深度优先
    # 深度优先遍历有三种方式：前序遍历、中序遍历和后序遍历
    # 所说的前序、中序、后序，是指根节点的先后顺序。
    # 前序遍历：根节点 -> 左子树 -> 右子树
    def preorder(self, root):
        if root is None:
            return ''
        rootval = root.val
        print(root.val)
        if root.left:
            self.preorder(root.left)
        if root.right:
            self.preorder(root.right)


    # 中序遍历：左子树 -> 根节点 -> 右子树
    def midorder(self, root):
        if root is None:
            return ''
        if root.left:
            self.midorder(root.left)
        print(root.val)
        if root.right:
            self.midorder(root.right)

    # 后序遍历：左子树 -> 右子树 -> 根节点
    def endorder(self, root):
        if root is None:
            return ''
        if root.left:
            self.endorder(root.left)
        if root.right:
            self.endorder(root.right)
        print(root.val)

#  广度优先
#
# 广度优先遍历，即层次遍历，优先遍历兄弟节点
#
# 层次遍历：根节点 -> 左节点 -> 右节点
    def graorder(self, root):
        if root is None:
            return ''
        queue = [root]
        while queue:
            res = []
            for item in queue:
                print(item.val)
                if item.left:
                    res.append(item.left)
                if item.right:
                    res.append(item.right)
            queue = res

    def issame(self, root1, root2):
        if root1 is None and root2 is None:
            return True
        elif root1 and root2:
            return root1.val == root2.val and self.issame(root1.left, root2.left) and self.issame(root1.right, root2.right)
        else:
            return False




if __name__ == "__main__":
    t1 = [1, 2, 3, 4, 5, 6, 7]
    t = Tree()
    for i in t1:
        t.add(i)

    maxdeep = t.maxdepth(t.root)
    # print(maxdeep)
    # t.preorder(t.root)
    # t.midorder(t.root)
    # t.endorder(t.root)
    t.graorder(t.root)
