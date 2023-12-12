class CircularQueue:
    def __init__(self, MAX_QSIZE):
        self. front = 0
        self.rear = 0
        self.MAX_QSIZE = MAX_QSIZE
        self.items = [None] * MAX_QSIZE
    
    def is_empty(self):
        return self.front == self.rear
    
    def is_full(self):
        return self.front == (self.rear + 1) % self.MAX_QSIZE
    
    def clear(self):
        self.front = self.rear
        
    def enqueue(self, item):
        if not self.is_full():
            self.rear = (self.rear + 1) % self.MAX_QSIZE
            self.items[self.rear] = item
            
    def dequeue(self):
        if not self.is_empty():
            self.front = (self.front + 1) % self.MAX_QSIZE
            return self.items[self.front]
        
    def peek(self):
        if not self.is_empty():
            return self.items[self.front % self.MAX_QSIZE]
        
    def size(self):
        return int((self.rear - self.front + len(self.items)) % self.MAX_QSIZE)

    def display(self):
        out = []
        if self.front < self.rear:
            out = self.items[self.front + 1: self.rear + 1]
        else:
            out = self.items[self.front + 1: self.MAX_QSIZE] \
                + self.items[0: self.rear + 1]
        print(f"f={self.front}, r={self.rear} ==> {out}")
