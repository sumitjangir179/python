age = 17

# syntax: if condition/expression/statement: need to be true or false to be executed
# if age >= 18:
    # print("You are an adult.")

# shorthand if
# if age >= 18: print("You are an adult.")


# if-else statement
if age >= 18:
    print("You are an adult.")
else:
    print("You are not an adult.")

# if-elif-else statement
if age < 13:
    print("You are a child.")
elif age < 18:
    print("You are a teenager.")
else:
    print("You are an adult.")


# nested if-else
age = 70
is_member = True

if age >= 60:
    if is_member:
        print("30% senior discount!")
    else:
        print("20% senior discount.")
else:
    print("Not eligible for a senior discount.")

# shorthand if-else
print("You are an adult." if age >= 18 else "You are not an adult.")


def check_number(x):
    match x:
        case 10:
            print("It's 10")
        case 20:
            print("It's 20")
        case _:
            print("It's neither 10 nor 20")

check_number(10)
check_number(30)