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
            node = self.hashtable[hashed_key]
            while node.next_node:
                node = node.next_node

            node.next_node = Node(Data(key, value), None)

    
    def get_value(self, key):
        hashed_key = self.hash_custom(key)

        if self.hashtable[hashed_key] is not None:
            node = self.hashtable[hashed_key]
            
            if node.next_node is None:
                return node.data.value

            while node.next_node:
                if key == node.data.key:
                    return node.data.value
                node = node.next_node
        
        if key == node.data.key:
            return node.data.value

        return None

    def print_hash_table(self):
        print("{")

        for i, val in enumerate(self.hashtable):
            if val is not None:
                list_string = ""
                node = val
                if node.next_node:
                    while node.next_node:
                        list_string += (
                            str(node.data.key) + " : " + str(node.data.value) + " -----> "
                        )

                        node = node.next_node
                    list_string += (
                        str(node.data.key) + " : " + str(node.data.value) + " -----> "
                    )

                    print(f"    [{i}] {list_string}")
                else:
                    print(f"    [{i}] {val.data.key} : {val.data.value}")
            else:
                print(f"    [{i}] {val}")

            print("}")