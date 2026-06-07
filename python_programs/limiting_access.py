import math
import os
import sys


def load_users():
	users = []
	base = os.path.dirname(os.path.abspath(__file__))
	path = os.path.join(base, 'authorized_users.txt')
	if os.path.exists(path):
		try:
			with open(path, 'r', encoding='utf-8') as f:
				for d in f:
					tmp = d.strip().split(',')
					if len(tmp) != 3:
						continue
					users.append({'username': tmp[0], 'pass': tmp[1], 'level': int(tmp[2])})
		except Exception:
			pass

	# default demo user if file missing
	if not users:
		users = [{'username': 'demo', 'pass': 'demo', 'level': 1}]
	return users


def fertilizer_calculator():
	print('Welcome to the Fertilizer Calculator! I will ask you for the length and width of four rectangular sections. Please enter your measurements in feet (numbers only, please). If you do not have a particular section, simply enter zero (0) for those dimensions!\n')

	def get_dimension(section_name):
		while True:
			try:
				length = float(input(f"What is the length of the {section_name} section? "))
				width = float(input(f"What is the width of the {section_name} section? "))
				return length, width
			except ValueError:
				print('Please enter numeric values for length and width.')
			except (EOFError, KeyboardInterrupt):
				raise

	sections = ['front', 'rear', 'left', 'right']
	areas = []
	for section in sections:
		length, width = get_dimension(section)
		area = length * width
		areas.append(area)

	total_area = int(sum(areas))

	# Fertilizer calculations
	COVERAGE_PER_BAG = 2000
	COST_PER_BAG = 27
	NITROGEN_PER_BAG = 1.0
	POTASSIUM_PER_BAG = 0.125
	SQFT_PER_HOUR = 2500
	LABOR_COST_PER_HOUR = 20

	bags_needed = math.ceil(total_area / COVERAGE_PER_BAG) if total_area > 0 else 0
	cost_fertilizer = bags_needed * COST_PER_BAG
	hours_needed = math.ceil(total_area / SQFT_PER_HOUR) if total_area > 0 else 0
	cost_labor = hours_needed * LABOR_COST_PER_HOUR
	total_cost = cost_fertilizer + cost_labor

	nitrogen_applied = bags_needed * NITROGEN_PER_BAG
	potassium_applied = bags_needed * POTASSIUM_PER_BAG

	print(f"Total area: {total_area} sq. feet\n")
	print(f"Cost of fertilizer: ${cost_fertilizer:.2f}\n")
	print(f"Bags of fertilizer required: {bags_needed}\n")
	print(f"Minimum hours required: {hours_needed}\n")
	print(f"Cost of labor: ${cost_labor:.2f}\n")
	print(f"Total cost: ${total_cost:.2f}\n")
	print(f"Nitrogen applied to soil: {nitrogen_applied:.3f} pounds\n")
	print(f"Potassium applied to soil: {potassium_applied:.3f} pounds")


def main():
	users = load_users()
	try:
		input_username = input("Please enter your username: ")
		input_password = input("Please enter your password: ")
	except (EOFError, KeyboardInterrupt):
		print('\nInput cancelled. Exiting.')
		return

	authorized = False
	for user in users:
		if input_username == user['username'] and input_password == user['pass']:
			authorized = True
			break

	if authorized:
		try:
			fertilizer_calculator()
		except (EOFError, KeyboardInterrupt):
			print('\nInput cancelled. Exiting.')
	else:
		print("You have entered invalid credentials, please find your password and start over")


if __name__ == '__main__':
	main()