import heapq
import argparse

class PersistentPriorityQueue:
    """
    A persistent priority queue implemented using a text file for storage.
    """
    def __init__(self, file_path):
        """
        Initialize the persistent priority queue.

        Parameters:
        - file_path (str): The path to the text file used for storage.
        """
        self.file_path = file_path

    def push(self, item, priority):
        """
        Push an item with a given priority into the queue.

        Parameters:
        - item: The item to push into the queue.
        - priority: The priority associated with the item.
        """
        with open(self.file_path, 'a') as file:
            file.write(f"{priority} {item}\n")

    def pop(self):
        """
        Pop the item with the highest priority from the queue and remove it.

        Returns:
        - item: The item with the highest priority.
        """
        # Read all items from the file and store them in a list of (priority, item) tuples
        items = []
        with open(self.file_path, 'r') as file:
            for line in file:
                priority, item = line.strip().split(' ', 1)
                items.append((int(priority), item))

        if not items:
            raise IndexError("Queue is empty")

        # Find the item with the highest priority
        highest_priority_item = min(items, key=lambda x: x[0])

        # Remove the item from the list and update the file
        items.remove(highest_priority_item)
        with open(self.file_path, 'w') as file:
            for priority, item in items:
                file.write(f"{priority} {item}\n")

        return highest_priority_item[1]

    def peek(self):
        """
        Get the item with the highest priority without removing it from the queue.

        Returns:
        - item: The item with the highest priority.
        """
        items = []
        with open(self.file_path, 'r') as file:
            for line in file:
                priority, item = line.strip().split(' ', 1)
                items.append((int(priority), item))

        if not items:
            raise IndexError("Queue is empty")

        highest_priority_item = min(items, key=lambda x: x[0])
        return highest_priority_item[1]

    def is_empty(self):
        """
        Check if the queue is empty.

        Returns:
        - bool: True if the queue is empty, False otherwise.
        """
        with open(self.file_path, 'r') as file:
            return not any(True for line in file)

    def change_priority(self, target_item, new_priority):
        """
        Change the priority of a specific item in the queue.

        Parameters:
        - target_item: The item whose priority you want to change.
        - new_priority: The new priority to assign to the item.
        """
        items = []
        updated_items = []

        # Read all items from the file and store them in a list of (priority, item) tuples
        with open(self.file_path, 'r') as file:
            for line in file:
                priority, item = line.strip().split(' ', 1)
                items.append((int(priority), item))

        # Find the target item and update its priority
        found = False
        for priority, item in items:
            if item == target_item:
                updated_items.append((new_priority, item))
                found = True
            else:
                updated_items.append((priority, item))

        if not found:
            raise ValueError(f"Item '{target_item}' not found in the queue.")

        # Write the updated items back to the file
        with open(self.file_path, 'w') as file:
            for priority, item in updated_items:
                file.write(f"{priority} {item}\n")

    def reorder_priorities(self):
        """
        Reorder the priorities in the queue to be consecutive starting from 1.
        """
        items = []
        updated_items = []

        # Read all items from the file and store them in a list of (priority, item) tuples
        with open(self.file_path, 'r') as file:
            for line in file:
                priority, item = line.strip().split(' ', 1)
                items.append((int(priority), item))

        # Sort the items by their existing priorities
        items.sort(key=lambda x: x[0])

        # Assign new consecutive priorities starting from 1
        new_priority = 1
        for _, item in items:
            updated_items.append((new_priority, item))
            new_priority += 1

        # Write the updated items back to the file
        with open(self.file_path, 'w') as file:
            for priority, item in updated_items:
                file.write(f"{priority} {item}\n")

    def print_queue(self):
        """
        Print the entire contents of the priority queue.
        """
        with open(self.file_path, 'r') as file:
            print(file.read())


    def insert_and_shift_up(self, item, target_priority):
        """
        Insert an item at a specific priority and shift up the priorities of all subsequent items by 1.

        Parameters:
        - item (str): The item to insert.
        - target_priority (int): The desired priority for the item.

        Returns:
        None

        Note: Feel free to use the reorder method after to make them consecutive
        """
        items = []

        # Read all items from the file into a list of (priority, item) tuples
        with open(self.file_path, 'r') as file:
            for line in file:
                priority, existing_item = line.strip().split(' ', 1)
                items.append((int(priority), existing_item))

        # Increment the priorities of items that are >= target_priority
        items = [(p + 1 if p >= target_priority else p, i) for p, i in items]

        # Insert the new item
        items.append((target_priority, item))

        # Sort the updated items
        items.sort(key=lambda x: x[0])

        # Write the updated items back to the file
        with open(self.file_path, 'w') as file:
            for priority, existing_item in items:
                file.write(f"{priority} {existing_item}\n")



# Example usage:
if __name__ == "__main__":
    pq = PersistentPriorityQueue("priority_queue.txt")

    parser = argparse.ArgumentParser(description="Persistent Priority Queue")
    parser.add_argument("--file", type=str, default="priority_queue.txt", help="Path to the storage file")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--push", nargs=2, metavar=("item", "priority"), help="Push an item with a priority")
    group.add_argument("--pop", action="store_true", help="Pop the highest priority item")
    group.add_argument("--peek", action="store_true", help="Peek at the highest priority item")
    group.add_argument("--is_empty", action="store_true", help="Check if the queue is empty")
    group.add_argument("--change_priority", nargs=2, metavar=("item", "new_priority"), help="Change the priority of an item")
    group.add_argument("--reorder_priorities", action="store_true", help="Reorder priorities in the queue")
    group.add_argument("--print_queue", action="store_true", help="Print the entire queue")

    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument("--insert_and_shift_up", nargs=2, metavar=("item", "target_priority"), help="Insert an item and shift up priorities")

    args = parser.parse_args()

if args.push: # Example: --push "Task C" 3
    item, priority = args.push
    pq.push(item, int(priority))
elif args.pop: # Example: --pop
    item = pq.pop()
    print(f"Popped item: {item}")
elif args.peek: # Example: --peek
    item = pq.peek()
    print(f"Peeked item: {item}")
elif args.is_empty: # Example: --is_empty
    is_empty = pq.is_empty()
    print(f"Queue is empty: {is_empty}")
elif args.change_priority: # Example: --change_priority "Task A" 2
    item, new_priority = args.change_priority
    pq.change_priority(item, int(new_priority))
elif args.reorder_priorities: # Example: --reorder_priorities
    pq.reorder_priorities()
elif args.print_queue: # Example: --print_queue
    pq.print_queue()
elif args.insert_and_shift_up: # Example: --insert_and_shift_up "Task D" 2
    item, target_priority = args.insert_and_shift_up
    pq.insert_and_shift_up(item, int(target_priority))
