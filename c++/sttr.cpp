#include <iostream>
using namespace std;

int main() {
    string firstName = "John";
    string lastName = "Doe";
    
    // Concatenation (Joining strings)
    string fullName = firstName + " " + lastName;
    
    cout << fullName << endl; // Output: John Doe
    
    // Finding length
    cout << fullName.length(); // Output: 8
    
    return 0;
}