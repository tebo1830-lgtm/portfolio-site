# TO-DO Calculate gross pay
wage = float(input("What is your hourly wage? "))
hours = float(input("How many hours did you work? "))
gross = wage * hours
print(f"Gross Pay: ${gross:.2f} ({hours} hours @ ${wage:.2f}/hr)")
# TO-DO Calculate withholding
federal = gross * 0.10
state = gross * 0.05
social = gross * 0.062

print(f"Federal tax: ${federal:.2f}")
print(f"State tax: ${state:.2f}")
print(f"Social security: ${social:.2f}")
# TO-DO Calculate net pay
net = gross - (federal + state + social)
print(f"Net pay: ${net:.2f}")
# TO-DO Create your menu and program
def main():
    transactions = []

    while True:
        print("\n1-Calculate net pay")
        print("2-Enter revenue or expense")
        print("3-Show discretionary income")
        print("4-Exit")
        choice = input("Choice: ")

        if choice == "1":
            # Net pay calculation
            wage = float(input("What is your hourly wage? "))
            hours = float(input("How many hours did you work? "))
            gross = wage * hours
            federal = gross * 0.10
            state = gross * 0.05
            social = gross * 0.062
            net = gross - (federal + state + social)

            print(f"\nGross Pay: ${gross:.2f} ({hours} hours @ ${wage:.2f}/hr)")
            print(f"Federal tax: ${federal:.2f}")
            print(f"State tax: ${state:.2f}")
            print(f"Social security: ${social:.2f}")
            print(f"Net pay: ${net:.2f}")

        elif choice == "2":
            # Enter transactions
            while True:
                name = input("Enter transaction name: ")
                amount = float(input("Enter amount (use negative sign for expense): "))
                transactions.append((name, amount))
                another = input("Another? (Y/N): ").lower()
                if another != "y":
                    break

        elif choice == "3":
            # Show discretionary income
            revenue = sum(a for _, a in transactions if a > 0)
            expenses = sum(a for _, a in transactions if a < 0)
            discretionary = revenue + expenses
            print(f"\nRevenue: ${revenue:.2f} Expenses: ${expenses:.2f} Discretionary: ${discretionary:.2f}")

        elif choice == "4":
            print("Thanks for using My Finance!")
            break

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()