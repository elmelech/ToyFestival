'''
Final Project: Wooden Toy Festival
https://codeforces.com/contest/1840/problem/D

Pattern requested by ith person is a_i in pattern array a
3 carvers, can make x pattern in time 0, can make other pattern y in time |x-y|
Carvers can work on requests simultatiously (don't have to account for carver being busy)
Which pattern should each carver specialize in to minimize the max wait over all people

Input:
- # of testcases
- # of people coming
- pattern request array - length n

Output:
- The minimal max wait by any individual
'''

'''
Attempt 1:
- Brute force, try every permutation of carvers 1,2 and 3
- Track the max wait time for each
- Return carver 1, 2 and 3 locations that resulted in the minimum max wait time over all people

Attempt 2:
'''

import sys

## Rutime theta(n^3 * )
# # Not sure what the runtime is 

def toy(patterns):
    # 3 or less patterns to make --> 0 wait time
    if len(set(patterns)) <=3:
        return 0
    
    # sort patterns
    patterns.sort()
    max_wait = 1000000000000

    # Check every combination of x patterns for carvers 1,2,3
    first_pattern = patterns[0]
    last_pattern = patterns[-1]
    for i in range(first_pattern, last_pattern-1):
        for k in range(i+1, last_pattern):
            for j in range(k+1, last_pattern+1):  
                # Wait array, track waiting time for each person
                wait_array = []

                # Update wait array by each carver
                for pattern in patterns:
                    wait_array.append(min([abs(pattern - i), # carver 1
                                           abs(pattern - k), # carver 2
                                           abs(pattern - j)])) # carver 3

                # Check max wait
                cur_max = max(wait_array)
                if cur_max < max_wait:
                    max_wait = cur_max
                
    return max_wait


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
