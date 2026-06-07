import sys
import math


def main():
    try:
        radius = float(input("What is the radius of the circle? "))
    except (ValueError, EOFError, KeyboardInterrupt):
        print('\nInvalid input or input cancelled. Exiting.')
        sys.exit(0)

    diameter = 2 * radius
    circumference = 2 * math.pi * radius
    area = math.pi * (radius ** 2)

    print(f"A circle with a radius of {radius} units will have a diameter of {diameter} units, "
          f"a circumference of {circumference} units, and an area of {area} square units.")


if __name__ == '__main__':
    main()
