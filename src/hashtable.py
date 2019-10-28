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
    
    # These little helpers keep our hash methods clean
    
    # append an item at the end of our linked pair chain. if the item exists overwrite it
    def append(self, key, value):
        if self.key == key:
            self.value = value
        elif not self.next:
            self.next = LinkedPair(key, value)
        else:
            self.next.append(key, value)
    
    # retrieve an item from our linked list chain
    def retrieve(self, key):
        if self.key == key:
            return self.value
        elif not self.next:
            print(f"Hash[{key}] is undefined")
            return None
        else:
            return self.next.retrieve(key)
        
class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''
    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity
    
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
        if not None in self.storage:
            self.resize()
        hash_mod = self._hash_mod(key)
        # if we have something at the hash_mod index, append this value. Using LinkedPair.append will overwrite a value if that value already exists, and traverse over all the values
        if self.storage[hash_mod]:
            self.storage[hash_mod].append(key, value)
        else:
            self.storage[hash_mod] = LinkedPair(key, value)
        
    def remove(self, key):
        '''
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Fill this in.
        '''
        hash_mod = self._hash_mod(key)
        # if there is nothing at our index, print our little error message and get out of there!
        if not self.storage[hash_mod]:
            print(f'Hash[{key}] cannot be deleted: it does not exist')
            return
        # otherwise take a look at the first node at that index
        current_node = self.storage[hash_mod]
        prev_node = None
        # if there is only one node at this index and it has the key we want we just need to delete it, make the value at this index None
        if current_node.key == key and not current_node.next:
            self.storage[hash_mod] = None
        # else if this is the node we want and it's the first node, set the value at this index to point to the next node in the list
        elif current_node.key == key:
            self.storage[hash_mod] = self.storage[hash_mod].next
        # otherwise traverse the list and delete the node if we find it
        else:
            while current_node:
                if current_node.key == key:
                    prev_node.next = current_node.next
                    return
                prev_node = current_node
                current_node = current_node.next
        

    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        '''
        hash_mod = self._hash_mod(key)
        if self.storage[hash_mod]:
            return self.storage[hash_mod].retrieve(key)
        else:
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
    # print(ht)
    # return_value = ht.retrieve("key-0")
    # print(return_value, "val-0")
    # return_value = ht.retrieve("key-1")
    # print(return_value, "val-1")
    # return_value = ht.retrieve("key-2")
    # print(return_value, "val-2")
    # return_value = ht.retrieve("key-3")
    # print(return_value, "val-3")
    # return_value = ht.retrieve("key-4")
    # print(return_value, "val-4")
    # return_value = ht.retrieve("key-5")
    # print(return_value, "val-5")
    # return_value = ht.retrieve("key-6")
    # print(return_value, "val-6")
    # return_value = ht.retrieve("key-7")
    # print(return_value, "val-7")
    # return_value = ht.retrieve("key-8")
    # print(return_value, "val-8")
    # return_value = ht.retrieve("key-9")
    # print(return_value, "val-9")

    # ht.remove("key-4")
    # ht.remove("key-3")
    # ht.remove("key-2")
    # ht.remove("key-1")
    # ht.remove("key-9")
    # ht.remove("key-8")
    # ht.remove("key-7")
    # ht.remove("key-6")
    # ht.remove("key-5")
    
    ht.remove("key-0")
    print(ht)
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