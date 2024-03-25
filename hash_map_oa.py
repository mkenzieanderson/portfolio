# Name: Mackenzie Anderson
# GitHub Username: mkenzieanderson
# Date: March 14, 2024
# Description: Defines the HashMap class, which represents an Open Address
#              hash map data structure. Methods include adding (or updating)
#              a key-value entry to the table, resizing the table in the case
#              that the load factor exceeds 0.5, getting the value of a specific
#              key in the table, determining whether a key exists in the table,
#              calculating the current load factor of the table, calculating the
#              current number of empty buckets in the table, removing a specific
#              key in the table, extracting all active key-value entries in the
#              table, clearing the table of all contents, and setting up an
#              iteration loop to iterate through all active hash entries in the
#              table.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Given some key and value, if this key does not exist in the HashMap, then
        a Hash Entry is created and hashed into the HashMap using the passed
        key and value parameters. If the key is found in the HashMap, then that
        key's value will be updated according to the passed value. This method
        will check that the current load factor is less than 0.5 before adding or
        updating a key. If the load factor is >= 0.5, then the table is resized by
        twice the current capacity.

        :param key:     some string key to add or update in the HashMap
        :param value:   some value to be added/updated with the key
        """
        # resize the table to double the capacity if the load factor is >= 0.5
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity*2)

        # use hash function to locate the index at which the key can be found.
        # add key if not present, or update value if key already exists
        j = 0
        hash_key = self._hash_function(key)
        if self.contains_key(key) is True:          # update existing key
            while self._buckets[(hash_key + j**2) % self._capacity] is not None:
                if self._buckets[(hash_key + j**2) % self._capacity].key == key:
                    self._buckets[(hash_key + j**2) % self._capacity].value = value
                    return
                j += 1
        else:                                       # add new key and value
            while self._buckets[(hash_key + j**2) % self._capacity] is not None:
                if self._buckets[(hash_key + j**2) % self._capacity].is_tombstone is True:
                    self._buckets[(hash_key + j**2) % self._capacity] = HashEntry(key, value)
                    self._size += 1
                    return
                j += 1
            self._buckets[(hash_key + j**2) % self._capacity] = HashEntry(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the Hash table according to the passed new_capacity integer.
        If the requested new_capacity is less than the current size of the
        Hash table, then nothing changes. Otherwise, all non-tombstone hash
        entries are rehashed into the new table of the specified new capacity.
        The new_capacity must be a prime number and result in a load factor
        that is less than 0.5. The new_capacity will be changed if it does not
        meet these criteria.

        :param new_capacity:    an integer representing the new table capacity
        """
        # new_capacity must be prime and greater than the current size
        if new_capacity < self._size:
            return
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # extract all active hash entries, then clear all the buckets
        key_value_tuples = self.get_keys_and_values()
        self._capacity = new_capacity
        self.clear()
        
        # use indirect recursion of put() method to rehash active Hash
        # entries into the resized table
        for index in range(key_value_tuples.length()):
            (key, value) = key_value_tuples[index]
            self.put(key, value)

    def table_load(self) -> float:
        """
        Calculates and returns the current load factor of the Hash table.

        :return:    float number representing the current load factor
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the HashMap

        :return:    integer representing the current number of empty buckets
        """
        return self._capacity - self._size

    def get(self, key: str) -> object:
        """
        Given some key, this method returns the value associated with that key.
        If the key is not in the HashMap, then returns None.

        :param key: some string key to search for in the HashMap

        :return:    the value associated with the key if the key is found in
                    HashMap. If not found, returns None.
        """
        if self._size == 0:
            return
        j = 0
        hash_key = self._hash_function(key)
        while self._buckets[(hash_key + j**2) % self._capacity] is not None:
            if self._buckets[(hash_key + j**2) % self._capacity].key == key:
                return self._buckets[(hash_key + j**2) % self._capacity].value
            j += 1
        return

    def contains_key(self, key: str) -> bool:
        """
        Given some key, returns True if that key exists in the HashMap.
        Returns False if it is not in the HashMap.

        :param key: some string key to search for in the HashMap

        :return:    True if key is found, False if not found
        """
        if self._size == 0:
            return False
        j = 0
        hash_key = self._hash_function(key)
        while self._buckets[(hash_key + j**2) % self._capacity] is not None:
            if self._buckets[(hash_key + j**2) % self._capacity].key == key:
                if self._buckets[(hash_key + j**2) % self._capacity].is_tombstone is False:
                    return True
                else:
                    return False
            j += 1
        return False

    def remove(self, key: str) -> None:
        """
        Given some key, removes this key-value pair from the HashMap if the key exists
        in the HashMap. If the key is not found, then no changes are made.

        :param key: some string key to remove in the HashMap
        """
        if self._size == 0:
            return
        j = 0
        hash_key = self._hash_function(key)
        while self._buckets[(hash_key + j**2) % self._capacity] is not None:
            if self._buckets[(hash_key + j**2) % self._capacity].key == key:
                if self._buckets[(hash_key + j**2) % self._capacity].is_tombstone is False:
                    self._buckets[(hash_key + j**2) % self._capacity].is_tombstone = True
                    self._size -= 1
                return
            j += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns all non-tombstone key-value pairs in the HashMap as tuples
        in a Dynamic Array.

        :return:    DynamicArray of tuples (key, value) for each non-tombstone
                    hash entry in the current HashMap
        """
        tuples_da = DynamicArray()
        for index in range(self._capacity):
            if self._buckets[index] is not None:
                if self._buckets[index].is_tombstone is False:
                    tuples_da.append((self._buckets[index].key, self._buckets[index].value))
        return tuples_da

    def clear(self) -> None:
        """
        Clears the contents of the HashMap without changing the capacity.
        """
        empty_table = DynamicArray()
        for index in range(self._capacity):
            empty_table.append(None)
        self._buckets = empty_table
        self._size = 0

    def __iter__(self):
        """
        Create the iteration loop for the current HashMap
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain the next active Hash Entry and advance the iterator
        """
        try:
            next_hash = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

        while self._buckets[self._index] is None or self._buckets[self._index].is_tombstone is True:
            self._index += 1
            if self._index >= self._capacity:
                raise StopIteration
        next_hash = self._buckets[self._index]
        self._index += 1
        return next_hash


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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
