#Basic Syntax and Printing
#Write a program to take user input (name) and print a greeting.
#name = input("What ist your name:"  )
from audioop import reverse

#print("Greeting", name)


#Data Types
#1.Create a program that takes two integers as input and outputs their sum.
#numero_one = int(input("Please enter the number:"  ))

#numero_dos = int(input("Please enter the number:"  ))

#suma = numero_one + numero_dos
#print("La sumatoria es:", suma)

#2.Write a program to swap two numbers without using a third variable.

   # numero_one = int(input("Please enter the number:"  ))

    #numero_dos = int(input("Please enter the number:"  ))

    #numero_one = numero_one + numero_dos
    #numero_dos = numero_one - numero_dos
    #numero_one = numero_one - numero_dos

    #print("After swaping:")
    #print("Number one:", numero_one )
    #print("Number dos:", numero_dos )

#3.Conditional Statements
#Write a program to check if a number is even or odd.

    #number = int(input("Please enter a number:"  ))

    #if number % 2 == 0:
        #print("Even")
    #else:
        #print("Odd")


#4.Create a program to find the largest of three numbers.

#numero_uno = float(input("Please enter a number:"  ))
#numero_dos = float(input("Please enter a number:"  ))
#numero_tres = float(input("Please enter a number:"  ))

#if numero_uno >= numero_dos and numero_uno >= numero_tres:
 #   print("The largest is:", numero_uno)

#elif numero_dos >= numero_uno and numero_dos >= numero_tres:
 #   print("The largest is:", numero_dos)

#else:
  #  print("The largest is:", numero_tres)

#4.Loops
#Write a program to print numbers from 1 to 10.

#for i in range(1, 11):
    #print(i)

#Create a program to calculate the factorial of a number using a for loop.

#number = int(input("Please enter a non negative integer:"  ))

#factorial = 1

#if number < 0:
    #print("Factorial is not defined for negative integer")

#elif number == 0:
    #print("Factorial the zero is one by definition")

#else:
   # for i in range(1, number + 1):
        #factorial *= i

    #print(f"The factorial of {number} is {factorial} ")


#5.List
#Write a program to find the largest element in a list.

#number_lista = list(map(int, input("Please enter numbers separated by space:"  ).split()))

#if not number_lista:
    #print("The list is empty")

#else:

    #largest = number_lista[0]

    #for i in number_lista:
       # if i > largest:
            #largest = i


   # print("Mayor numero es:", i)


#Implement a program to reverse a list without using the reverse() method.

#lista = list(map(int, input("Please enter number separated by space: ").split()))

#if not lista:
    #print("Please enter the numbers")

#else:
    #revirada = []

    #for i in range(len(lista) - 1, -1, -1):
        #revirada.append(lista[i])

    #print("The reverse list is:", revirada)

#listaa = [200, 76, 65, 43, 20]

#listaa.reverse()
#print(listaa)








