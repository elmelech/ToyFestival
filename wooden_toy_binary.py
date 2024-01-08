'''
Attempt 2:
Binary Search version
'''

''''
Logic:
- We want to divide the customer array into three segments that minimized the max range across all of them
- Find the borders of each section by estimating max wait time (t) directly
- We will be using binary search to narrow the window of possible wait times 
    - With a high wait time and a low wait time converging on the ideal wait time

Pseudocode:
- estimate wait time t as midpoint of wait time window
    - Calculate the right hand boarder of ranges of sections 
        - Section 1 (first element + 2t),
        - Section 2 (next element not covered by carver 1 + 2t), 
        - and Section 3 (next element not covered by carver 2 + 2t)
    - if final element of patterns array is within limits of section 3, the wait time estimate is either correct or too long
        - Move high down to midpoint
    - if final element of patterns array is not within limits of section 3, the estimated wait time is not long enough
        - move low up to midpoint+1
    - Recalculate the new midpoint of the window as the estimate t
    - repeat while lo < hi
    - return low
'''

import sys

def toy(n, patterns):
    patterns.sort()

    # 3 or less patterns to make --> 0 wait time
    if len(set(patterns)) <=3:
        return 0

    # Wait time estimate window
    lo = 0
    hi = patterns[-1]

    while lo < hi:
        # Midpoint as estimated wait time
        mid = (hi+lo) // 2

        # Calculate right hand side of ranges based on current wait time estimate (mid)
        # Carver 1 can cover the first element to any element within 2t
        x1 = patterns[0] + 2*mid

        # Carver 2 starts at next element outside of carver 1's range. Not necessarily the next integer 
        i = 0 # track index location of next not covered element
        while (i < (n-1)) and (patterns[i] <= x1):
            i +=1

        # Right hand limit of what carver 2 can cover
        x2 = patterns[i] + 2*mid

        # Find the next element not covered by carver 2's range
        while (i < (n-1)) and (patterns[i] <= x2):
            i +=1

        # Right hand limit of what carver 3 can cover
        x3 = patterns[i] + 2*mid

        print(f"hi: {hi}, lo: {lo}, mid: {mid}")
        print(f"carver 1: {x1} carver 2: {x2} carver 3: {x3}")
        # Test if final element in pattern array is in range
        if patterns[-1] < x3:
            hi = mid
        elif patterns[-1] == x3: # is this true?, is it too small of an edge case to matter? Could just make 1st statement <= and still get correct answer
            return mid
        else:
            lo = mid+1
    
    return lo

def main():
    """
    Main function that takes in input from stdin or from a file and prints the result
    :return: None
    """
    # if  filepath provided
    if len(sys.argv) == 2:
        with open(sys.argv[1], encoding='utf-8') as input_file:
            lines = input_file.readlines()

        lines = [x.strip('\n') for x in lines]

        num_test_cases = int(lines.pop(0))

        for _ in range(num_test_cases):
            n = int(lines.pop(0))
            patterns = [int(x) for x in lines.pop(0).split(" ")]
            print(toy(n, patterns))

    # No filepath provided — get input from stdin
    else:
        num_test_cases = int(input())

        for _ in range(num_test_cases):
            n = int(input())
            patterns = [int(x) for x in input().split(" ")]
            print(toy(n, patterns))

if __name__ == "__main__":
    main()
