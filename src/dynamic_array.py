class Dynamic_Array:
    def __init__(self, capacity=8):
        self.count = 0
        self.capacity = capacity
        self.storage = [None] * capacity
    
    def insert(self, index, value):
        if self.count >= self.capacity:
            self.double_size()
        for i in range(self.count, index, -1):
            self.storage[i] = self.storage[i - 1]
        self.storage[index] = value    
        self.count += 1
        
    def append(self, value):
        if self.count >= self.capacity:
            self.double_size()
        self.storage[self.count] = value
        self.count += 1
    
    def double_size(self):
        self.capacity *= 2
        new_storage = [None] * self.capacity
        for i in range(self.count):
            new_storage[i] = self.storage[i]
        self.storage = new_storage
        
arr = Dynamic_Array()
arr.append('a')
arr.append('a')
arr.append('a')
arr.append('a')
arr.append('a')
arr.append('a')
arr.append('a')
arr.append('a')
arr.insert(4, 'b')
print(arr.storage)