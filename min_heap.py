# Name: Mackenzie Anderson
# OSU Email: andemac2@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: A5
# Due Date: March 4, 2024
# Description: Defines the MinHeap class, which uses DynamicArray
#              objects to implement the Min Heap data structure.
#              Methods of MinHeap include adding some node to the
#              heap, getting and/or removing the minimum value from
#              the heap, getting the size of the heap, clearing the
#              heap of all its contents, and building a MinHeap from
#              some DynamicArray object. There is an additional method
#              outside the MinHeap class that uses the HeapSort algorithm
#              to sort a DynamicArray in non-ascending order.


from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return 'HEAP ' + str(heap_data)

    def add(self, node: object) -> None:
        """
        Adds the given node (value) to the MinHeap to its appropriate
        location.

        :param node:    some node (aka value) to be added to the heap
        """
        # add the node to the end of the heap to start the process
        self._heap.append(node)

        # if the new node is less than its parent, switch spots. Repeat
        # until the new node is greater than its parent, and less than
        # its children
        index = self.size()-1
        is_added = False
        while is_added is False:
            if index == 0:              # new node is the root of the heap
                is_added = True
            else:
                parent_index = (index-1)//2
                if self._heap[index] < self._heap[parent_index]:
                    self._heap[index] = self._heap[parent_index]
                    self._heap[parent_index] = node
                    index = parent_index
                else:
                    is_added = True     # node is in the appropriate spot

    def is_empty(self) -> bool:
        """
        Returns True if the heap is empty, False otherwise

        :return:    True is heap is empty, False if not empty
        """
        return self._heap.is_empty()

    def get_min(self) -> object:
        """
        Returns the minimum value in the heap, but does not remove this
        value. If the heap is empty, then the MinHeapException is raised

        :return:    the minimum value in the heap
        """
        if self.is_empty() is True:
            raise MinHeapException
        return self._heap[0]

    def remove_min(self) -> object:
        """
        Removes and returns the minimum node in the heap. If the heap is
        empty, then the MinHeapException is raised.

        :return:    the key of the minimum node
        """
        # heap is empty - raise MinHeapException
        if self.is_empty() is True:
            raise MinHeapException

        # special case: the heap only has one node
        removed_key = self._heap[0]
        heap_size = self.size()
        if heap_size == 1:
            self._heap.remove_at_index(0)
            return removed_key

        # Use downwards percolation to reset the heap after the root removal
        self._heap[0] = self._heap[heap_size-1]
        self._heap.remove_at_index(heap_size-1)
        _percolate_down(self._heap, 0)
        return removed_key

    def build_heap(self, da: DynamicArray) -> None:
        """
        Receives a Dynamic Array and builds a MinHeap from that data, which is
        stored in this MinHeap's _heap data member. Any data current in _heap
        will be overwritten.

        :param da:  Some DynamicArray object
        """
        # identify the first non-leaf element
        self._heap = DynamicArray(da)
        non_leaf_index = (self.size()//2)-1

        # percolate each non-leaf element downwards, if needed
        for index in range(non_leaf_index, -1, -1):
            _percolate_down(self._heap, index)

    def size(self) -> int:
        """
        Returns the number of elements inside the heap.

        :return:    integer representing the number of elements in the heap
        """
        return self._heap.get_size()

    def clear(self) -> None:
        """
        Clears the heap of all its contents.
        """
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """
    Given some Dynamic Array, this method will sort its contents in
    non-ascending order using the Heapsort algorithm. The sort is completed
    in place without creating any new data structures.

    :param da:  Some DynamicArray object where all elements are homogenous
                and there is at least one element in the array
    """
    # modify the DynamicArray such that it is in MinHeap organization
    for index in range((da.get_size()//2)-1, -1, -1):
        _percolate_down(da, index)

    # Use the HeapSort algorithm to organize the array, in place, in
    # non-ascending order
    k = da.get_size()-1
    while k > 0:
        value = da[0]
        da[0] = da[k]
        da[k] = value
        k -= 1
        _percolate_down(da, 0, k)

def _percolate_down(da: DynamicArray, parent: int, last=None) -> None:
    """
    Given some MinimumHeap in dynamic array form and index of some value in
    the array, this method performs downwards percolation to ensure that the
    value at this index in its correct location.

    :param da:      a DynamicArray that represents a minimum heap
    :param parent:  the integer index of the value to percolate downwards
    :param last:    an integer representing the index of the last element to
                    percolate downwards to. Is default set to None if no last
                    argument is passed
    """
    value = da[parent]
    if last is None:              # if last was not specified, it becomes
        last = da.get_size()-1    # the last element of the dynamic array
    is_removed = False

    while is_removed is False:
        if parent*2+1 > last:     # reached the end of the heap
            is_removed = True
        elif parent*2+2 > last:
            if da[parent] > da[parent*2+1]:
                da[parent] = da[parent * 2 + 1]
                da[parent * 2 + 1] = value
            is_removed = True
        elif da[parent] <= da[parent*2+1] and da[parent] <= da[parent*2+2]:
            is_removed = True           # node is in appropriate spot
        else:
            if da[parent* 2+1] <= da[parent*2+2]:
                new_parent = parent*2+1  # swap with left child
            else:
                new_parent = parent*2+2  # swap with right child
            da[parent] = da[new_parent]
            da[new_parent] = value
            parent = new_parent


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)
