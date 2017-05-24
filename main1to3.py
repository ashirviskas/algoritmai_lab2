import random
import time
import sys
import os
import matplotlib.pyplot as plt
import struct
import string
import multiprocessing
from multiprocessing import Pool

# from numpy.core.tests.test_multiarray import x


class Node:
    def __init__(self, value = None, next = None):
        self.value = value
        self.next = next

    def __str__(self):
        return 'Node ['+str(self.value)+']'


class LinkedList:
    def __init__(self):
        self.first = None
        self.last = None

    def insert(self, x):
        if self.first == None:
            self.first = Node(x, None)
            self.last = self.first
        elif self.last == self.first:
            self.last = Node(x, None)
            self.first.next = self.last
        else:
            current = Node(x, None)
            self.last.next = current
            self.last = current

    def __str__(self):
        if self.first != None:
            current = self.first
            out = 'LinkedList [\n' +str(current.value) +' '
            while current.next != None:
                current = current.next
                out += str(current.value) + ' '
            return out + ']'
        return 'LinkedList []'

    def clear(self):
        self.__init__()

    def length(self):
        node = self.first
        n = 0
        if node != None:
            n = 1
        while node.next != None:
            n += 1
            node = node.next
        return n


class Student:
    def __init__(self, name = None):
        self.name = name

    def __str__(self):
        return 'Name: ' + self.name


class HashTable:
    def __init__(self, size, from_file = False, filename = "", space_for_name = 32):
        self.size = size
        self.table = [None for y in range(size)]
        self.from_file = from_file
        self.filename = filename
        self.full = False
        self.space_for_name = space_for_name
        if from_file:
            self.fill_with_zerooos()

    def __str__(self):
        string = ""
        if not self.from_file:
            for student in self.table:
                string = string + student.name + "; "
        else:
            with open(self.filename, "r") as file:
                string = file.read()
                file.close()
        return string



    def Retrieve(self, key):
        bytes = str.encode(key)
        number = int.from_bytes(bytes, sys.byteorder)
        hash = number % self.size
        index = hash
        if not self.from_file:
            for j in range(self.size):
                index = (hash + j * j) % self.size
                if self.table[index] is not None:
                    if self.table[index].name == key:
                        return self.table[index]
            return False
        else:
            with open(self.filename, "r+b", 0) as file:
                data = file.read()
                for j in range(self.size):
                    index = (hash + j * j) % self.size
                    if data[index * self.space_for_name:index * self.space_for_name + self.space_for_name] != (
                        ' ' * self.space_for_name).encode():
                        if data[index * self.space_for_name:index * self.space_for_name + self.space_for_name] != (key + (' '*(self.space_for_name - len(key)))).encode():
                            return data[index * self.space_for_name:index * self.space_for_name + self.space_for_name]
                return False

    def checkIfFull(self):
        full = True
        if not self.from_file:
            for student in self.table:
                if student is None:
                    return False
        else:
            with open(self.filename, "r+b", 0) as file:
                data = file.read()
                for i in range(0, self.space_for_name):
                    if data[i*self.space_for_name:i*self.space_for_name+self.space_for_name+1] != ' '*self.space_for_name:
                        return False
        return full

    def fill_with_zerooos(self):
        file = open(self.filename, "wb")
        for i in range(self.size):
            zero = 0
            namestring = " "*self.space_for_name
            bytes = namestring.encode('utf-8')
            file.write(bytes)
            #print(bytes)
        file.close()

    def QuadraticHashInsert(self, student):
        if (self.checkIfFull()):
            print("Tabley is fulley")
            return False
        key = student.name
        bytes = str.encode(key)
        number = int.from_bytes(bytes, byteorder='big')
        hash = number % self.size
        index = hash
        if not self.from_file:
            for j in range(self.size):
                index = (hash + j * j) % self.size
                if self.table[index] is None:
                    self.table[index] = student
                    return True
        else:
            with open(self.filename, "r+b", 0) as file:
                data = file.read()
                for j in range(self.size):
                    index = (hash + j * j) % self.size
                    if data[index*self.space_for_name:index*self.space_for_name+self.space_for_name] == (' '*self.space_for_name).encode():
                        part_one = data[:self.space_for_name*(index)]
                        part_three = data[self.space_for_name*(index+1):]
                        part_two = (student.name + (' '*(self.space_for_name - len(student.name)))).encode()
                        data = part_one+part_two+part_three
                        file.seek(0)
                        file.write(data)
                        file.close()
                        return True
        return False

    def Remove(self, student):
        key = student.name
        bytes = str.encode(key)
        number = int.from_bytes(bytes)
        hash = number % self.size
        index = hash
        j = 1
        while self.table[index] is not None and self.table[index] != student:
            index = (hash + j * j) % self.size
            j += 1
        if self.table[index] is None:
            return False
        else:
            self.table[index] = None
            return True


def file_size(filename):
    st = os.stat(filename)
    return st.st_size


def file_len(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
def do_nothing(self):
    return
def populate_binary_file_array(filename, min, max, size):
    file = open(filename, 'wb', 0)
    for i in range(size):
        rndint = random.randint(min,max)
        my_bytes = rndint.to_bytes(4, sys.byteorder)
        my_bytearray = bytearray(my_bytes)
        file.write(my_bytes)
        #print(rndint)
    file.close()


def populate_binary_file_list(filename, min, max, size):
    file = open(filename, 'wb', 0)
    for i in range(size):
        rndint = random.randint(min, max)
        my_bytes = rndint.to_bytes(4, sys.byteorder)
        file.write(my_bytes)
        if (i != size-1):
            next_node = (i+1).to_bytes(4, sys.byteorder)
            file.write(next_node)
            my_bytearray = bytearray(my_bytes + next_node)
        else:
            next_node = (2147483647).to_bytes(4, sys.byteorder)
            file.write(next_node)
        #file.write(my_bytearray)
        #print(rndint)
    file.close()


def swap_in_file_array(filename, a_ind, b_ind, linked_list=False):
    with open(filename, "r+b", 0) as file:
        data = file.read()
        tuples = [data[i:i+4] for i in range(0, len(data), 4)]
        a = []
        b = []
        step = 1
        if linked_list:
            step = 2
        for i in range(0, (len(tuples)), step):
            if i == a_ind:
                a = tuples[i]
                # print(struct.unpack("i", tupples[i])[0])
            if i == b_ind:
                b = tuples[i]
        tuples[b_ind] = a
        tuples[a_ind] = b
        data = b''.join(tuples)
        file.seek(0)
        file.write(data)
        file.close()
        return True

def set_bytevalue_file(filename, value, index):
    with open(filename, "r+b", 0) as file:
        data = file.read()
        tuples = [data[i:i + 4] for i in range(0, len(data), 4)]
        tuples[index] = struct.pack("i", value)
        data = b''.join(tuples)
        file.seek(0)
        file.write(data)
        file.close()
        return True


def counting_sort_linked(aList, k): #Counting Sort, k is max value
    counter = [0] * (k + 1)
    node = aList.first
    if node != None:
        counter[node.value] += 1
        while node.next != None:
            node = node.next
            counter[node.value] += 1
    #for i in aList:
      #counter[i] += 1
    node = aList.first
    for i in range( len( counter ) ):
        for x in range (counter[i]):
            node.value = i
            node = node.next


def counting_sort_linked_file(filename): #need to do something with max value. Probalby. Maybe not
    counter = [0] * (10000 + 1)
    node = 0
    if node < 2147483647:
        file = open(filename, "rb", 0)
        data = file.read()
        file.close()
        tuples = [data[i:i + 4] for i in range(0, len(data), 4)]
        counter[struct.unpack("i", tuples[node*2])[0]] += 1
        while struct.unpack("i", tuples[node*2+1])[0] < 2147483647:
            node = struct.unpack("i", tuples[node*2+1])[0]
            counter[struct.unpack("i", tuples[node*2])[0]] += 1
    file = open(filename, "rb", 0)
    data = file.read()
    file.close()
    tuples = [data[i:i + 4] for i in range(0, len(data), 4)]
    node = 0
    for i in range(len(counter)):
        for x in range (counter[i]):
            set_bytevalue_file(filename, i, node*2)
            node = struct.unpack("i", tuples[node * 2 + 1])[0]


def counting_sort_array(arrray, k):
    counter = [0] * (k + 1)
    for i in arrray:
        counter[i] += 1
    ndx = 0
    for i in range(len(counter)):
        while 0 < counter[i]:
            arrray[ndx] = i
            ndx += 1
            counter[i] -= 1


def counting_sort_array_file(filename):
    k = 10000
    counter = [0] * (k + 1)
    file = open(filename, "rb", 0)
    data = file.read()
    file.close()
    tuples = [data[i:i + 4] for i in range(0, len(data), 4)]
    for i in tuples:
        counter[struct.unpack("i", i)[0]] += 1
    ndx = 0
    for i in range(len(counter)):
        while 0 < counter[i]:
            set_bytevalue_file(filename, i, ndx)
            ndx += 1
            counter[i] -= 1


def selection_sort_linked(aList):  # Selection Sort
    node0 = aList.first
    while (node0 != None):
        node_min = node0
        node1 = node0
        while (node1 != None):
            if (node_min.value > node1.value):
                node_min = node1
            node1 = node1.next
        temp = Node(node0.value)
        node0.value = node_min.value
        node_min.value = temp.value
        node0 = node0.next

def selection_sort_linked_file(filename):  # Selection Sort
    node0 = 0
    while (node0 < 2147483647):
        node_min = node0
        node1 = node0
        while (node1 < 2147483647):
            file = open(filename, "rb", 0)
            data = file.read()
            file.close()
            tuples = [data[i:i + 4] for i in range(0, len(data), 4)]
            if struct.unpack("i", tuples[node_min*2])[0] > struct.unpack("i", tuples[node1*2])[0]:
                node_min = node1
            node1 = struct.unpack("i", tuples[node1*2+1])[0]
        swap_in_file_array(filename, node0*2, node_min*2)
        node0 = struct.unpack("i", tuples[node0 * 2 + 1])[0]


def selection_sort_array(array):
    for fillslot in range(len(array) - 1, 0, -1):
        positionOfMax = 0
        for location in range(1, fillslot + 1):
            if array[location] > array[positionOfMax]:
                positionOfMax = location
        temp = array[fillslot]
        array[fillslot] = array[positionOfMax]
        array[positionOfMax] = temp

def selection_sort_array_file(filename):
    length = file_size(filename)/4
    length = int(length)
    for fillslot in range(length-1, 0, -1):
        positionOfMax = 0
        for location in range(1, fillslot + 1):
            file = open(filename, "rb", 0)
            data = file.read()
            file.close()
            tuples = [data[i:i + 4] for i in range(0, len(data), 4)]
            if struct.unpack("i", tuples[location])[0] > struct.unpack("i", tuples[positionOfMax])[0]:
                positionOfMax = location
        swap_in_file_array(filename,fillslot,positionOfMax)



def populate_list(aList, min, max, n):
        for i in range (n):
            aList.insert(random.randrange(min, max, 1))


def populate_array(array, min, max, n):
    for i in range(n):
        array.append(random.randrange(min, max, 1))

def do_CSLLF(sizes):
    times = []
    for size in sizes:
        print("FILE Sorting Linked with counting sort, size: ", '{:>10}'.format(size))
        populate_binary_file_list("linked_data", 0, 10000, size)
        start_time = time.time()
        counting_sort_linked_file("linked_data")
        elapsed = time.time() - start_time
        times.append(elapsed)
        print("Time elapsed: ", time.time() - start_time)
    return times

def do_CSLL(sizes):
    times = []
    for size in sizes:
        L = LinkedList()
        populate_list(L, 0, 10000, size)
        print("Sorting Linked List with counting sort, size: ", '{:>10}'.format(size))
        start_time = time.time()
        counting_sort_linked(L, 10000)
        #print("Sorted Linked List:",L)
        elapsed = time.time() - start_time
        times.append(elapsed)
        print("Time elapsed: ",time.time() - start_time)
        L.clear()
    return times

def do_CSA(sizes):
    times = []
    for size in sizes:
        Array = []
        populate_array(Array, 0, 10000, size)
        #print(Array)
        print("Sorting Array with counting sort, size: ", '{:>10}'.format(size))
        start_time = time.time()
        counting_sort_array(Array, 10000)
        #print(Array)
        elapsed = time.time() - start_time
        times.append(elapsed)
        print("Time elapsed: ",time.time() - start_time)
    return times


def do_SSLL(sizes):
    times = []
    L = LinkedList()
    for size in sizes:
        populate_list(L, 0, 10000, size)
        print("Sorting Linked List with selection sort, size: ", '{:>10}'.format(size))
        start_time = time.time()
        selection_sort_linked(L)
        #print("Sorted Linked List:",L)
        elapsed = time.time() - start_time
        times.append(elapsed)
        print("Time elapsed: ",time.time() - start_time)
        L.clear()
    return times


def do_SSA(sizes):
    times = []
    for size in sizes:
        Array = []
        populate_array(Array, 0, 10000, size)
        print("Sorting Array with selection sort, size: ", '{:>10}'.format(size))
        start_time = time.time()
        selection_sort_array(Array)
        elapsed = time.time() - start_time
        times.append(elapsed)
        print("Time elapsed: ", time.time() - start_time)
    return times


def do_SSAF(sizes):
    times = []
    for size in sizes:
        print("FILE Sorting Array with selection sort, size: ", '{:>10}'.format(size))
        populate_binary_file_array("arr_data", 0, 10000, size)
        start_time = time.time()
        selection_sort_array_file("arr_data")
        elapsed = time.time() - start_time
        times.append(elapsed)
        print("Time elapsed: ", time.time() - start_time)
    return times


def do_SSLLF(sizes):
    times = []
    for size in sizes:
        print("FILE Sorting Linked with selection sort, size: ", '{:>10}'.format(size))
        populate_binary_file_list("linked_data", 0, 10000, size)
        start_time = time.time()
        selection_sort_linked_file("linked_data")
        elapsed = time.time() - start_time
        times.append(elapsed)
        print("Time elapsed: ", time.time() - start_time)
    return times


def do_CSAF(sizes):
    times = []
    for size in sizes:
        print("FILE Sorting Array with counting sort, size: ", '{:>10}'.format(size))
        populate_binary_file_array("arr_data", 0, 10000, size)
        start_time = time.time()
        counting_sort_array_file("arr_data")
        elapsed = time.time() - start_time
        times.append(elapsed)
        print("Time elapsed: ", time.time() - start_time)
    return times
def do_hash_file(sizes, from_file = False, filename = ""):
    times = []
    for size in sizes:
        hashtable = HashTable(size,from_file,filename)
        print("FILE Hash table search, size: ", '{:>10}'.format(size))
        str = ""
        for i in range(size):
            str_temp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            #print(str_temp)
            hashtable.QuadraticHashInsert(Student(str_temp))
            str = str_temp
        start_time = time.time()
        print(hashtable.Retrieve(str))
        elapsed = time.time() - start_time
        times.append(elapsed)
        print("Time elapsed: ", time.time() - start_time)
    return times

def do_all(sizes_l, sizes_b, sizes_m):
    # CSLLF = do_CSLLF(sizes_l)
    # CSLL = do_CSLL(sizes_b)
    # CSAF = do_CSAF(sizes_l)
    CSA = do_CSA(sizes_b)
    ##Geometric:
    # SSLLF = do_SSLLF(sizes_l)
    # SSLL = do_SSLL(sizes_m)
    # SSAF = do_SSAF(sizes_l)
    SSA = do_SSA(sizes_m)
    # HTB = 0
    # HTBF = 0

    start_time = time.time()
    hashtable = HashTable(5)
    hashtable.QuadraticHashInsert(Student("Matas Minelga"))
    hashtable.QuadraticHashInsert(Student("Rokas"))
    hashtable.QuadraticHashInsert(Student("Paulius"))
    hashtable.QuadraticHashInsert(Student("Matas Minelga"))
    hashtable.QuadraticHashInsert(Student("Simas"))
    elapsed = time.time() - start_time
    HTB = elapsed

    start_time = time.time()
    hashtable = HashTable(5, True, "hashtabley")
    hashtable.QuadraticHashInsert(Student("Matas Minelga"))
    hashtable.QuadraticHashInsert(Student("Rokas"))
    hashtable.QuadraticHashInsert(Student("Paulius"))
    hashtable.QuadraticHashInsert(Student("Matas Minelga"))
    hashtable.QuadraticHashInsert(Student("Simas"))
    elapsed = time.time() - start_time
    HTBF = elapsed
    #print(hashtable)

    # plt.xlabel('Elementų skaičius, n')
    # plt.ylabel('Laikas, s')
    # plt.subplot(241) # pirmi du skaičiai yra XY, trečias indeksas
    # plt.plot(sizes_l, CSLLF, 'b-o')
    # plt.title('Counting Sort in Linked List in file')
    # plt.xlabel('Elementų skaičius, n')
    # plt.ylabel('Laikas, s')
    # plt.subplot(242)
    # plt.plot(sizes_l, CSAF, 'b-o')
    # plt.title("Counting Sort in Array in file")
    # plt.xlabel('Elementų skaičius, n')
    # plt.ylabel('Laikas, s')
    # plt.subplot(243)
    # plt.plot(sizes_b, CSLL, 'b-o')
    # plt.title('Counting Sort in Linked List in mem')
    # plt.xlabel('Elementų skaičius, n')
    # plt.ylabel('Laikas, s')
    # plt.subplot(244)
    # plt.plot(sizes_b, CSA, 'b-o')
    # plt.title("Counting Sort in Array in mem")
    # plt.xlabel('Elementų skaičius, n')
    # plt.ylabel('Laikas, s')
    # plt.subplot(245)
    # plt.plot(sizes_l, SSLLF, 'b-o')
    # plt.title('Selection Sort in Linked List in file')
    # plt.xlabel('Elementų skaičius, n')
    # plt.ylabel('Laikas, s')
    # plt.subplot(246)
    # plt.plot(sizes_l, SSAF, 'b-o')
    # plt.title("Selection Sort in Array in file")
    # plt.xlabel('Elementų skaičius, n')
    # plt.ylabel('Laikas, s')
    # plt.subplot(247)
    # plt.plot(sizes_m, SSLL, 'b-o')
    # plt.title('Selection Sort in Linked List in mem')
    # plt.xlabel('Elementų skaičius, n')
    # plt.ylabel('Laikas, s')
    # plt.subplot(248)
    # plt.plot(sizes_m, SSA, 'b-o')
    # plt.title("Selection Sort in Array in mem")
    #plt.plot( CSLLF, CSLL, CSAF, CSA, SSLLF, SSLL, SSAF, SSA)
    #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()

def retrieve_several(students, hashtable, partsize, part):
    start = int(len(students)*part/partsize)
    #print("st: ", start)
    end = int(len(students)*(part+1)/partsize)
    #print("end: ", end)
    for i in range(start, end):
        hashtable.Retrieve(students[i])

def do_parallel(students, hashtable, threads):
    start = time.time()
    jobs = []
    for i in range(0, threads):
        proc = multiprocessing.Process(target=retrieve_several, args=(students, hashtable, threads, i))
        proc.start()
        jobs.append(proc)
        processes.append(proc)
        # print(i)
        # hashtable.Retrieve(student)
    for job in jobs:
        job.join()
    print("Paraleliai užtruko: ", time.time() - start, "s.", " Su ", threads, " procesais")

if __name__ == "__main__":
    processes = []
    print("Creating hashtable")
    count = 20000
    hashtable = HashTable(count)
    students = []
    print("Inserting students")
    for i in range(count):
        str_temp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        student = Student(str_temp)
        students.append(str_temp)
        # students.append(student)
        hashtable.QuadraticHashInsert(student)
    start = time.time()
    print("Finding students")
    i = 0
    for student in students:
        hashtable.Retrieve(student)
        i+=1
        if(i%1000 == 1):
            print(i)

    print("Ne paraleliai užtruko: ", time.time() - start, "s.")
    start = time.time()
    threads = 6
    with Pool(threads) as pool:
        results = pool.map(hashtable.Retrieve, students)
    print("Paraleliai su ", threads, " threads užtruko: ", time.time() - start, "s.")
    print("Daroma su processes:")
    do_parallel(students, hashtable, threads)

    # for i in range(8, 9, 1):
    #     do_parallel(students, hashtable, i)
    # jobs = []
    # threads = 5
    # start = time.time()
    # for i in range(0, threads):
    #     proc = multiprocessing.Process(target=retrieve_several, args=(students, hashtable,threads,i))
    #     proc.start()
    #     jobs.append(proc)
    #     processes.append(proc)
    #     # print(i)
    #     # hashtable.Retrieve(student)
    # for job in jobs:
    #     job.join()
    # print("Paraleliai užtruko: ", time.time() - start, "s.", " Su ", threads, " procesais")
