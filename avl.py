# Name: Mackenzie Anderson
# GitHub Username: mkenzieanderson
# Date: February 26, 2024
# Description: Defines the AVLTree and AVLNode classes, which in
#              combination, implement the AVL Binary Search Tree
#              data structure. An AVLNode object contains a value,
#              left and right children, parent, and height data.
#              The AVLTree class has two primary methods to add and
#              remove nodes from the tree. The AVLTree must always
#              stay balanced. Thus, left and right rotation methods
#              are included in the class to rotate nodes after an
#              insertion or removal leaves the tree temporarily un-
#              balanced. There are additional methods in AVLTree to
#              help with the balancing process, and to update the
#              height of affected nodes.


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def _add_helper(self, value: object) -> AVLNode:
        """
        Helper method to the add() method. Specifically does the task of
        traversing the tree and adding the new value as a node to its
        appropriate location. Returns this newly added Node so that add()
        can take care of re-balancing the tree, if needed.

        :param value:   some new value to be added to the tree

        :return:        The newly-added Node. Returns None only if a duplicate
                        value was found, so a node was not added.
        """
        # create AVLNode object with the given value
        new_node = AVLNode(value)

        # # if the tree is empty, insert new value as the root of the tree
        if self._root is None:
            self._root = new_node
            return new_node

        # traverse the tree to find location to add the new node
        current_node = self._root
        while current_node is not None:
            if value == current_node.value:     # don't add duplicate values
                return
            previous_node = current_node
            if value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right

        # add node to the appropriate location, and update child / parent data
        new_node.parent = previous_node
        if value < previous_node.value:
            previous_node.left = new_node
        else:
            previous_node.right = new_node
        return new_node

    def add(self, value: object) -> None:
        """
        Adds the given value to the AVL tree. Duplicate values are not
        allowed and will not be added to the tree. Tree will be re-balanced
        if the newly added node unbalances the Tree.

        :param value:   object to be added to the tree
        """
        # No balancing is needed if there is an attempt to add a duplicate
        # value, or adding the first node in the tree
        new_node = self._add_helper(value)
        if new_node is None or new_node.parent is None:
            return

        # only need to re-balance the tree if the new node is a single child
        if new_node.parent.left is not None and new_node.parent.right is not None:
            return
        parent_node = new_node.parent
        while parent_node is not None:
            self._rebalance(parent_node)
            parent_node = parent_node.parent

    def remove(self, value: object) -> bool:
        """
        Removes the given value from the AVLTree. If the value is not found
        in the tree, then there is no removal, and False is returned. If the
        value is found and removed, then balancing methods are called to
        re-balance the tree, and True is returned.

        :param value:   some value to be removed from the AVLTree

        :return:        True if removal was successful, False otherwise
        """
        # # special case: attempted to remove a value from an empty tree
        if self._root is None:
            return False

        # traverse the AVL tree until the value is found
        current_node = self._root
        while current_node.value != value:
            if value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right
            if current_node is None:    # value not found in tree
                return False

        # initiate the value removal based on its number of subtrees
        if current_node.left is None and current_node.right is None:
            balance_node = current_node.parent
            super()._remove_no_subtrees(current_node.parent, current_node)
        elif current_node.left is not None and current_node.right is not None:
            balance_node = self._remove_two_subtrees(current_node.parent, current_node)
        else:
            balance_node = self._remove_one_subtree(current_node.parent, current_node)

        # balance the tree after the removal
        while balance_node is not None:
            self._rebalance(balance_node)
            balance_node = balance_node.parent
        return True

    def _remove_one_subtree(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        Removes a node from the tree in the specific case where this node to be
        removed only has one subtree. Updates the child of the node's parent to equal
        the first node in remove_node's only subtree

        :param remove_parent:   the parent AVLNode of the node to be removed
        :param remove_node:     The AVLNode to be removed, has only one subtree

        :return:                The node that replaced the spot of the removed node
        """
        # case where the value being removed is the root node
        if remove_node == self._root:
            if remove_node.left is None:
                self._root = remove_node.right
                remove_node.right.parent = None
            else:
                self._root = remove_node.left
                remove_node.left.parent = None
            return self._root

        # Update the remove_parent's appropriate child to be the first node
        # in remove_node's only subtree
        if remove_node.left is None:
            if remove_parent.left == remove_node:
                remove_parent.left = remove_node.right
            else:
                remove_parent.right = remove_node.right
            remove_node.right.parent = remove_node.parent
            return remove_node.right

        if remove_parent.left == remove_node:
            remove_parent.left = remove_node.left
        else:
            remove_parent.right = remove_node.left
        remove_node.left.parent = remove_node.parent
        return remove_node.left


    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        Removes a node in the case that the node has two subtrees. The node
        is replaced with its inorder successor, and the re-balancing process
        begins with the (old) parent node of the inorder successor

        :param remove_parent:   the parent AVLNode of the node to be removed
        :param remove_node:     the AVLNode to be removed

        :return:                returns the original parent node of the inorder
                                successor
        """
        # inorder successor replaces the node to be removed
        successor_node, successor_parent = super()._find_inorder_successor(remove_node)

        # move the inorder successor to the removed node's spot
        successor_node.parent = remove_node.parent
        if self._root == remove_node:
            self._root = successor_node
        elif remove_parent.left == remove_node:
            remove_parent.left = successor_node
        else:
            remove_parent.right = successor_node

        # special case: remove node's right child is in the inorder successor
        if successor_parent == remove_node:
            successor_node.left = remove_node.left
            if remove_node.left is not None:
                remove_node.left.parent = successor_node
            return successor_node

        # update the child relationships of the original parent to the inorder
        # successor, and the child relationships of the inorder successor
        successor_parent.left = None
        if successor_node.right is not None:
            successor_parent.left = successor_node.right
            successor_node.right.parent = successor_parent
        successor_node.right = remove_node.right
        remove_node.right.parent = successor_node
        successor_node.left = remove_node.left
        if remove_node.left is not None:
            remove_node.left.parent = successor_node
        return successor_parent

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Given some AVLNode in the AVL Tree, this method will calculate that
        node's balance factor, and return the result as an integer.

        :param node:    some AVLNode in this AVLTree

        :return:        an integer indicating the balance factor of node
        """
        # determine the height of the node's left and right subtrees
        if node.left is None:
            left_height = -1
        else:
            left_height = node.left.height
        if node.right is None:
            right_height = -1
        else:
            right_height = node.right.height

        # calculate and return the balance factor
        return right_height-left_height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Performs a left rotation on the passed node, which is right-heavy. The
        parameter node is the center of the rotation. Node heights, parents, and
        children data members are updated according to the rotation. Returns the
        node that is now the root of this subtree.

        :param node:    some AVLNode in the tree that is right-heavy

        :return:        the new root of this subtree, after the left rotation
        """
        # the right-heavy node becomes the left child of its right child, and
        # inherits any of that node's left children
        new_root = node.right
        node.right = new_root.left
        if node.right is not None:
            node.right.parent = node
        new_root.left = node

        # update parent and child relationships between the new root node and
        # the parent of the once-right-heavy node
        new_root.parent = node.parent
        if new_root.parent is None:
            self._root = new_root
        else:
            if node.parent.left == node:
                node.parent.left = new_root
            else:
                node.parent.right = new_root
        node.parent = new_root

        # update heights and return the new root of this subtree
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Performs a right rotation on the passed node, which is left-heavy. The
        parameter node is the center of the rotation. Node heights, parents, and
        children data members are updated according to the rotation. Returns the
        node that is now the root of this subtree.

        :param node:    some AVLNode in the tree that is right-heavy

        :return:        the new root of this subtree, after the left rotation
        """
        # the left-heavy node becomes the right child of its left child, and
        # inherits any of that node's right children
        new_root = node.left
        node.left = new_root.right
        if node.left is not None:
            node.left.parent = node
        new_root.right = node

        # update parent and child relationships between the new root node and
        # the parent of the once-right-heavy node
        new_root.parent = node.parent
        if new_root.parent is None:
            self._root = new_root
        else:
            if node.parent.left == node:
                node.parent.left = new_root
            else:
                node.parent.right = new_root
        node.parent = new_root

        # update heights and return the new root of this subtree
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _update_height(self, node: AVLNode) -> None:
        """
        After a node insertion or removal, this method updates the height data
        members of any node whose subtree was impacted by the insertion / removal.
        Requires the parent of the node that was inserted or removed to start the
        chain of node heights. Traverses up the tree to update heights.

        :param node:    some AVLNode in this AVL Tree
        """
        if node.left is None and node.right is None:
            node.height = 0
            return

        if node.left is None:
            node.height = node.right.height + 1
            return

        if node.right is None:
            node.height = node.left.height + 1
            return

        if node.left.height > node.right.height:
            node.height = node.left.height + 1
        else:
            node.height = node.right.height + 1

    def _rebalance(self, node: AVLNode) -> None:
        """
        Checks that the AVLTree is balanced after a node removal or
        insertion. If the tree is unbalanced, then the appropriate
        rotation method(s) will be called to balance the tree.

        :param node:    Some AVLNode in the tree
        """
        balance_factor = self._balance_factor(node)

        # The node is left-heavy and requires a right rotation
        if balance_factor < -1:
            # L-R Case: Double Rotation (left, then right)
            if self._balance_factor(node.left) > 0:
                node_left = self._rotate_left(node.left)
                node_left.parent = node
            self._rotate_right(node)


        # The node is right-heavy and requires a left rotation
        elif balance_factor > 1:
            # R-L Case: Double Rotation (right, then left)
            if self._balance_factor(node.right) < 0:
                node.right = self._rotate_right(node.right)
                node.right.parent = node
            self._rotate_left(node)

        # this subtree is balanced, update the height of this node and continue
        else:
            self._update_height(node)




# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
