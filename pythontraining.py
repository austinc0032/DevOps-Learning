# Python Training Script
# Start with basic concepts for DevOps automation

# 1. Hello World - Basic output
print("Hello, DevOps World!")

# 2. Variables and data types
name = "Austin"
age = 27  # Update with your age
print(f"My name is {name} and I'm {age} years old.")

message = "One of Python's strengths is its diverse community."
print(message)

first_name = "Austin"
last_name = "Campbell"
full_name = f"{first_name} {last_name}"
print(f"My full name is {full_name}.")

message = "Hello Python World!"
print(message)

message = "Hello Python Crash Course world!"
print(message)

# 3. Lists
bicycles = ['trek', 'cannondale', 'redline', 'specialized']
message = f"My first buicycle was a {bicycles[0].title()}."
print(message)

cars = ['bmw', 'audi', 'toyota', 'subaru']
print(cars)

cars.reverse()
print(cars)

motorcycles = ['honda', 'yamaha', 'suzuki', 'ducati']
print(motorcycles)

too_expensive = 'ducati'
motorcycles.remove(too_expensive)
print(motorcycles)
print(f"\nA {too_expensive.title()} is too expensive for me.")

a = int(input("Enter the first number: "))
b = int(input("Enter the second number: "))
def add_numbers(a, b):
    return a + b

# Write a function that checks if a number is prime.
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Write a prgram that converts a Roman numeral to an integer.
def roman_to_int(s):
    roman_numerals = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    total = 0
    prev_value = 0

    for char in s:
        value = roman_numerals[char]
        if prev_value < value:
            total += value - 2 * prev_value
        else:
            total += value
        prev_value = value

    return total