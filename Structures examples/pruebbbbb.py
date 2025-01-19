def check_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative.")

    print(f"Age is valid: {age}")


de = int(input("Enter num:" ))

check_age(de)