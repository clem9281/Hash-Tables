# '''
# Linked List hash table key/value pair
# '''
class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        
    def __str__(self):
        return f"{{{self.key}, {self.value}}}"
    
    def __repr__(self):
        next = None
        if self.next:
            next = self.next.key
        return f"{{key: {self.key}, value: {self.value}, next_key: {next}}}"
        
class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''
    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity
        # self.count = 0
    
    def __str__(self):
        # This helped me to see the structure we are making, it prints our hash table as an dictionary with each index as it's key, and as the value either None or the 'linked list' as an array
        holder = {}
        def append_to_holder(element, holder, index):
            holder[index].append(element)
        for i in range(len(self.storage)):
            holder[i] = []
            if self.storage[i]:
                current_node = self.storage[i]
                while current_node:
                    holder[i].append(current_node) 
                    current_node = current_node.next
            else:
                holder[i] = None
        return f"{holder}"

    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key)


    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        '''
        hash_value = 5381
        # Bit-shift and sum value for each character
        for char in key:
            hash_value = ((hash_value << 5) + hash_value) + ord(char)
        return hash_value


    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self._hash(key) % self.capacity
        # return self._hash_djb2(key) % self.capacity


    def insert(self, key, value):
        '''
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Fill this in.
        '''
        # if there are no "None"s in our array we have reached capacity
        # double the hash capacity
        if not None in self.storage:
            print(f'FILLED UP HERE: {self}')
            self.resize()
        hash_mod = self._hash_mod(key)
        # if we have something at the hash_mod index
        if self.storage[hash_mod]:
            # iterate over the linked pairs
            current_node = self.storage[hash_mod]
            while current_node:
                # if any of these nodes already has the provided key, overwrite the value there, and break
                if current_node.key == key:
                    current_node.value = value
                    break
                # if the current node does not have a next it is the last one, add the new key value and break
                if not current_node.next:
                    current_node.next = LinkedPair(key, value)
                    break
                
                current_node = current_node.next
        else:
            self.storage[hash_mod] = LinkedPair(key, value)
        



    def remove(self, key):
        '''
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Fill this in.
        '''
        hash_mod = self._hash_mod(key)
        if self.storage[hash_mod]:
            current_node = self.storage[hash_mod]
            prev_node = current_node
            # if there is only one node at this index we just need to delete it
            if not current_node.next:
                self.storage[hash_mod] = None
            # otherwise traverse the list, when we find the node with the key we want we will set the next of the node before it to the current node's next, whether that is another node or None is fine
            else:
                while current_node:
                    if current_node.key == key:
                        prev_node.next = current_node.next
                    prev_node = current_node
                    current_node = current_node.next
        else:
            print(f'Hash[{key}] cannot be deleted: it does not exist')

    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        '''
        hash_mod = self._hash_mod(key)
        if self.storage[hash_mod]:
            current_node = self.storage[hash_mod]
            while current_node:
                if current_node.key == key:
                    return current_node.value
                current_node = current_node.next
        print(f"Hash[{key}] is undefined")
        return None

    def resize(self):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Fill this in.
        '''
        self.capacity *= 2
        old_storage = self.storage
        self.storage = [None] * self.capacity
        for node in old_storage:
            # we should be able to assume at this point that the node should not be None, as we should only call resize when the storage is full, but it looks like in the tests they call resize a couple different times so just in case we'll check to make sure the node we are looking at is not None before attempting to traverse it
            if node:
                current_node = node
                while current_node:
                    self.insert(current_node.key, current_node.value)
                    current_node = current_node.next


if __name__ == "__main__":
    # ht = HashTable(2)

    # ht.insert("line_1", "Tiny hash table")
    # # print(1, ht)
    # ht.insert("line_2", "Filled beyond capacity")
    # # print(2, ht)
    # ht.insert("line_3", "Linked list saves the day!")
    # # print(3, ht)
    # ht.insert("line_3", "Second line 3")
    # print(4, ht)
    # print("")

    # # # Test storing beyond capacity
    # print(ht.retrieve("line_1"))
    # print(ht.retrieve("line_2"))
    # print(ht.retrieve("line_3"))

    # # Test resizing
    # old_capacity = len(ht.storage)
    # ht.resize()
    # print(4, ht)
    # new_capacity = len(ht.storage)

    # print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # # Test if data intact after resizing
    # print(ht.retrieve("line_1"))
    # print(ht.retrieve("line_2"))
    # print(ht.retrieve("line_3"))

    # print("")
    ht = HashTable(8)

    ht.insert("key-0", "val-0")
    ht.insert("key-1", "val-1")
    ht.insert("key-2", "val-2")
    ht.insert("key-3", "val-3")
    ht.insert("key-4", "val-4")
    ht.insert("key-5", "val-5")
    ht.insert("key-6", "val-6")
    ht.insert("key-7", "val-7")
    ht.insert("key-8", "val-8")
    ht.insert("key-9", "val-9")

    # return_value = ht.retrieve("key-0")
    # print(return_value , "val-0")
    # return_value = ht.retrieve("key-1")
    # print(return_value , "val-1")
    # return_value = ht.retrieve("key-2")
    # print(return_value , "val-2")
    # return_value = ht.retrieve("key-3")
    # print(return_value , "val-3")
    # return_value = ht.retrieve("key-4")
    # print(return_value , "val-4")
    # return_value = ht.retrieve("key-5")
    # print(return_value , "val-5")
    # return_value = ht.retrieve("key-6")
    # print(return_value , "val-6")
    # return_value = ht.retrieve("key-7")
    # print(return_value , "val-7")
    # return_value = ht.retrieve("key-8")
    # print(return_value , "val-8")
    # return_value = ht.retrieve("key-9")
    # print(return_value , "val-9")

    ht.remove("key-9")
    ht.remove("key-8")
    ht.remove("key-7")
    ht.remove("key-6")
    ht.remove("key-5")
    ht.remove("key-4")
    ht.remove("key-3")
    ht.remove("key-2")
    ht.remove("key-1")
    ht.remove("key-0")

    return_value = ht.retrieve("key-0")
    print(return_value)
    # return_value = ht.retrieve("key-1")
    # print(return_value)
    # return_value = ht.retrieve("key-2")
    # print(return_value)
    # return_value = ht.retrieve("key-3")
    # print(return_value)
    # return_value = ht.retrieve("key-4")
    # print(return_value)
    # return_value = ht.retrieve("key-5")
    # print(return_value)
    # return_value = ht.retrieve("key-6")
    # print(return_value)
    # return_value = ht.retrieve("key-7")
    # print(return_value)
    # return_value = ht.retrieve("key-8")
    # print(return_value)
    # return_value = ht.retrieve("key-9")
    # print(return_value)