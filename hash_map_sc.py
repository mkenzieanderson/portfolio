# Name: Mackenzie Anderson
# GitHub Username: mkenzieanderson
# Date: March 14, 2024
# Description: Defines the HashMap class, which represents a separate
#              chaining hash map data structure. Methods include adding
#              and updating keys in the HashMap, removing keys, clearing
#              the HashMap of all contents, getting a value based on its
#              key, getting a dynamic array of tuples of all key-value
#              pairs in the HashMap, resizing the HashMap, calculating
#              the load factor, identifying if a key exists in the HashMap,
#              and returning the number of empty buckets in the HashMap.
#              There is an additional function outside of the HashMap class
#              that uses a HashMap and its methods to calculate the mode(s)
#              from a given DynamicArray of strings.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Given some key and value pair, if this key already exists in the HashMap,
        then update its value with the new value. If the key is not in the HashMap,
        then create a new key-value pair in the HashMap. Will check if the current
        load factor is less than 1. If not, then the HashMap is doubled in size.

        :param key:     string representing the key in the HashMap
        :param value:   some object that will be this key's value in the HashMap
        """
        # resize the table to double the capacity if the load factor is >= 1
        if self.table_load() >= 1:
            self.resize_table(self._capacity*2)

        # use hash function to locate the index at which the key can be found.
        # add key if not present, or update value if key already exists
        index = self._hash_function(key)%self._capacity
        for node in self._buckets[index]:
            if node.key == key:
                node.value = value
                return
        self._buckets[index].insert(key, value)
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the Hash table such that its capacity matches the passed
        new_capacity argument. If new_capacity is less than 1, then this method
        does not change anything. If new_capacity is not prime, then is_prime
        and next_prime will be called to set new_capacity to the next greatest
        prime number.

        :param new_capacity:    integer representing the new capacity of resized
                                Hash table
        """
        if new_capacity < 1:
            return

        # new_capacity must be prime and load factor should be less than 1
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)
        while (self._size-1)/new_capacity >= 1:
            new_capacity *= 2
            new_capacity = self._next_prime(new_capacity)

        # create a new DynamicArray and append an empty LinkedList to each element
        new_table = DynamicArray()
        for index in range(new_capacity):
            new_table.append(LinkedList())

        # gather all key-value pairs stored as tuples in a DynamicArray and use the
        # hash function mod-divided by the new_capacity to append each key-value in
        # the new hash table
        key_value_tuples = self.get_keys_and_values()
        for index in range(self._size):
            (key, value) = key_value_tuples[index]
            new_table[self._hash_function(key)%new_capacity].insert(key, value)
        self._capacity = new_capacity
        self._buckets = new_table

    def table_load(self) -> float:
        """
        Calculates and returns the current load factor of the Hash table.

        :return:    Float representing the current load factor of the Hash table
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the HashMap.

        :return:    integer representing the number of empty buckets in the HashMap.
        """
        empty_counter = 0
        for index in range(self._buckets.length()):
            if self._buckets[index].length() == 0:
                empty_counter += 1
        return empty_counter

    def get(self, key: str) -> object:
        """
        Given some key, this method returns its value if the key is in the HashMap.
        If the key is not in the HashMap, then this method returns None. Uses
        hash_function_1() to find the bucket for this key.

        :param key:     string form of a key to be searched in the HashMap

        :return:        Value if key is found, None if key is not found
        """
        if self._size == 0:
            return None
        for node in self._buckets[self._hash_function(key)%self._capacity]:
            if node.key == key:
                return node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Given some key, returns True if the key is found in the HashMap. Returns
        False if not found in the HashMap.

        :param key:     string of key to be searched for in HashMap

        :return:        True if the key is found in the HashMap, False otherwise
        """
        if self._size == 0:
            return False
        for node in self._buckets[self._hash_function(key)%self._capacity]:
            if node.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Given some key, this method removes that key and its value from the HashTable
        if the key is found. If the key is not found, then nothing changes.

        :param key:     string of some key to be removed from the HashTable
        """
        if self._size == 0:
            return
        if self._buckets[self._hash_function(key)%self._capacity].remove(key) is True:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray of (key, value) tuples of all key-value pairs
        in the current HashMap.

        :return:    DynamicArray of (key, value) tuples of all key-value pairs
        """
        tuples_da = DynamicArray()
        for index in range(self._capacity):
            for node in self._buckets[index]:
                tuples_da.append((node.key, node.value))
        return tuples_da

    def clear(self) -> None:
        """
        Clears all the contents of the HashMap, but does not modify the capacity.
        """
        new_buckets = DynamicArray()
        for bucket in range(self._capacity):
            new_buckets.append(LinkedList())
        self._buckets = new_buckets
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receives some DynamicArray, which is not required to be sorted. Analyze the
    elements of the array and returns a tuple containing a DynamicArray of the
    mode(s), and an integer representing the frequency of this mode(s). It can
    be assumed that the passed array will contain at least one element, and all
    elements will be strings.

    :param da:  some DynamicArray of string elements, contains at least 1 element

    :return:    a tuple with a dynamic array of the mode(s), and an integer
                representing the frequency of the mode(s).
    """
    # add each unique string element to the HashMap. The key is the string
    # element, and its value is its frequency in the dynamic array
    map = HashMap()
    for index in range(da.length()):
        value = 1
        if map.contains_key(da[index]) is True:
            value = map.get(da[index]) + 1
        map.put(da[index], value)

    # iterate through the key-value pairs and update the mode Dynamic Array
    # and frequency integer according to the highest value in the tuples
    key_value_tuples = map.get_keys_and_values()
    mode_array = DynamicArray()
    mode_frequency = 1
    for index in range(map.get_size()):
        key, value = key_value_tuples[index]
        if value > mode_frequency:
            mode_frequency = value
            mode_array = DynamicArray()
            mode_array.append(key)
        elif value == mode_frequency:
            mode_array.append(key)
    return (mode_array, mode_frequency)



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
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
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
