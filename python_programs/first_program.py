# first_program.py
import sys

def main():
	try:
		print("Hello! What is your name?")
		name = input()
		print(f"Hello, {name}! Nice to meet you! What city were you born in?")
		city = input()
		message = f"{city} is a nice city! I wouldn't mind living there!"
		print(message)
	except (EOFError, KeyboardInterrupt):
		print('\nInput cancelled. Exiting.')
		sys.exit(0)


if __name__ == '__main__':
	main()
