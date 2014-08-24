#!/usr/bin/python3

import random

import unittest
import string

class _TreapNode(object):

    def __init__(self, key, value, left_son = None, right_son = None, priority = None):

        self.key = key
        self.value = value

        self.priority = priority
        if priority is None:
            self.priority = random.random()

        self.left_son = left_son
        self.right_son = right_son

        self.height_of_subtree = 1
        self.height_of_subtree += left_son.height_of_subtree if left_son is not None else 0
        self.height_of_subtree += right_son.height_of_subtree if right_son is not None else 0

        self.min_key = self.max_key = key
        if left_son is not None:
            self.min_key = min(self.min_key, left_son.min_key)
            self.max_key = max(self.max_key, left_son.max_key)
        if right_son is not None:
            self.min_key = min(self.min_key, right_son.min_key)
            self.max_key = max(self.max_key, right_son.max_key)

    def rotate_right(self):

        his_left_node = self.left_son
        self.left_son = his_left_node.right_son
        his_left_node.right_son = self
        self.update_fields()

        return his_left_node

    def rotate_left(self):

        his_right_node = self.right_son
        self.right_son = his_right_node.left_son
        his_right_node.left_son = self
        self.update_fields()

        return his_right_node

    # Assumes that his sons are already updated
    def update_fields(self):

        self.height_of_subtree = 1
        self.height_of_subtree += self.left_son.height_of_subtree if self.left_son is not None else 0
        self.height_of_subtree += self.right_son.height_of_subtree if self.right_son is not None else 0

        self.min_key = self.max_key = self.key
        if self.left_son is not None:
            self.min_key = min(self.min_key, self.left_son.min_key)
            self.max_key = max(self.max_key, self.left_son.max_key)
        if self.right_son is not None:
            self.min_key = min(self.min_key, self.right_son.min_key)
            self.max_key = max(self.max_key, self.right_son.max_key)


class Treap(object):

    def __init__(self, root = None):
        self._root = None
        if root is not None:
            self._root = root

    @staticmethod
    def _balance(node):

        if (node.left_son is not None and
           (node.right_son is None or node.left_son.priority >= node.right_son.priority) and
           node.left_son.priority >= node.priority):
            return node.rotate_right()

        if (node.right_son is not None and
           (node.left_son is None or node.right_son.priority >= node.left_son.priority) and
           node.right_son.priority >= node.priority):
            return node.rotate_left()

        return node

    # Support insertion
    @staticmethod
    def _insert(node, key, value, _priority):

        if node is None:
            return _TreapNode(key, value, priority = _priority)

        if node.key == key:
            # replace the old value with the new one
            node.value = value
            return node

        if node.key > key:
            node.left_son = Treap._insert(node.left_son, key, value, _priority)
        else:
            node.right_son = Treap._insert(node.right_son, key, value, _priority)

        node = Treap._balance(node)
        node.update_fields()

        return node

    def insert(self, key, value = None, priority = None):

        self._root = Treap._insert(self._root, key, value, priority)

    # Support erasing
    @staticmethod
    def _erase(node, key):

        if node is None:
            return None

        if key < node.key:
            node.left_son = Treap._erase(node.left_son, key)
        elif key > node.key:
            node.right_son = Treap._erase(node.right_son, key)
        else:
            # the current node must be deleted
            if node.left_son is None and node.right_son is None:
                # can be deleted
                del node
                return None
            else:
                if node.left_son is not None and (node.right_son is None or node.left_son.priority >= node.right_son.priority):
                    node = node.rotate_right()
                    node.right_son = Treap._erase(node.right_son, key)
                else:
                    node = node.rotate_left()
                    node.left_son = Treap._erase(node.left_son, key)

        node.update_fields()
        return node

    def erase(self, key):

        self._root = Treap._erase(self._root, key)

    # Support split
    def split(self, key):
        key += 0.5
        self.insert(key, None, 1)

        root_lower, root_higher = self._root.left_son, self._root.right_son
        del self._root

        return Treap(root_lower), Treap(root_higher)

    # Support join
    def join(self, treap_higher):
        if self.get_max_key() > treap_higher.get_min_key():
            raise ValueError("All keys from the treap must be lower than those from the higher treap.")

        middle_key = self.get_max_key() + 0.5

        joining_root = _TreapNode(middle_key, None, self._root, treap_higher._root)
        join_treap = Treap(joining_root)
        join_treap.erase(middle_key)

        return join_treap

    # Queries
    @staticmethod
    def _items(node, items_list):

        if node is None:
            return

        Treap._items(node.left_son, items_list)
        items_list.append((node.key, node.value))
        Treap._items(node.right_son, items_list)

    def items(self):

        items_list = []
        Treap._items(self._root, items_list)
        return items_list

    def keys(self):
        return [key for key, value in self.items()]

    def choose_element(self):
        return random.choice(self.items())

    @staticmethod
    def _get_height(node, current_height):
        if node is None:
            return 0

        return max(current_height,
                   Treap._get_height(node.left_son, current_height+1),
                   Treap._get_height(node.right_son, current_height+1))

    def get_height(self):

        return Treap._get_height(self._root, 1)

    @staticmethod
    def _get_min_key(node):
        if node.left_son is not None:
            return Treap._get_min_key(node.left_son)
        else:
            return node.key

    def get_min_key(self):
        if self._root is None:
            return None
        else:
            return Treap._get_min_key(self._root)

    @staticmethod
    def _get_max_key(node):
        if node.right_son is not None:
            return Treap._get_max_key(node.right_son)
        else:
            return node.key

    def get_max_key(self):
        if self._root is None:
            return None
        else:
            return Treap._get_max_key(self._root)

    @staticmethod
    def _get_kth_element(node, k):
        if node is None:
            return None

        left_son_height = node.left_son.height_of_subtree if node.left_son is not None else 0

        if k == left_son_height:
            return node.key, node.value

        if k < left_son_height:
            return Treap._get_kth_element(node.left_son, k)
        else:
            return Treap._get_kth_element(node.right_son, k - left_son_height - 1)


    def get_kth_element(self, k):
        return Treap._get_kth_element(self._root, k)

########################## Testing

class TestTreapOperations(unittest.TestCase):

    def setUp(self):
        self.treap = Treap()

        # populate the treap
        self.number_of_insertions = 10000
        for i in range(self.number_of_insertions):
            key = random.randint(1, 1000000)
            value = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(50))
            self.treap.insert(key, value)

    @staticmethod
    def is_sorted(L):
        return all(L[i] <= L[i+1] for i in range(len(L)-1))

    @staticmethod
    def check_treap_priorities(node):
        if node is None:
            return True
        return ((node.left_son is None or node.priority >= node.left_son.priority) and
                (node.right_son is None or node.priority >= node.right_son.priority) and
                ((node.left_son is None or TestTreapOperations.check_treap_priorities(node.left_son)) and 
                (node.right_son is None or TestTreapOperations.check_treap_priorities(node.right_son))))

    def test_insert(self):

        # the items list must be sorted by keys
        self.assertTrue(TestTreapOperations.is_sorted(self.treap.keys()))

        # the treap must have the apropiate structure
        self.assertTrue(TestTreapOperations.check_treap_priorities(self.treap._root))

    def test_erase(self):

        print ("Erasing elements...")
        number_of_deletions = 50
        for i in range(number_of_deletions):
            k, v = self.treap.choose_element()
            self.treap.erase(k)

        # the items list must be sorted by keys
        self.assertTrue(TestTreapOperations.is_sorted(self.treap.keys()))

        # the treap must have the apropiate structure
        self.assertTrue(TestTreapOperations.check_treap_priorities(self.treap._root))

    def test_split_and_join(self):

        k, v = self.treap.choose_element()
        t1, t2 = self.treap.split(k)

        # Test the split
        # the items lists must be sorted by keys
        self.assertTrue(TestTreapOperations.is_sorted(t1.keys()))
        self.assertTrue(TestTreapOperations.is_sorted(t2.keys()))

        # the treaps must have the apropiate structure
        self.assertTrue(TestTreapOperations.check_treap_priorities(t1._root))
        self.assertTrue(TestTreapOperations.check_treap_priorities(t2._root))

        # the treaps elements must all be lower/higher than k
        self.assertTrue(all(current_key <= k for current_key in t1.keys()))
        self.assertTrue(all(current_key > k  for current_key in t2.keys()))

        # Test the join
        t = t1.join(t2)
        # the items lists must be sorted by keys
        self.assertTrue(TestTreapOperations.is_sorted(t.keys()))

        # the treaps must have the apropiate structure
        self.assertTrue(TestTreapOperations.check_treap_priorities(t._root))

    def test_queries(self):

        number_of_deletions = 50
        for i in range(number_of_deletions):
            k, v = self.treap.choose_element()
            self.treap.erase(k)

        self.assertTrue(self.treap._root.height_of_subtree == len(self.treap.items()))

        number_of_indexing_queries = 1000
        for i in range(number_of_indexing_queries):
            query_index = random.randint(0, 11000)

            k = None
            try:
                k, v = self.treap.get_kth_element(query_index)
            except TypeError:
                pass

            correct_k = None
            try:
                correct_k = self.treap.keys()[query_index]
            except IndexError:
                pass

            self.assertTrue(k == correct_k)

if __name__ == "__main__":
    unittest.main()