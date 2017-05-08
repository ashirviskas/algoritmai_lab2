# Turime skaičių seką susidedančia iš skaitmenų nuo 0 iki 9
# , surasti visas įmanomas skaičių kombinacijas, kurios dalinasi iš pasirinkto skaičiaus.
# Pvz. skaičių seka „676“, daliklis 6; Ats.: įmanomos skaičių kombinacijos, kurios dalinasi iš 6 : 6, 6, 66.
import plotly as py
import plotly.graph_objs as go
import time
from random import randint

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def divides(left_in_list, seq, answers, divider):
    if seq % divider == 0 and seq != 0:
        answers.append(seq)
    for x in left_in_list:
        ll = list(left_in_list)
        ll.remove(x)
        seq_n = seq*10 + x
        if len(ll) > 0:
            divides(ll, seq_n, answers, divider)

def divides_alternative(list, seq, current, divider, answers):
    if seq % divider == 0 and seq != 0:
        answers.append(seq)
    seq_a = seq*10+list[current]
    if (current+1) >= len(list):
        return
    divides_alternative(list, seq_a, current+1, divider, answers)
    divides_alternative(list, seq, current+1, divider, answers)


def divides_alternative_optimised(list, seq, current, divider, answers, added = True):
    if seq % divider == 0 and seq != 0 and not added:
        answers.append(seq)
    seq_a = seq*10+list[current]
    if (current+1) >= len(list):
        return
    divides_alternative_optimised(list, seq_a, current+1, divider, answers)
    divides_alternative_optimised(list, seq, current+1, divider, answers, False)



def printing(answers):
   print(str(answers)[1:-1], sep=", ", end=".\n")


def main():
    sequence = input("Įveskite norimą seką: ")
    divider = int(input("Įveskite norimą daliklį: "))
    list_sequence = []
    answers = []
    for letter in str(sequence):
        list_sequence.append(int(letter))
    divides(list_sequence, 0, answers, divider)
    printing(answers)


def graphing(max_length, increase):
    go_on = True
    do_printing = False
    length_of_seq = 1
    times = []
    lengths = []
    while(go_on):
        answers = []
        seka0 = str(random_with_N_digits(length_of_seq))
        seka = []
        for letter in seka0:
            seka.append(int(letter))
        daliklis = randint(1, 10)
        t0 = time.clock()
        #divides(seka, 0, answers, daliklis)
        divides_alternative_optimised(seka, 0, 0, daliklis, answers)
        t1 = time.clock()
        times.append(t1-t0)
        lengths.append(length_of_seq)
        length_of_seq = length_of_seq + increase
        if length_of_seq > max_length:
            go_on = False

        if do_printing:
            print("seka: ", seka0)
            print('Daliklis: ', daliklis)
            print("Atsakymai: ")
            printing(answers)
    trace = go.Scatter(
        x = lengths,
        y = times,
        mode='lines',
        name='Greitis'
    )
    data = [trace]
    py.offline.plot(data, filename='alternative')

graphing(20, 1)