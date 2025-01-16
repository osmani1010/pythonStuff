# ==========================================
# 1. Listas (Arrays)
# ==========================================
print("EJEMPLO: Listas")
lista = [3, 1, 4, 1, 5, 9]  # Crear una lista
print("Lista original:", lista)

lista.append(2)  # Agregar un elemento
print("Después de agregar 2:", lista)

lista.remove(1)  # Eliminar el primer 1 encontrado
print("Después de eliminar el primer 1:", lista)

# Algoritmo: Búsqueda lineal
def busqueda_lineal(lista, objetivo):
    for i, valor in enumerate(lista):
        if valor == objetivo:
            return f"Elemento {objetivo} encontrado en el índice {i}"
    return f"Elemento {objetivo} no encontrado"

print(busqueda_lineal(lista, 5))  # Buscar el número 5
print()

# ==========================================
# 2. Pilas (Stacks)
# ==========================================
print("EJEMPLO: Pilas (Stack)")
pila = []  # Crear una pila

# Operaciones
pila.append(1)  # Push
pila.append(2)
pila.append(3)
print("Pila después de agregar elementos:", pila)

pila.pop()  # Pop (elimina el último elemento)
print("Pila después de eliminar el último elemento:", pila)

print()

# ==========================================
# 3. Colas (Queues)
# ==========================================
print("EJEMPLO: Colas (Queue)")
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

# ==========================================
# 4. Conjuntos (Sets)
# ==========================================
print("EJEMPLO: Conjuntos (Set)")
conjunto = {1, 2, 3, 4}  # Crear un conjunto
print("Conjunto original:", conjunto)

conjunto.add(5)  # Agregar un elemento
print("Después de agregar 5:", conjunto)

conjunto.remove(2)  # Eliminar un elemento
print("Después de eliminar 2:", conjunto)

# Algoritmo: Verificar si un elemento está en el conjunto
print("¿3 está en el conjunto?", 3 in conjunto)
print()

# ==========================================
# 5. Diccionarios (Maps/Hash Tables)
# ==========================================
print("EJEMPLO: Diccionarios")
diccionario = {"a": 1, "b": 2, "c": 3}  # Crear un diccionario
print("Diccionario original:", diccionario)

diccionario["d"] = 4  # Agregar una nueva clave-valor
print("Después de agregar 'd':", diccionario)

del diccionario["b"]  # Eliminar una clave
print("Después de eliminar 'b':", diccionario)

# Algoritmo: Búsqueda en un diccionario
clave = "c"
print(f"¿'{clave}' está en el diccionario?", clave in diccionario)
print()

# ==========================================
# 6. Algoritmo: Ordenamiento (Bubble Sort)
# ==========================================
print("EJEMPLO: Algoritmo Bubble Sort")
def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        print("Iteracion i", [i])
        print(lista)
        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:  # Intercambiar si el elemento actual es mayor que el siguiente
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                print("Iteracion j", [j])
                print(lista)
    return lista

desordenada = [64, 34, 25, 12, 22, 11, 90]
print("Lista desordenada:", desordenada)
ordenada = bubble_sort(desordenada)
print("Lista ordenada:", ordenada)
print()

# ==========================================
# 7. Algoritmo: Búsqueda binaria (Binary Search)
# ==========================================
print("EJEMPLO: Algoritmo Búsqueda Binaria")
def busqueda_binaria(lista, objetivo):
    izquierda, derecha = 0, len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if lista[medio] == objetivo:
            return f"Elemento {objetivo} encontrado en el índice {medio}"
        elif lista[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return f"Elemento {objetivo} no encontrado"

print(busqueda_binaria(ordenada, 25))  # Buscar 25 en la lista ordenada
print(busqueda_binaria(ordenada, 100))  # Buscar 100 (no está en la lista)



