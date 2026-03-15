import csv
import datetime
import os
import subprocess


today = datetime.datetime.today()
day_of_month = today.day  
theme_song = "theme.mp3"
nami = "nami.mp3"
bye = "bye.mp3"
budget_targets = {
    "rent": 374,
    "electricity": 20,
    "laundry": 20,
    "groceries_week1": 20,
    "groceries_week2": 20,
    "groceries_week3": 20,
    "groceries_week4": 20,
    "stationary": 6 
}

total = sum(budget_targets.values())
csv_file = 'budget.csv'
csv_header = ["date", "category", "amount"]

def check_balance():
    try: 
        spent_total = 0
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                amount = int(row[2])
                spent_total += amount
        balance = total - spent_total
        return balance
    except FileNotFoundError:
        return total

def read_csv():
    try:
        spent_by_category = {}
        spent_total = 0
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                category = row[1].lower()
                amount = int(row[2])
                spent_total += amount
                spent_by_category[category] = spent_by_category.get(category, 0) + amount

        balance = total - spent_total
        print(f"\n💰 Total remaining berries: {balance}")
        if balance < 30:
            print("⚠️ Nami is glaring at you! Your treasure is almost gone… hurry or face her wrath! ⚡")
            subprocess.run(["afplay", nami])

        print("\n📊 Per-category spending:")
        for category, target in budget_targets.items():
            spent = spent_by_category.get(category, 0)
            remaining = target - spent
            print(f"{category}: spent {spent} / target {target}", end='')
            if remaining < 0:
                print(" ⚠️ Woah! You’ve gone overboard here! Zoro would be proud… or angry!")
            else:
                print(f" | remaining: {remaining}")

        return balance
    except FileNotFoundError:
        print("😱 Budget file does not exist yet… let’s create our treasure map!")
        return total

def write_csv():
    print("\n📝 Time to log a new expense, Captain!")
    
    while True:
        date = input("Date (YYYY-MM-DD): ")
        try:
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("❌ That’s not a valid date! Even Usopp couldn’t lie about this one…")

    while True:
        print("\nSelect a category for your treasure spending:")
        for i, category in enumerate(budget_targets.keys(), 1):
            print(f"{i}. {category}")

        cat_choice = input("Enter the category number: ")
        if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(budget_targets):
            category = list(budget_targets.keys())[int(cat_choice) - 1]

            spent_in_category = 0
            if os.path.isfile(csv_file):
                with open(csv_file, 'r') as file:
                    reader = csv.reader(file)
                    next(reader, None)
                    for row in reader:
                        if row[1].lower() == category:
                            spent_in_category += int(row[2])

            remaining_budget = budget_targets[category] - spent_in_category
            if remaining_budget <= 0:
                print(f"⚠️ {category} treasure chest is empty! Even Luffy can’t stretch it more! 🍖")
                continue

            break
        else:
            print("🚫 Invalid choice, Captain! Try again.")

    print(f"Remaining budget for {category}: {remaining_budget}")

    while True:
        amount = input("Amount spent: ")
        if amount.isdigit():
            amount = int(amount)
            if amount <= remaining_budget:
                break
            else:
                print(f"⚠️ You can’t spend more than {remaining_budget} berries here! Even Sanji won’t cook for free!")
        else:
            print("❌ Enter a valid number, Captain!")

    file_exists = os.path.isfile(csv_file)
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(csv_header)
        writer.writerow([date, category, amount])

    print(f"🏴‍☠️ Recorded {amount} berries in {category}! Onward to more treasure!")

def main():
    print("🏴‍☠️ Welcome aboard, Captain! Your treasure awaits…")
    subprocess.run(["afplay", theme_song])
    balance = check_balance()
    if balance is None:
        balance = total
    if 10 <= day_of_month <= 20 and balance < 30:
        print("⚠️ Mid-month alert! Nami is shouting: 'Save your berries or you’ll regret it!'")

    while True:
        print("\n1. Record an expense")
        print("2. Check balance")
        print("3. Quit")

        choice = input("Choose an option: ")
        if choice == '1':
            write_csv()
        elif choice == '2':
            read_csv()
        elif choice == '3':
            print("🌊 Fair winds, Captain! Until the next adventure!")
            subprocess.run(["afplay", bye])
            break
        else:
            print("❌ Invalid choice, try again, Captain!")

if __name__ == "__main__":
    main()