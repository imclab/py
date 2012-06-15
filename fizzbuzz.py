def print_fizz_buzz(num):
    to_print = ""
    if num % 3 == 0:
        to_print += "Fizz"
    if num % 5 == 0:
        to_print += "Buzz"
    if num % 3 != 0 and num % 5 != 0:
        to_print += str(num)
    print to_print

if __name__ == "__main__":
    map( print_fizz_buzz, range(101) )