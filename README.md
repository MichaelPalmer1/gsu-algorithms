# Algorithm Design and Analysis
Code from CSCI 5330

## Graphing Complexities
Growth function visualization

## Maximum Subarray
Within an array A, find a contiguous subarray such that the sum of its elements is greater than that of any other 
contiguous subarray. Output the starting and ending indices and the sum of this subarray.

## Levenshtein Distance
Calculate the Levenshtein Distance

## Master Method
The formula for the master theorem is as follows:

```
T(n) = aT(n/b) + Θ(n^k * log^i (n))
```

The purpose of the master theorem is to calculate the complexity of a divide and conquer expression that is divided 
into `a` sub-problems, with each sub-problem being of size `n/b`. `n` represents the size of the entire problem and 
`f(n)` represents the cost outside of the recursive call, such as the cost of merging the sub-problems back together. 
The end goal is to determine an asymptotically tight bound for the problem.