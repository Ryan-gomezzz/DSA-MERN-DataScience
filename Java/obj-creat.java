// Test class
class obj_creat {
    int age;
    public void assignAge(int num) {
        // Assign the number to age
        age = num;
    }
}

class Basics {
    public static void main(String[] args) {
        // Creating an object having name test1 of Test class
        obj_creat test1 = new obj_creat();
        test1.assignAge(10); // Assigning age 10 to test1 object
        
        // Creating an object having name test2 of Test class
        obj_creat test2 = new obj_creat(); 
        test2.assignAge(19); // Assigning age 19 to test2 object
        
        System.out.println(test1.age);
        System.out.println(test2.age);
    }
}