from collections import deque

dq = deque([2,3,1,4,5])

dq.append(6)  # Add to the right
print(dq)  # deque([2, 3, 1, 4, 5, 6])

dq.appendleft(0)  # Add to the left
print(dq)  # deque([0, 2, 3, 1, 4, 5, 6])

print(dq.pop())  # Remove from the right
print(dq)  # deque([0, 2, 3, 1, 4, 5])

print(dq.popleft())
print(dq)  # deque([2, 3, 1, 4, 5])

dq.extend([7, 8, 9])  # Extend to the right It can be any kind of data type 
print(dq)  # deque([2, 3, 1, 4, 5, 7, 8, 9])

dq.rotate(2)
print(dq)  # deque([8, 9, 2, 3, 1, 4, 5, 7])


# USed for stack and queue problems and BFS, sliding window oproblems and fast add and rmeove on both ends 



