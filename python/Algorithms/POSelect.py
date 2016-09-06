'''
Dynamic Order Statistic

OS_select(x) find the xth smallest element in the dynamic array

OS_rank(i) find the rank(i) in the order array

size[x] = size[left[x]] + size[right[x]] + 1

K <- size[left[x]] +1

if i=k then return x

if i<k then return OS-Select(left[x]+i)

   else then return OS-select(right[x] +i- k)


