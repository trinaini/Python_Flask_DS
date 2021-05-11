class Node:

    def __init__(self, data = None, next_node = None):
        self.data = data
        self.next_node = next_node

class Data:

    def __init__(self, key, value):
        self.key = key
        self.value = value
    

class HashTable:
    def __init__(self, table_size):
        self.table_size = table_size
        self.hashtable = [None] * table_size

    def hash_custom(self, key):
        hashvalue = 0

        for i in key:
            hashvalue += ord(i)
            hashvalue = (hashvalue * ord(i)) % self.table_size
        
        return hashvalue

    def add_key_value(self, key, value):
        hashed_key = self.hash_custom(key)

        if self.hashtable[hashed_key] is None:
            self.hashtable[hashed_key] = Node(Data(key, value), None)

        else:
            pass