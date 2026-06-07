import math


print('Welcome to the Fertilizer Calculator! I will ask you for the length and width of four rectangular sections. Please enter your measurements in feet (numbers only, please). If you do not have a particular section, simply enter zero (0) for those dimensions!\n')

def get_dimension(section_name):
	length = float(input(f"What is the length of the {section_name} section? "))
	width = float(input(f"What is the width of the {section_name} section? "))
	return length, width

sections = ['front', 'rear', 'left', 'right']
areas = []
for section in sections:
	length, width = get_dimension(section)
	area = length * width
	areas.append(area)

total_area = int(sum(areas))

# Fertilizer calculations
import math
import sys


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


def main():
	print('Welcome to the Fertilizer Calculator! I will ask you for the length and width of four rectangular sections. Please enter your measurements in feet (numbers only, please). If you do not have a particular section, simply enter zero (0) for those dimensions!\n')

	sections = ['front', 'rear', 'left', 'right']
	areas = []
	for section in sections:
		try:
			length, width = get_dimension(section)
		except (EOFError, KeyboardInterrupt):
			print('\nInput cancelled. Exiting.')
			return
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


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('\nExiting...')
		sys.exit(0)


