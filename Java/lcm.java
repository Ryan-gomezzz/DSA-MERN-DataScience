class Solution {
    // Function to find the GCD of two numbers
    private int GCD(int n1, int n2) {
        
        /* Continue loop as long as both 
         n1 and n2 are greater than zero */
        while (n1 > 0 && n2 > 0) {
            
            /* If n1 is greater than n2, perform
             modulo operation - n1 % n2 */
            if (n1 > n2) {
                n1 = n1 % n2;
            }
            
            /* Else perform modulo
            operation - n2 % n1 */
            else {
                n2 = n2 % n1;
            }
        }
        
        // If n1 is zero, GCD is stored in n2
        if (n1 == 0) return n2;
        
        // else GCD is stored in n1
        return n1;
    }
    
    // Function to find LCM of n1 and n2
    public int LCM(int n1, int n2) {
        // Function call to find gcd
        int gcd = GCD(n1, n2);
        
        int lcm = (n1 * n2) / gcd;
        
        // Return the LCM
        return lcm;
    }

    public static void main(String[] args) {
        int n1 = 3, n2 = 5;
        
        /* Creating an instance of 
        Solution class */
        Solution sol = new Solution();
        
        // Function call to get LCM of n1 and n2
        int ans = sol.LCM(n1, n2);
        System.out.println("The LCM of " + n1 + " and " + n2 + " is: " + ans);
    }
}
