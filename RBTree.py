#!/usr/bin/python3

from Dictionary import Dictionary

import unittest
import string
import random

class RBNode(object):

    def __init__(self, colour, key, value = None, parent = None, left_son = None, right_son = None):

        self.colour = colour
        self.key = key
        self.value = value
        self.parent = parent
        self.left_son = left_son
        self.right_son = right_son

    def set_black(self):
        self.colour = True

    def set_red(self):
        self.colour = False

    def grand_parent(self):
        return self.parent.parent if self.parent is not None else None

    def uncle(self):
        grand_parent = self.grand_parent()
        if grand_parent is None:
            return None
        if grand_parent.left_son == self.parent:
            return grand_parent.right_son
        else:
            return grand_parent.left_son

    def rotate_right(self):
        left_son = self.left_son
        self.left_son = left_son.right_son
        if self.left_son is not None:
            self.left_son.parent = self
        left_son.right_son = self
        if self.parent is not None:
            if self.parent.left_son == self:
                self.parent.left_son = left_son
            else:
                self.parent.right_son = left_son
        left_son.parent = self.parent
        self.parent = left_son

    def rotate_left(self):
        right_son = self.right_son
        self.right_son = right_son.left_son
        if self.right_son is not None:
            self.right_son.parent = self
        right_son.left_son = self
        if self.parent is not None:
            if self.parent.left_son == self:
                self.parent.left_son = right_son
            else:
                self.parent.right_son = right_son
        right_son.parent = self.parent
        self.parent = right_son

    @staticmethod
    def is_black(node):
        return node is None or node.colour
    @staticmethod
    def is_red(node):
        return not RBNode.is_black(node)


class RBTree(Dictionary):

    def __init__(self, root = None):
        self._root = root

    def _insert(self, node, parent, key, value):
        if node is None:
            new_node = RBNode(False, key, value, parent, None, None)
            return new_node, new_node

        if key == node.key:
            node.value = value
            return node, None
        if key < node.key:
            new_son, inserted_node = self._insert(node.left_son, node, key, value)
            node.left_son = new_son
        else:
            new_son, inserted_node = self._insert(node.right_son, node, key, value)
            node.right_son = new_son

        return node, inserted_node

    def _checkCase1(self, node):

        if node.parent is None:
            node.set_black()
        else:
            self._checkCase2(node)

    def _checkCase2(self, node):

        if RBNode.is_red(node.parent):
            self._checkCase3(node)

    def _checkCase3(self, node):

        uncle = node.uncle()
        if RBNode.is_red(uncle):
            node.grand_parent().set_red()
            node.parent.set_black()
            node.uncle().set_black()
            self._checkCase1(node.grand_parent())
        else:
            self._checkCase4(node)

    def _checkCase4(self, node):

        grand_parent = node.grand_parent()
        if grand_parent.right_son == node.parent and node == node.parent.left_son:
            node.parent.rotate_right()
            self._checkCase5(node.right_son)
        elif grand_parent.left_son == node.parent and node == node.parent.right_son:
            node.parent.rotate_left()
            self._checkCase5(node.left_son)
        else:
            self._checkCase5(node)

    def _checkCase5(self, node):

        parent = node.parent
        grand_parent = node.grand_parent()
        if grand_parent.left_son == parent and parent.left_son == node:
            parent.set_black()
            grand_parent.set_red()
            grand_parent.rotate_right()
        elif grand_parent.right_son == parent and parent.right_son == node:
            parent.set_black()
            grand_parent.set_red()
            grand_parent.rotate_left()
        else:
            raise AssertionError

    def insert(self, key, value = None):
        self._root, inserted_node = self._insert(self._root, None, key, value)
        if inserted_node is not None:
            self._checkCase1(inserted_node)

    # Specific queries
    def size(self):
        raise NotImplementedError

########################## Testing

class TestRBTreeOperations(unittest.TestCase):

    def setUp(self):
        self.rbtree = RBTree()

        # populate the rbtree
        self.number_of_insertions = 100000
        for i in range(self.number_of_insertions):
            key = random.randint(1, 1000000)
            value = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(50))
            self.rbtree.insert(key, value)

    @staticmethod
    def is_sorted(L):
        return all(L[i] <= L[i+1] for i in range(len(L)-1))

    @staticmethod
    def checkRBTree(node):
        if node is None:
            return True, 0
        check_left_son, height_left_son = TestRBTreeOperations.checkRBTree(node.left_son)
        check_right_son, height_right_son = TestRBTreeOperations.checkRBTree(node.right_son)

        height_left_son += RBNode.is_black(node.left_son)
        height_right_son +=RBNode.is_black(node.right_son)

        return (check_left_son and check_right_son and
                (not RBNode.is_red(node) or not RBNode.is_black(node.parent)) and
                height_left_son == height_right_son), height_left_son

    def test_insert(self):

        # the items list must be sorted by keys
        self.assertTrue(TestRBTreeOperations.is_sorted(self.rbtree.keys()))
        print (self.rbtree.get_height())

        # the treap must have the apropiate structure
        self.assertTrue(TestRBTreeOperations.checkRBTree(self.rbtree._root))

if __name__ == "__main__":
    unittest.main()