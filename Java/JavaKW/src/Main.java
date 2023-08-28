import java.io.*;
import java.util.*;

class Toy {
    private int id;
    private String name;
    private int quantity;
    private double frequency;

    public Toy(int id, String name, int quantity, double frequency) {
        this.id = id;
        this.name = name;
        this.quantity = quantity;
        this.frequency = frequency;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public int getQuantity() {
        return quantity;
    }

    public double getFrequency() {
        return frequency;
    }

    public void setFrequency(double frequency) {
        this.frequency = frequency;
    }

    public void decreaseQuantity() {
        quantity--;
    }
}

class ToyStore {
    private List<Toy> toys = new ArrayList<>();
    private List<Toy> prizeToys = new ArrayList<>();

    public void addToy(int id, String name, int quantity, double frequency) {
        toys.add(new Toy(id, name, quantity, frequency));
    }

    public void updateToyFrequency(int toyId, double newFrequency) {
        for (Toy toy : toys) {
            if (toy.getId() == toyId) {
                toy.setFrequency(newFrequency);
                break;
            }
        }
    }

    public void startRaffle() {
        Random random = new Random();
        double totalFrequency = toys.stream().mapToDouble(Toy::getFrequency).sum();

        for (int i = 0; i < 10; i++) {
            double randomValue = random.nextDouble() * totalFrequency;
            Toy selectedToy = null;

            for (Toy toy : toys) {
                randomValue -= toy.getFrequency();
                if (randomValue <= 0) {
                    selectedToy = toy;
                    break;
                }
            }

            if (selectedToy != null && selectedToy.getQuantity() > 0) {
                selectedToy.decreaseQuantity();
                prizeToys.add(selectedToy);
            }
        }
    }

    public void savePrizeToysToFile() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("prize_toys.txt"))) {
            for (Toy toy : prizeToys) {
                writer.write(toy.getName());
                writer.newLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

class ToyRaffleProgram {
    public static void main(String[] args) {
        ToyStore toyStore = new ToyStore();

        toyStore.addToy(1, "Teddy Bear", 10, 30);
        toyStore.addToy(2, "Lego Set", 15, 25);
        toyStore.addToy(3, "Doll", 8, 20);

        toyStore.updateToyFrequency(2, 15);

        toyStore.startRaffle();
        toyStore.savePrizeToysToFile();
    }
}
