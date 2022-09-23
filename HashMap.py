# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out



    def get_index(self,key) -> int:
        """
        Method returns an index for given key
        """
        # testing to find which hash_function is being used
        index = None
        if self.hash_function('ab') == 195:
            hash = hash_function_1(key)
            index = hash % self.capacity

        elif self.hash_function('ab') == 293:
            hash = hash_function_2(key)
            index = hash % self.capacity

        return index


    def clear(self) -> None:
        """
        Method clears the contents of the hash map. It does not change the underlying hash
        table capacity
        """
        # creates new data storage, each bucket in the new dynamic array with a linked list and sets
        # the size to zero while maintaining the same original capacity
        new_da = DynamicArray()
        self.buckets = new_da
        for _ in range(0,self.capacity):
            self.buckets.append(LinkedList())
        self.size = 0



    def get(self, key: str) -> object:
        """
        Method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        """
        # gathers appropriate index from chosen hash function
        index = self.get_index(key)

        # iterates through linkedlist using dunder method, if there is a key match we return it's value
        # if there are no matches, we return None
        for node in self.buckets[index]:
            if node.key == key:
                return node.value
        return None



    def put(self, key: str, value: object) -> None:
        """
        Method updates the key / value pair in the hash map, removing key/replacing with new
        key if duplicates
        """
        # gets correct index from hash function we are using
        index = self.get_index(key)

        # if the key exists in any linked list, we remove and replace it with a new key/value pair
        for node in self.buckets[index]:
            if node.key == key:
                self.buckets[index].remove(key)
                self.buckets[index].insert(key,value)
                return

        # if the key does not exist anywhere in the linked list, we add it ourselves and increment size
        else:
            self.buckets[index].insert(key,value)
            self.size += 1



    def remove(self, key: str) -> None:
        """
        Method removes the given key and its associated value from the hash map. If a given
        key is not in the hash map, the method does nothing
        """
        # gets appropriate index for the hash function we are using
        index = self.get_index(key)

        # iterates through the linked list at the given index
        # if the key matches the provided key, we remove the key/value pair and decriment size
        for node in self.buckets[index]:
            if node.key == key:
                self.buckets[index].remove(key)
                self.size -= 1



    def contains_key(self, key: str) -> bool:
        """
        Method returns True if the given key is in the hash map, otherwise it returns False
        """
        # if hash map is empty, return False
        if self.buckets.length() == 0:
            return False

        else:
            for _ in range(0, self.buckets.length()):
                # checks each bucket for key, if exists then returns with True, otherwise returns False
                if self.buckets[_].contains(key) != None:
                    return True
            return False



    def empty_buckets(self) -> int:
        """
        Method returns the number of empty buckets in the hash table
        """
        count = 0
        # counts number of buckets with lengths of zero
        for bucket in range(0, self.buckets.length()):
            if self.buckets[bucket].length() == 0:
                count += 1
        return count



    def table_load(self) -> float:
        """
        Method returns the current hash table load factor
        """
        # calculates and returns load factor
        load_factor = self.size / self.capacity
        return load_factor



    def resize_table(self, new_capacity: int) -> None:
        """
        Method changes the capacity of the internal hash table.  If
        new_capacity is less than 1, method should do nothing.
        """
        # if the new capacity is less than 1, method returns and does nothing
        if new_capacity < 1:
            return

        # creates new dynamic array
        new_da = DynamicArray()

        # saves old capacity for us to iterate through
        old_capacity = self.capacity

        # updates capacity
        self.capacity = new_capacity

        # appends a new linked list for each bucket in capacity to our new dynamic array
        for _ in range(0, self.capacity):
            new_da.append(LinkedList())

        # goes through each bucket of original bucket and gathers key/value pairs for new_da(new bucket)
        for _ in range(0, old_capacity):
            # gets sll at bucket for checking if there are any SLnodes
            sll = self.buckets.get_at_index(_)
            # if there are SLnodes, then we look to gather the keys
            if sll.length() != 0:
                current = self.buckets.get_at_index(_)
                for node in current:
                    index = self.get_index(node.key)
                    new_da[index].insert(node.key,node.value)

        # assign new bucket as new_da, which we've been building
        self.buckets = new_da



    def get_keys(self) -> DynamicArray:
        """
        Method returns a DynamicArray that contains all keys stored in hash map
        """
        # creates da to hold keys
        keys = DynamicArray()

        # goes through each bucket of original bucket and gathers keys from the linked lists in buckets
        for _ in range(0, self.capacity):
            # gets sll at bucket for checking if there are any SLnodes/keys
            sll = self.buckets.get_at_index(_)
            # if there are SLnodes with keys, we append them to our keys DA
            if sll.length() != 0:
            #if self.buckets[_] != None:
                # set current to SLNode
                current = self.buckets.get_at_index(_)
                # gathers all keys from linked list
                for node in current:
                    keys.append(node.key)
        return keys



# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
