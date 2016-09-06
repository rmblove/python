#!usr/bin/python3
# This is Sort Problem Solving.
'''
Insertion Sort

for j <- 2 to n
    do key <- A[j]
        i <- j-1
        while i > 0 and A[i] > key
            do A[i+1] <- A[i]
               i <- i-1
        A[i+1] <- key

'''

def insertionSort(list):
    '''
    Running time:Ø(n**2)
    '''
    for j in range(1, len(list)):
        key = list[j]
        i = j-1
        while(i >= 0 and list[i] > key):
            list[i+1] = list[i]
            i = i-1
        list[i+1] = key

'''
Merge Sort

1, if n == 1 done   RT:Ø(1)

2, recursively sort
    
    A[1...[n/2]] sort
    B[[[n/2]+1]...n] sort
    
3, merge sorted list
    
key subroutine : MERGE

'''

def _merge(list1, list2):
    list = []
    n1_lenth = len(list1)
    n2_lenth = len(list2)
    n1 = 0
    n2 = 0
    while(n1 < n1_lenth and n2 < n2_lenth):
        if list1[n1] > list2[n2]:
            list.append(list2[n2])
            n2 += 1
        else:
            list.append(list1[n1])
            n1 += 1
    while(n1 < n1_lenth):
        list.append(list1[n1])
        n1 += 1
    while(n2 < n2_lenth):
        list.append(list2[n2])
        n2 += 1
    return list

def mergeSort(list):
    n = len(list)
    import sys
    sys.setrecursionlimit = n
    if (n == 1):
        return list
    else:
        return _merge(mergeSort(list[:int(n/2)]), mergeSort(list[int(n/2):]))



'''
    Binary search
1, Divide : compare in the middle.

2, Conquer : in the the subarray.

3. Combine ; nothing
'''



'''
    Powering a number
'''

def powerNum(x:int, n: int):
    '''
        running time : Ø(lg(n))
    '''
    if(n==1):
        return x
    if(n%2 == 0):
        return powerNum(x, n/2)*powerNum(x, n/2)
    if(n%2 == 1):
        return powerNum(x, (n-1)/2)*powerNum(x, (n-1)/2)*x

'''
    fibnacci 
    bottom- up algorithm
    computer F1 F2 F3 F4 F5
    time: Ø(n)
    naive recursive algorithm f(n) = f(n-1) + f(n-2)
    time: x**n/sqrt(5)
    
'''

def fibnacciNum(x:int, n:int):
    '''
        recursive squaring
        Thm:   [Fn+1, Fn     =   ([1, 1
                  Fn, Fn-1]        1, 0])**n
    '''
    pass

'''
    matrix multipulication
    
    INPUT : A = a[i][j] B = b[i][j]  i,j = 1,2,3...n
    OUTPUT : C = c[i][j] = A.B

    Divide : 
'''

'''
    QuickSort - Tony Hoere 1962
    Sorting in place.
    
    //import sys
    //sys.setrecursionlimit = n
    
    very pratical
    Divide : partition the array into two subarray around pivot x $element in lower subarray ≤ x ≤ in upper subarray.
    conquer : recursively sort the two subarray
    Combine : trivial
    Time : linear time Ø(n) partitioning subarray
    
        Partitionly(A, p, q)// A[p....q]
        x (<- A[p] //pivoit A[p]
        i <- p
        for j <- p+1 to q
            do if A[j] ≤ x
                  then i = i+1
                  exch a[i] <-> a[j]
        exch a[p] <-> a[i]
        return i
    Time : Ø(nlogn) average case
        QuickSort(A, p ,q)
        if p < q:
           then r <- Partition(A, p, q)
                QuickSort(A, p, r-1)
                QuickSort(A, r+1, q)
        Initial QuickSort(A, 0, len(A))
'''
def _partition(list, p, q):
    piviot = list[p]
    i = p
    for j in range(p+1, q+1):
        if list[j] <= piviot:
            i += 1
            list[i], list[j] = list[j], list[i]
    list[i], list[p] = list[p], list[i]
    return i


def quickSort(list, p, q):
    if p < q:
        r = _partition(list, p, q)
        quickSort(list,p, r-1)
        quickSort(list,r+1, q)

'''
    Decision tree 
    sort <a1, a2, a3>
'''











