'''
Order statistics

find kth smallest 

k=1
k=n
k=n+1/2

randomized divide and conquer

Random-Select(A, p, q, i)

ith smallest in the A[p, q]

if p = q then return A[p]
r <- Rand-Partitioan(A, p, q)
k <- r-p+1 // k = rank(A[r])

if i = k then return A[r]

if i < k then return Random-Select(A, p, r-1, i)

else  return Random-Select(A, r+1, q, i-k)
'''
from PSort import _partition

def randSelect(A, p, q, i):
    r = _partition(A, p, q)
    k = r - p + 1
    if  i == k:
        return A[r]
    if  i < k:
        return randSelect(A, p, r-1, i)
    else:
        return randSelect(A, r+1, q, i-k)


'''
worst case linear time order stats
good pivot force good good pivot

Select(i,n)
1, divide n element in to n/5 group of 5 elems each
   find middle of each group
2, recursively select the  middle of the n/5 group

3, partition with x of pivot let k = rank(x)

4, if i = k return x
   if i < k return  randSelect(.......)
   
   else return  randSeclt(.....)

'''