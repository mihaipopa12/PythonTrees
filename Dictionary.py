
import abc

class Dictionary(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def insert(self, key, value = None):
        """ Associates a value to a key.
            Complexity: O(log n)
        :param key: The inserted key.
        :param value: The associated value.
        :return: None
        """

    def __setitem__(self, key, value):
        self.insert(key, value)

    @abc.abstractmethod
    def erase(self, key):
        """ Deletes a key from the data structure.
            Complexity: O(log n)
        :param key: The key to be deleted
        :return: None
        """
    # Queries

    @abc.abstractmethod
    def size(self):
        """ Returns the size of the dictionary. """

    @staticmethod
    def _items(node, items_list):

        if node is None:
            return

        Dictionary._items(node.left_son, items_list)
        items_list.append((node.key, node.value))
        Dictionary._items(node.right_son, items_list)

    def items(self):
        """ Returns a list with all the (key, value) pairs sorted by keys.
            Complexity: O(n)
        """

        items_list = []
        Dictionary._items(self._root, items_list)
        return items_list

    def keys(self):
        """ Returns the sorted list of keys.
            Complexity: O(n)
        """
        return [key for key, value in self.items()]

    @staticmethod
    def _get_height(node, current_height):
        if node is None:
            return 0

        return max(current_height,
                   Dictionary._get_height(node.left_son, current_height+1),
                   Dictionary._get_height(node.right_son, current_height+1))

    def get_height(self):
        """ Returns the height of the tree.
            Complexity: O(n)
        """
        return Dictionary._get_height(self._root, 1)

    @staticmethod
    def _look_up(node, key):
        if node is None:
            return None

        if key == node.key:
            return node.value
        if key < node.key:
            return Dictionary._look_up(node.left_son, key)
        else:
            return Dictionary._look_up(node.right_son, key)

    def look_up(self, key):
        return self._look_up(self._root, key)

    def __getitem__(self, key):
        return self.look_up(key)
