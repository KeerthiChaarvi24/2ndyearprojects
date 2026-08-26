public class LinkedList {

    private Node head;
    private Node tail;
    private int length;

    // Node
    class Node {
        int value;
        Node next;

        Node(int value) {
            this.value = value;
        }
    }

    // Constructor
    public LinkedList(int value) {
        Node newNode = new Node(value);
        head = newNode;
        tail = newNode;
        length = 1;
    }

    // Print List
    public void printList() {
        Node temp = head;

        while (temp != null) {
            System.out.println(temp.value);
            temp = temp.next;
        }
    }

    // Append
    public void append(int value) {
        Node newNode = new Node(value);

        if (length == 0) {
            head = newNode;
            tail = newNode;
        } else {
            tail.next = newNode;
            tail = newNode;
        }

        length++;
    }

    // Remove Last
    public Node removeLast() {

        if (length == 0) {
            return null;
        }

        Node temp = head;
        Node pre = head;

        while (temp.next != null) {
            pre = temp;
            temp = temp.next;
        }

        tail = pre;
        tail.next = null;
        length--;

        if (length == 0) {
            head = null;
            tail = null;
        }

        return temp;
    }

    // Prepend
    public void prepend(int value) {
        Node newNode = new Node(value);

        if (length == 0) {
            head = newNode;
            tail = newNode;
        } else {
            newNode.next = head;
            head = newNode;
        }

        length++;
    }

    // Remove First
    public Node removeFirst() {

        if (length == 0) {
            return null;
        }

        Node temp = head;
        head = head.next;
        temp.next = null;
        length--;

        if (length == 0) {
            tail = null;
        }

        return temp;
    }

    // Get
    public Node get(int index) {

        if (index < 0 || index >= length) {
            return null;
        }

        Node temp = head;

        for (int i = 0; i < index; i++) {
            temp = temp.next;
        }

        return temp;
    }

    // Set
    public boolean set(int index, int value) {

        Node temp = get(index);

        if (temp == null) {
            return false;
        }

        temp.value = value;
        return true;
    }

    // Insert
    public boolean insert(int index, int value) {

        if (index < 0 || index > length) {
            return false;
        }

        if (index == 0) {
            prepend(value);
            return true;
        }

        if (index == length) {
            append(value);
            return true;
        }

        Node newNode = new Node(value);
        Node temp = get(index - 1);

        newNode.next = temp.next;
        temp.next = newNode;

        length++;
        return true;
    }

    // Remove
    public Node remove(int index) {

        if (index < 0 || index >= length) {
            return null;
        }

        if (index == 0) {
            return removeFirst();
        }

        if (index == length - 1) {
            return removeLast();
        }

        Node prev = get(index - 1);
        Node temp = prev.next;

        prev.next = temp.next;
        temp.next = null;

        length--;

        return temp;
    }

    // Reverse
    public void reverse() {

        Node temp = head;
        head = tail;
        tail = temp;

        Node after;
        Node before = null;

        for (int i = 0; i < length; i++) {
            after = temp.next;
            temp.next = before;
            before = temp;
            temp = after;
        }
    }

    // Main
    public static void main(String[] args) {

        LinkedList myLinkedList = new LinkedList(10);

        myLinkedList.append(20);
        myLinkedList.append(30);
        myLinkedList.append(40);

        myLinkedList.prepend(5);

        myLinkedList.printList();

        System.out.println("Get: " + myLinkedList.get(2).value);

        myLinkedList.set(2, 25);

        myLinkedList.insert(2, 15);

        myLinkedList.remove(2);

        myLinkedList.reverse();

        System.out.println("After reverse:");
        myLinkedList.printList();
    }
}