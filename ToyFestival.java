/**
 * ToyFestival.java
 * CodeForces D. - Wooden Toy Festival
 * COMS 4995 - Summer 2023
 * Authors: James Albanese, Steven Chase, Roey Elmelech
 */

import java.util.*;
import java.io.*;

/**
 * Class to solve the Wooden Toy Festival problem
 */
public class ToyFestival {
    
    /**
     * Function to calculate the minimum number of seconds to complete all the toys
     * 
     * @param n The number of toy patterns
     * @param toyPatterns The array of toy patterns
     * @return The minimum number of seconds to complete all the toys
     */

    private static int toy(int n, int[] toyPatterns) {
        Arrays.sort(toyPatterns);

        // Initialize the lower and upper bounds for the binary search
        int lo = 0;
        int hi = toyPatterns[toyPatterns.length-1];

        // Perform binary search
        while (lo < hi) {
            // Calculate the mid point
            int mid = (hi + lo) / 2;

            // Calculate the first range
            int x1 = toyPatterns[0] + 2 * mid;

            // Find the index of the toy pattern that is greater than x1
            int i = 0;
            while ((i < (n-1)) && (toyPatterns[i] <= x1)) {
                i += 1;
            }

            // Calculate the second range
            int x2 = toyPatterns[i] + 2 * mid;

            // Find the index of the toy pattern that is greater than x2
            while ((i < (n-1)) && (toyPatterns[i] <= x2)) {
                i += 1;
            }

            // Calculate the third range
            int x3 = toyPatterns[i] + 2 * mid;

            // If the final element in the toy pattern array is within the range, adjust the upper bound
            if (toyPatterns[toyPatterns.length-1] <= x3) {
                hi = mid;
            }
            // Else, adjust the lower bound
            else {
                lo = mid + 1;
            }
        }
        // Return the minimum number of days to complete all the toys
        return lo;
    }

    /**
     * The main function
     * 
     * @param args The command line arguments
     * @throws IOException If an I/O error occurs
     */
    
    public static void main(String[] args) throws IOException {
        // Initialize a BufferedReader to read the input
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        // Read the number of test cases
        int numTestCases = Integer.parseInt(br.readLine().trim());
        
        for (int i = 0; i < numTestCases; i++) {
            // Read the number of toy patterns
            int n = Integer.parseInt(br.readLine().trim());
            // Read the toy patterns
            String[] toyPatternStr = br.readLine().split(" ");
            int[] toyPatterns = new int[n];
            
            // Convert the toy patterns to integers
            for (int j = 0; j < toyPatternStr.length; j++) {
                toyPatterns[j] = Integer.parseInt(toyPatternStr[j]);
            }
            
            // Print the minimum number of seconds to complete all the toys
            System.out.println(toy(n, toyPatterns));
        }
    }
}