// Base class
class Vehicle {
    private String VehicleNumber;
    
    public Vehicle(String VehicleNumber) {
        this.VehicleNumber = VehicleNumber;
    }
    
    public void honk() {
        System.out.println("Honk !!!!!!!!!!!");
    }
    
    public void printVehicleNumber() {
        System.out.println(VehicleNumber);
    }
}

// Derived class
class Car extends Vehicle{
    public Car(String CarNumber) {
        super(CarNumber);
    }
    
    @Override
    public void honk() {
        System.out.println("Car Honk !!!!!!!");
    }
}

// Derived class
class Bus extends Vehicle{
    public Bus(String BusNumber) {
        super(BusNumber);
    }
}

class Main {
    public static void main(String[] args) {
        Car car = new Car("AB12CD2345");
        car.printVehicleNumber();
        car.honk();
        
        Bus bus = new Bus("XY23MN5678");
        bus.printVehicleNumber();
        bus.honk();
    }
}