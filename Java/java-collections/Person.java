// Custom classes in java can be used to define our own data types. In this example, we will create a custom class called "Person" that has two properties: name and age. We will also create a method to display the person's information.
public class Person {
    private String name;
    private int age;

    // Constructor
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // Method to display person's information
    public void displayInfo() {
        System.out.println("Name: " + name + ", Age: " + age);
    }

    // Main method to test the Person class
    public static void main(String[] args) {
        Person person1 = new Person("Alice", 30);
        person1.displayInfo();

        Person person2 = new Person("Bob", 25);
        person2.displayInfo();
    }
}