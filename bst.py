# Name: Mackenzie Anderson
# GitHub Username: mkenzieanderson
# Date: February 26, 2024
# Description: Defines the BST Class, which implements the Binary
#              Search Tree data structure. A BST is composed of
#              BSTNode objects, and has a _root private data member
#              which identifies the root of the binary tree. The BST
#              class methods include adding and removing nodes from
#              the tree, conducting an inorder traversal of the tree,
#              checking the tree for a specified value, determining the
#              minimum and maximum values in the tree, checking whether
#              the tree is empty, and emptying the tree of its contents


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Creates a BSTNode object corresponding to the passed value, then adds this
        new node to the binary tree. Duplicate values are allowed, and will be
        added to the right subtree of the node of equal value.

        :param value:   some value to be added to the binary tree
        """
        # create new node using passed value as its value
        new_node = BSTNode(value)

        # special case: adding the first node to the binary tree
        if self._root is None:
            self._root = new_node
            return

        # traverse the tree to find the correct space for the new node
        current_node = self._root
        previous_node = current_node
        while current_node is not None:
            previous_node = current_node
            if value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right

        # After finding appropriate location for the new node, update the
        # corresponding child data member of its parent node
        if value < previous_node.value:
            previous_node.left = new_node
            return
        previous_node.right = new_node
        return

    def remove(self, value: object) -> bool:
        """
        Removes specified value from the binary tree. Returns True if the value
        was successfully removed. Returns False otherwise (ie. value does not
        exist in the tree).

        :param value:   Some value to be removed from the binary tree
        """
        # special case: attempted to remove a value from an empty tree
        if self._root is None:
            return False

        # traverse the binary tree until the value is found
        current_node = self._root
        previous_node = current_node
        while current_node.value != value:
            previous_node = current_node
            if value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right
            if current_node is None:    # value not found in tree
                return False

        # initiate the value removal based on its number of subtrees
        if current_node.left is None and current_node.right is None:
            return self._remove_no_subtrees(previous_node, current_node)
        if current_node.left is not None and current_node.right is not None:
            return self._remove_two_subtrees(previous_node, current_node)
        return self._remove_one_subtree(previous_node, current_node)

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes a node from the tree in the specific case where this node to be
        removed does not have a left nor right subtree. Updates the child of the
        node's parent to None.

        :param remove_parent:   the parent BSTNode of the node to be removed
        :param remove_node:     The BSTNode to be removed, has no subtrees
        """
        # case of removing the only remaining node from the tree
        if remove_node == self._root:
            self._root = None
            return True

        # Set the appropriate child of the parent node to None
        if remove_parent.left == remove_node:
            remove_parent.left = None
            return True
        remove_parent.right = None
        return True

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes a node from the tree in the specific case where this node to be
        removed only has one subtree. Updates the child of the node's parent to equal
        the first node in remove_node's only subtree

        :param remove_parent:   the parent BSTNode of the node to be removed
        :param remove_node:     The BSTNode to be removed, has only one subtree
        """
        # case where the value being removed is the root node
        if remove_node == self._root:
            if remove_node.left is None:
                self._root = remove_node.right
            else:
                self._root = remove_node.left
            return True

        # Update the remove_parent's appropriate child to be the first node
        # in remove_node's only subtree
        if remove_node.left is None:
            if remove_parent.left == remove_node:
                remove_parent.left = remove_node.right
            else:
                remove_parent.right = remove_node.right
            return True

        if remove_parent.left == remove_node:
            remove_parent.left = remove_node.left
        else:
            remove_parent.right = remove_node.left
        return True


    def _find_inorder_successor(self, node):
        """
        Given a node in the binary tree, this method returns its inorder
        successor. The passed node must have a right subtree.

        :param node:    Some BSTNode that exists in this binary tree
                        and that has a right subtree

        :return:        A tuple containing the inorder successor node,
                        and the inorder successor's parent node
        """
        previous_node = node
        current_node = node.right
        while current_node.left is not None:
            previous_node = current_node
            current_node = current_node.left
        return (current_node, previous_node)

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes a node from the tree in the specific case where this node to be
        removed has both subtrees. Updates the child of the node's parent to equal
        the first node in remove_node's only subtree

        :param remove_parent:   the parent BSTNode of the node to be removed
        :param remove_node:     The BSTNode to be removed, has only one subtree
        """
        (inorder_successor, inorder_parent) = self._find_inorder_successor(remove_node)

        # remove the node by giving its children to its inorder successor
        inorder_successor.left = remove_node.left
        if inorder_successor != remove_node.right:
            inorder_parent.left = inorder_successor.right
            inorder_successor.right = remove_node.right

        # update the removed node's parent to point to the inorder successor as
        # its appropriate child
        if remove_node == self._root:
            self._root = inorder_successor
            return True
        if remove_parent.left == remove_node:
            remove_parent.left = inorder_successor
        else:
            remove_parent.right = inorder_successor
        return True

    def contains(self, value: object) -> bool:
        """
        Searches the Binary Tree for a given value. Returns True if the value
        is found. Returns False otherwise.

        :param value:   some value to search for in the binary tree

        :return:        True if value is found, False otherwise
        """
        # binary tree is empty: return False
        if self._root is None:
            return False

        # traverse the binary tree in search of the value
        current_node = self._root
        while current_node is not None:
            if current_node.value == value:
                return True
            if value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right

        # traversed tree and did not find the value. Return False
        return False

    def _inorder(self, current_node, inorder_queue):
        """
        Helper function to implement the recursion of inorder_traversal()
        method.

        :param current_node:    some BSTNode that exists in the tree
        :param inorder_queue:   Queue object that is storing the values of
                                the nodes as they are visited
        """
        if current_node is not None:
            self._inorder(current_node.left, inorder_queue)
            inorder_queue.enqueue(current_node.value)
            self._inorder(current_node.right, inorder_queue)

    def inorder_traversal(self) -> Queue:
        """
        Performs an inorder traversal of the binary tree. Creates
        and returns a Queue object that stores the values in the
        order in which they were visited.

        :return:    A Queue object of the binary tree values in their
                    inorder traversal order
        """
        inorder_queue = Queue()
        current_node = self._root
        self._inorder(current_node, inorder_queue)
        return inorder_queue

    def find_min(self) -> object:
        """
        Returns the lowest value in the binary tree. Will return None
        if the binary tree is empty.

        :return:    The lowest value in the binary tree
        """
        # return None if the tree is empty
        if self._root is None:
            return None

        # traverse tree as far left as possible, then return this value
        current_node = self._root
        while current_node.left is not None:
            current_node = current_node.left
        return current_node.value


    def find_max(self) -> object:
        """
        Returns the highest value in the binary tree. Will return None
        if the binary tree is empty.

        :return:    The highest value in the binary tree
        """
        # return None if the tree is empty
        if self._root is None:
            return None

        # traverse tree as far right as possible, then return this value
        current_node = self._root
        while current_node.right is not None:
            current_node = current_node.right
        return current_node.value

    def is_empty(self) -> bool:
        """
        Returns True if the binary tree is empty. Returns false otherwise.

        :return:    True if tree is empty, False otherwise
        """
        return(self._root is None)

    def make_empty(self) -> None:
        """
        Empties the tree of all existing nodes.
        """
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
