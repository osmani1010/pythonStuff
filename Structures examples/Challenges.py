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






















































