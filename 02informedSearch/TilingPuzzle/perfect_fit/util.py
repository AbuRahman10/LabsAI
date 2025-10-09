from collections import deque

class Stack:
    def __init__(self):
        self._d = []
    def push(self, item):
        self._d.append(item)
    def pop(self):
        return self._d.pop()
    def isEmpty(self):
        return not self._d

class Queue:
    def __init__(self):
        self._d = deque()
    def push(self, item):
        self._d.append(item)
    def pop(self):
        return self._d.popleft()
    def isEmpty(self):
        return not self._d


from collections import deque
import heapq

class Stack:
    def __init__(self):
        self._d = []
    def push(self, item):
        self._d.append(item)
    def pop(self):
        return self._d.pop()
    def isEmpty(self):
        return not self._d

class Queue:
    def __init__(self):
        self._d = deque()
    def push(self, item):
        self._d.append(item)
    def pop(self):
        return self._d.popleft()
    def isEmpty(self):
        return not self._d

class PriorityQueue:
    """
    A min-priority queue where items with lower priority values are popped first.
    Usage:
        pq = PriorityQueue()
        pq.push(item, priority)
        item = pq.pop()
    """
    def __init__(self):
        self._heap = []
        self._count = 0  # tie-breaker to preserve FIFO among equal priorities
    def push(self, item, priority):
        heapq.heappush(self._heap, (priority, self._count, item))
        self._count += 1
    def pop(self):
        if not self._heap:
            raise IndexError("pop from empty PriorityQueue")
        priority, _, item = heapq.heappop(self._heap)
        return item
    def isEmpty(self):
        return not self._heap
