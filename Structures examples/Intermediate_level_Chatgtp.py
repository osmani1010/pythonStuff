#1.String Manipulation
#Write a program to count the number of vowels in a string.


string_one = (input("Please write something:" ))

count_vowels = 0

vowels = "aeiouAEIOU"

for char in string_one:

    if char.isalpha() and char in vowels:

        count_vowels += 1

print(f"The number of vowels in the string is: {count_vowels}")


#Write a program to count the number of consonants in a string.

string_one = (input("Please write something:" ))

counter_consonants = 0

vowels = "aeiouAEIOU"

for char in string_one:
    if char.isalpha() and char not in vowels:

        counter_consonants += 1

print(f"The number of consonants is {counter_consonants}")


#Count the numbers of words in the string
string_one = str(input("Please write something:" ))

voc = string_one.split()

print(len(voc))

#Create a program to check if a string is a palindrome.

stringg = input("Please enter a string:"  )

if stringg == stringg[::-1]:
    print("The string is a palindrome")
else:
    print("No lo es")



def is_palindrome(string):
# Normalize the string: Remove non-alphanumeric characters and convert to lowercase
    normalized_string = "".join(char.lower() for char in string if char.isalnum())

    return normalized_string == normalized_string[::-1]

user_input = input("Please write a string: ")

if is_palindrome(user_input):
    print("Its palindrome")

else:
    print("Its not palindrome")


#Example with "".join(char.lower() for char in valor if char.isalnum())
valor = input("Please enter a sentence:" )

valor_normalizado = "".join(char.lower() for char in valor if char.isalnum())

print (valor_normalizado)


#2.Functions

#Write a program to create a function that calculates the area of a circle given its radius.

def area_circle(radio):
    area = 3.1416 * (radio**2)
   return float(area)

valor_radio = float(input("Enter the radio: "))

if valor_radio < 0:
    print("Its not allowed negative values")

else:
    resultado = area_circle(valor_radio)
    print(f"The area of the circle is {resultado:.2f} m**2.")


#Another way using modulo math

from math import pi

def area_circulo(rad):

    if rad < 0:
        raise ValueError("Radio can not be negative")

    return pi * rad**2

try:
    value_radio = float(input("Enter the radio:" ))

    result = area_circulo(value_radio)
    print(f"El area del circulo con {value_radio} es {result:.2f} m**2")

except ValueError as e:
    print(f"Error: {e} ")



#Implement a function to check if a number is prime.
#a prime number is only divisible by 1 and the number itself without leaving a remainder.

def is_prime(number):

    if number <= 1:
        return False

    for i in range(2, int(number ** 0.5) + 1):

        if number % i == 0:

            return False

    return True

valor = int(input("Enter the number:"  ))

if is_prime(valor):
    print("Es primo")

else:
    print("No primo")


#3.File Handling
#Write a Python script to read a text file and count the number of lines, words, and characters.

def read_file(path_file):

    try:

        with open(path_file, "r") as file:

            lines = file.readlines()

            number_lines = len(lines)

            count_words = 0
            count_characters = 0

            for line in lines:

                count_words += (len(line.split()))

                count_characters += (len(line))

            print(f"The number of lines is: {number_lines} ")
            print(f"The number of words is: {count_words} ")
            print(f"The number of characters is: {count_characters} ")

    except FileNotFoundError:
        print(f"Error: The file ¨{path_file}¨ does not exist")

    except IOError as e:
        print(f"Error reading the file: {e} ")

path_file = input("Enter the file to read:" )

read_file(path_file)


#Create a program to write a list of numbers to a file and read them back.

def write_numbers_to_file(numbers, path_file):

    try:

        with open(path_file, "w") as file:

            for number in numbers:
                file.write(f"{number} \n")

        print(f"Numbers written in {path_file} ")


    except IOError as e:
        print(f"Error writing to file: {e}")

entrada = [2, 4, 7, 8, 9, 47, 200]

write_numbers_to_file(entrada, "ForPython.txt")


def read_back_number(path_file):

    try:

        with open(path_file, "r") as file:

            numbers = [int(line.strip()) for line in file]

        print(f"Numbers read from {path_file} are: {numbers}")

    except FileNotFoundError:
       print(f"Error: The {path_file} does not exist")

        return[]

    except ValueError as e:
        print(f"Error reading number from file: {e} ")

        return[]

read_back_number("ForPython.txt")


#4.Dictionaries
#Write a program to count the frequency of elements in a list using a dictionary.

def elements_list(key):

    frecuencia = {}

    for char in key:

        frecuencia[char] = frecuencia.get(char, 0) + 1

    return frecuencia  # funskjonen må returneres

    print(f"The frecuencia es: {frecuencia}")

entrada = list(map(int, input( "Please enter the numbers separates by space:  ").split()))

#lista = [3, 6, 7, 8, 8]
#lista = "Es de verdad muy complicado hoy"
result = elements_list(entrada)

print("The frecuencia of elements is:", result)







