# Turime skaičių seką susidedančia iš skaitmenų nuo 0 iki 9
# , surasti visas įmanomas skaičių kombinacijas, kurios dalinasi iš pasirinkto skaičiaus.
# Pvz. skaičių seka „676“, daliklis 6; Ats.: įmanomos skaičių kombinacijos, kurios dalinasi iš 6 : 6, 6, 66.


def divides(left_in_list, seq, answers, divider):

    if seq % divider == 0 and seq != 0:
        answers.append(seq)
    for x in left_in_list:
        ll = list(left_in_list)
        ll.remove(x)
        seq_n = seq*10 + x
        if len(ll) > 0:
            divides(ll, seq_n, answers, divider)


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

while True:
    main()