#!/usr/bin/python3

from Dictionary import Dictionary

import unittest
import string
import random


class RBNode(object):

    def __init__(self, colour, key, value=None, parent=None, left_son=None, right_son=None):

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

    def sibling(self):
        return None if self.parent is None else (self.parent.left_son if self.parent.left_son != self else self.parent.right_son)

    def rotate_right(self, root = None):

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

    @staticmethod
    def is_black(node):
        return node is None or node.colour
    @staticmethod
    def is_red(node):
        return not RBNode.is_black(node)


class RBTree(Dictionary):

    def __init__(self, root=None):
        self._root = root
        self._size = 0

    def get_root(self):
        return self._root

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
            self._root = node.parent.rotate_right(self._root)
            self._checkCase5(node.right_son)
        elif grand_parent.left_son == node.parent and node == node.parent.right_son:
            self._root = node.parent.rotate_left(self._root)
            self._checkCase5(node.left_son)
        else:
            self._checkCase5(node)

    def _checkCase5(self, node):

        parent = node.parent
        grand_parent = node.grand_parent()
        if grand_parent.left_son == parent and parent.left_son == node:
            parent.set_black()
            grand_parent.set_red()
            self._root = grand_parent.rotate_right(self._root)
        elif grand_parent.right_son == parent and parent.right_son == node:
            parent.set_black()
            grand_parent.set_red()
            self._root = grand_parent.rotate_left(self._root)
        else:
            raise AssertionError

    def insert(self, key, value=None):
        self._root, inserted_node = self._insert(self._root, None, key, value)
        if inserted_node is not None:
            self._size += 1
            self._checkCase1(inserted_node)

    def _erase(self, node):
        if node.left_son is not None and node.right_son is not None:
            raise AssertionError

        existing_son = node.left_son if node.left_son is not None else node.right_son
        if existing_son is not None:
            if RBNode.is_black(existing_son):
                raise AssertionError
            node.key, node.value = existing_son.key, existing_son.value
            node.left_son = node.right_son = None
            existing_son.detach()
        else:

            double_black_node = node
            while double_black_node != self._root and RBNode.is_black(double_black_node):

                parent = double_black_node.parent
                sibling = double_black_node.sibling()

                if double_black_node == double_black_node.parent.left_son:

                    if RBNode.is_red(sibling):

                        self._root = parent.rotate_left(self._root)
                        parent.set_red()
                        sibling.set_black()
                    elif RBNode.is_black(sibling.left_son) and RBNode.is_black(sibling.right_son):

                        sibling.set_red()
                        if RBNode.is_black(parent):
                            double_black_node = parent
                        else:
                            parent.set_black()
                            double_black_node = self._root
                    else:

                        if RBNode.is_black(sibling.right_son):

                            self._root = sibling.rotate_right(self._root)
                            parent.right_son.set_black()
                            parent.right_son.right_son.set_red()
                            parent = double_black_node.parent
                            sibling = double_black_node.sibling()
                        sibling.colour = parent.colour
                        parent.set_black()
                        if sibling.right_son is not None:
                            sibling.right_son.set_black()
                        self._root = parent.rotate_left(self._root)
                        double_black_node = self._root
                else:

                    if RBNode.is_red(sibling):

                        self._root = parent.rotate_right(self._root)
                        parent.set_red()
                        sibling.set_black()
                    elif RBNode.is_black(sibling.right_son) and RBNode.is_black(sibling.left_son):

                        sibling.set_red()
                        if RBNode.is_black(parent):
                            double_black_node = parent
                        else:
                            parent.set_black()
                            double_black_node = self._root
                    else:

                        if RBNode.is_black(sibling.left_son):

                            self._root = sibling.rotate_left(self._root)
                            parent.left_son.set_black()
                            parent.left_son.left_son.set_red()
                            parent = double_black_node.parent
                            sibling = double_black_node.sibling()

                        sibling.colour = parent.colour
                        parent.set_black()
                        if sibling.left_son is not None:
                            sibling.left_son.set_black()
                        self._root = parent.rotate_right(self._root)
                        double_black_node = self._root

            node.detach()

    def erase(self, key):
        node_to_be_erased = Dictionary._find(self._root, key)[0]
        if node_to_be_erased is None:
            return

        self._size -= 1

        replacing_node = Dictionary._get_left_most(node_to_be_erased.right_son)
        if replacing_node is None:
            replacing_node = node_to_be_erased

        node_to_be_erased.key, node_to_be_erased.value = replacing_node.key, replacing_node.value

        if replacing_node != self._root:
            self._erase(replacing_node)
        else:
            # Delete the root
            self._root = None

    # Queries
    def size(self):
        return self._size

########################## Testing

class TestRBTreeOperations(unittest.TestCase):

    def setUp(self):

        self.rbtree = RBTree()

        # populate the rbtree
        self.number_of_insertions = 10000
        for i in range(self.number_of_insertions):
            key = random.randint(1, 1000000)
            value = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(50))
            self.rbtree.insert(key, value)

    @staticmethod
    def is_sorted(L):
        return all(L[i] <= L[i+1] for i in range(len(L)-1))

    @staticmethod
    def check_rbtree(node):
        if node is None:
            return True, 0
        check_left_son, height_left_son = TestRBTreeOperations.check_rbtree(node.left_son)
        check_right_son, height_right_son = TestRBTreeOperations.check_rbtree(node.right_son)

        height_left_son += RBNode.is_black(node.left_son)
        height_right_son += RBNode.is_black(node.right_son)

        return (check_left_son and check_right_son and
                (not RBNode.is_red(node) or not RBNode.is_red(node.parent)) and
                height_left_son == height_right_son), height_left_son

    def test_insert(self):

        # the items list must be sorted by keys
        self.assertTrue(TestRBTreeOperations.is_sorted(self.rbtree.keys()))

        # the treap must have the apropiate structure
        self.assertTrue(TestRBTreeOperations.check_rbtree(self.rbtree._root)[0])

    def test_erase(self):

        number_of_deletions = 50
        for i in range(number_of_deletions):

            random_key = random.choice(self.rbtree.keys())
            self.rbtree.erase(random_key)
            self.assertTrue(TestRBTreeOperations.check_rbtree(self.rbtree._root)[0])


if __name__ == "__main__":
    unittest.main()