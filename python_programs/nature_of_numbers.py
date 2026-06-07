# TO-DO import math

# TO-DO Determine if number is even or odd

# TO-DO Determine if number has perfect square root

# TO-DO Determine all factors of number
import math
import sys


def main():
    play_game = True

    while play_game:
        try:
            number = int(input("Enter a whole number (i.e., an integer): "))
        except ValueError:
            print('Please enter a valid integer.')
            continue
        except (EOFError, KeyboardInterrupt):
            print('\nInput cancelled. Exiting.')
            return

        print(f"\nThe number you entered is {number}.")

        # Check even, odd, or zero
        if number == 0:
            print("0 is an even number.")
        elif number % 2 == 0:
            print(f"{number} is an even number.")
        else:
            print(f"{number} is an odd number.")

        # Check for perfect square root
        if number >= 0:
            root = math.isqrt(number)
            if root * root == number:
                print(f"{number} has a perfect square root.")
            else:
                print(f"{number} does not have a perfect square root.")
        else:
            print(f"{number} does not have a real square root.")

        # Find all the factors of the number (use absolute value)
        n = abs(number)
        factors = []
        for i in range(1, n + 1):
            if n % i == 0:
                factors.append(i)

        print(f"The factors of {number} are {','.join(map(str, factors))}.")

        # Ask user if they want to continue
        try:
            again = input("\nWould you like to enter another number? (Y/N): ")
        except (EOFError, KeyboardInterrupt):
            print('\nInput cancelled. Exiting.')
            return
        if again.lower() != "y":
            play_game = False
            print("\nThank you for playing!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nExiting...')
        sys.exit(0)