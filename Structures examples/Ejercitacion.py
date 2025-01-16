from operator import length_hint

numeros = [2, 5, 6, 6, 7, 9, 0]
print(numeros)

numeros.sort()
print(numeros)

numeros.insert(2, 15)

print(numeros)

pila = []
pila.append("a")
pila.append("b")

print(pila)

from collections import deque

cola = deque()  # Crear una cola

# Operaciones
cola.append("A")  # Enqueue
cola.append("B")
cola.append("C")
print("Cola después de agregar elementos:", cola)

cola.popleft()  # Dequeue (elimina el primer elemento)
print("Cola después de eliminar el primer elemento:", cola)
print()

def miprimera():
    print("Its ok")

miprimera()

def miprimera(calor, frio):
    print(f"El {calor} esta {frio}")

miprimera("Julio", "December")

def total_calc(bill_amount, tip_percentaje=10):
    total = bill_amount * (1 + tip_percentaje*0.01)
    total = round(total,2)
    print(f"Please pay {total}")
total_calc(150)

total_calc(200, 20)

def volume_cube(lenght, width, hight):
    return lenght * width * hight

volume = volume_cube(4, 6, 3)
print(f"Volumen of the cube is {volume}")

def cube(side):
    volume = side **3
    surface = 6 *(side**2)
    return volume, surface
value = cube(8)
print(value)


# First Class Function " Using closures\cierres with parameters"

def outer_scope(name, city):

    def inner_scope():
        print(f"Hello {name}, Greetings from {city}")

    return inner_scope

# Creatings closures with differents name and locations

greet_Jorge = outer_scope("Jorge", "Norway")
greet_Osmani = outer_scope("Osmani", "Switzerland")

greet_Jorge()
greet_Osmani()



