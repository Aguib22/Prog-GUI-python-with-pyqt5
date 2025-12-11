"""
val = input("Saisir un nombre : ")

n = int(val)
if(n > 1):
    max = n
    count = 1
 
    while (n > 1):
        if (n % 2 == 0):
            n = n / 2
        else:
            n = 3 * n + 1
        count = count + 1
   
        if (n > max):
            max = n
        print(n)
    print("nombre de termes dans la suite :" + str(count))
    print("valeur max de la suite :" + str(max))
"""
def GenerateSyracuseSequence(val):
    n = int(val)
    sequence = [n]
    if n  >1:
        max = n
        count = 1
        while n > 1:
            if n % 2 == 0:
                n = n // 2
            else:
                n = 3 * n + 1
            count += 1
            if n > max:
                max = n
            sequence.append(n)
    return sequence, count, max


if __name__ == "__main__":
    val = input("Saisir un nombre : ")
   
    values,count, max = GenerateSyracuseSequence(val)
    print("Suite de Syracuse :", values)
    print(f"Nombre de termes dans la suite :{count}")
    print(f"Valeur max de la suite :{max}")