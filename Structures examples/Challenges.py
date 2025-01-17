#1 Check if a list its sorted
#Write a function that checks whether a given list of numbers is sorted in either ascending or descending order.

def is_sorted(lista):

    asc, desc = True, True

    for i in range(len(lista) - 1):
        if lista[i] > lista[i + 1]:
            asc = False

    for i in range(len(lista) - 1):
        if lista[i] < lista[i + 1]:
            desc = False

    return asc or desc

resultado = is_sorted([4, 5, 6, 7, 8])

print(resultado)


#2 Convert binary number to  decimal
#Write a function that converts a binary number to its decimal equivalent



#3
lista_integer = ["El", "casi", "sii"]

print(" ".join(lista_integer))


#5: Hide a Credit Card Number
#Write a function that takes a credit card number and transforms it into a string where all
#digits except the last four are replaced with asterisks.

def hide_credict_card(card_number):
    card = str(card_number)
    return "*"*(len(card) - 4) + card[-4:]

resultado = hide_credict_card(456798630883)
print(resultado)




#8: Is the Product Divisible by the Sum?



def prueb(numeros):
    if not numeros:
        return False

    produc = 1
    add = 0

    for num in numeros:
        produc *= num
        add += num

    if add == 0:
        return False

    return produc % add == 0


resultado = prueb([4, 4, 8])

print(resultado)


squares = [ x**2 for x in range(4)]

cub = [ x**3 for x in range(8)]

print(squares)

print(cub)

even_numbers = [x for x in range(7) if x % 2 == 0]

print(even_numbers)

odd_numbers = [x for x in range(7) if x % 2 != 0]

print(odd_numbers)

mylist= [4, 7, 9, 8, 10, 12, 16]


for num in mylist:
    if num % 2 == 0:
        print("Even",num)
        print("break")
        break

    else:
        print("Odd",num)

# Another way more readable and effective
par = [num for num in mylist if num % 2 == 0]
print(par)


mylist= [4, 7, 9, 8, 10, 12, 16]

for num in mylist:
    if num > 6:
        print(f"Eres mayor que seis:", num)

    else:
        print("break")


def even(real):
    for num in real:
        if num > 6:
            return f" Mayor que seis:", num


final = even([4, 7, 9, 8, 10, 12, 16])

print(final)






































































