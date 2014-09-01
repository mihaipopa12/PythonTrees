#!/usr/bin/python3

from Dictionary import Dictionary

import unittest
import string
import random


class SplayNode(object):

    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.parent = None
        self.left_son = self.right_son = None

    def rotate_right(self, root=None):

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
        else:
            root = left_son
        left_son.parent = self.parent
        self.parent = left_son

        return root

    def rotate_left(self, root=None):

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
        else:
            root = right_son
        right_son.parent = self.parent
        self.parent = right_son

        return root

    def detach(self):

        parent = self.parent
        if parent is not None:
            if parent.left_son == self:
                parent.left_son = None
            else:
                parent.right_son = None


class SplayTree(Dictionary):

    def __init__(self, root=None):
        self._root = root
        self._size = 0

    def get_root(self):
        return self._root

    def splay(self, node):

        while node.parent is not None:
            parent = node.parent
            grand_parent = parent.parent

            if grand_parent is not None:

                if grand_parent.left_son == parent and parent.left_son == node:
                    self._root = grand_parent.rotate_right(self._root)
                    self._root = parent.rotate_right(self._root)
                elif grand_parent.left_son == parent and parent.right_son == node:
                    self._root = parent.rotate_left(self._root)
                    self._root = grand_parent.rotate_right(self._root)
                elif grand_parent.right_son == parent and parent.right_son == node:
                    self._root = grand_parent.rotate_left(self._root)
                    self._root = parent.rotate_left(self._root)
                else:  # grand_parent.right_son == parent and grand_parent.left_son == node
                    self._root = parent.rotate_right(self._root)
                    self._root = grand_parent.rotate_left(self._root)
            else:

                if parent.left_son == node:
                    self._root = parent.rotate_right(self._root)
                else:  # parent.right_son == node
                    self._root = parent.rotate_left(self._root)

    @staticmethod
    def _insert(node, key, value):
        if node is None:
            new_node = SplayNode(key, value)
            return new_node, new_node, True

        if key == node.key:
            node.value = value
            return node, node, False
        if key < node.key:
            node.left_son, new_node, was_created = SplayTree._insert(node.left_son, key, value)
            node.left_son.parent = node
        else:
            node.right_son, new_node, was_created = SplayTree._insert(node.right_son, key, value)
            node.right_son.parent = node
        return node, new_node, was_created

    def insert(self, key, value=None):
        self._root, new_node, was_created = SplayTree._insert(self._root, key, value)
        if was_created:
            self._size += 1
        self.splay(new_node)

    def erase(self, key):

        node_to_be_erased, node_to_be_splayed = Dictionary._find(self._root, key, None)
        if node_to_be_erased is not None:
            self._size -= 1

            node_to_be_replaced = Dictionary._get_left_most(node_to_be_erased.right_son)
            if node_to_be_replaced is None:
                node_to_be_replaced = node_to_be_erased

            node_to_be_erased.key, node_to_be_erased.value = node_to_be_replaced.key, node_to_be_replaced.value
            if node_to_be_replaced.left_son is not None:
                node_to_be_replaced.key, node_to_be_replaced.value = node_to_be_replaced.left_son.key, node_to_be_replaced.left_son.value
                node_to_be_replaced.left_son.detach()
            elif node_to_be_replaced.right_son is not None:
                node_to_be_replaced.key, node_to_be_replaced.value = node_to_be_replaced.right_son.key, node_to_be_replaced.right_son.value
                node_to_be_replaced.right_son.detach()
            else:
                if node_to_be_replaced.parent is not None:
                    node_to_be_replaced.detach()
                else:
                    self._root = None

        if node_to_be_splayed is not None:
            self.splay(node_to_be_splayed)

    def split(self, key):
        self.insert(key)
        t1, t2 = SplayTree(self._root.left_son), SplayTree(self._root.right_son)
        t1._size, t2._size = len(t1.keys()), len(t2.keys())
        return t1, t2

    def join(self, other_splay_tree):
        if other_splay_tree is None:
            return self

        other_splay_tree.splay(Dictionary._get_left_most(other_splay_tree.get_root()))
        new_root = other_splay_tree.get_root()
        new_root.left_son = self._root

        new_splay_tree = SplayTree(new_root)
        new_splay_tree._size = self.size() + other_splay_tree.size()
        return new_splay_tree

    def __add__(self, other):
        return self.join(other)

    # Queries
    def size(self):
        return self._size

    def choose_element(self):
        return random.choice(self.items())


########################## Testing


class TestSplayOperations(unittest.TestCase):

    def setUp(self):
        self.splay = SplayTree()

        # populate the splay
        self.number_of_insertions = 10000
        for i in range(self.number_of_insertions):
            key = random.randint(1, 1000000)
            value = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(50))
            # self.splay.insert(key, value)
            self.splay[key] = value

    @staticmethod
    def is_sorted(L):
        return all(L[i] <= L[i+1] for i in range(len(L)-1))

    def test_insert(self):

        # the items list must be sorted by keys
        self.assertTrue(TestSplayOperations.is_sorted(self.splay.keys()))

        print ("The height of the splay tree is: " + str(self.splay.get_height()))

    def test_erase(self):

        number_of_deletions = 50
        for i in range(number_of_deletions):
            k = random.choice(self.splay.keys())
            self.splay.erase(k)

        # the items list must be sorted by keys
        self.assertTrue(TestSplayOperations.is_sorted(self.splay.keys()))

    def test_split_and_join(self):

        k, v = self.splay.choose_element()
        t1, t2 = self.splay.split(k)

        # Test the split
        # the items lists must be sorted by keys
        self.assertTrue(TestSplayOperations.is_sorted(t1.keys()))
        self.assertTrue(TestSplayOperations.is_sorted(t2.keys()))

        # the splays elements must all be lower/higher than k
        self.assertTrue(all(current_key <= k for current_key in t1.keys()))
        self.assertTrue(all(current_key > k  for current_key in t2.keys()))

        # Test the join
        t = t1 + t2
        # the items lists must be sorted by keys
        self.assertTrue(TestSplayOperations.is_sorted(t.keys()))

if __name__ == "__main__":
    unittest.main()