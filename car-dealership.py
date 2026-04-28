import json

users_file = "users.json"
cars_file = "cars.json"

discounts = {
    "chevrolet": 0.25,
    "ford": 0.20,
}

#users JSON functions
def load_users():
    with open(users_file, "r") as file:
        return json.load(file)
    
def save_user(users):
    with open(users_file, "w") as file:
        json.dump(users, file, indent=4)

#cars JSON functions
def load_cars():
    with open(cars_file, "r") as file:
        return json.load(file)
    
def save_car(cars):
    with open(cars_file, "w") as file:
        json.dump(cars, file, indent=4)

#--------USER FUNCTIONS
def add_user(users):
    name = input("Enter with your name: ").strip()
    email = input("Enter with your email: ").strip()
    password = input("Enter with your password: ").strip()
    user_id = max([u["user_id"] for u in users], default=0) + 1
    
    for u in users:
        if u["email"] == email or u["password"] == password:
            print("Email or password already exists.")
            return None
    users.append({"user_id": user_id, 
                  "name": name, 
                  "email": email, 
                  "password": password, 
                  "balance": 0,
                  "owned_cars": [],
                  "is_admin": False
    })
    save_user(users)
    print(f"Your account was saved successfully, {name}!")

def login_user(users):
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    for user in users:
        if user["email"] == email and user["password"] == password:
            print(f'\nWelcome {user["name"]}! Take a look around and see if you like one of our cars.\n')
            return user
        
    print("\nInvalid user or password. Try again or create your account.")
    return None

def add_balance(users, current_user):
    if current_user is None:
        print("You need an account to access this.")
        return None

    try:
        amount = float(input("Put a value: ").strip())

        if amount <= 0:
            print("You have to put a positive value.")
            return current_user

        for u in users:
            if u["user_id"] == current_user["user_id"]:
                u["balance"] += amount
                current_user["balance"] = u["balance"]
                break
        save_user(users)
        print("Balance updated!")
        return current_user

    except ValueError:
        print("Invalid input. Please use numbers.")
        return current_user

#--------CAR FUNCTIONS
def show_cars(cars, current_user):
    if current_user is None:
        print("You need an account to access this.")
        return None

    if not cars:
        print("No cars available.\n")
        return
    else:
        for car in cars:
            print(f'{car["car_id"]}- Brand: {car["brand"]} | Name: {car["car_name"]} | Year: {car["car_year"]} | Price: ${car["price"]:.3f}')

def add_car(cars, current_user):
    if current_user is None or not current_user.get("is_admin", False):
        print("Access denied. Only admins can access.")
        return
    brand = input("Brand of the car: ").strip()
    car_name = input("Name of car: ").strip()
    car_year = int(input("Year: ").strip())
    price = float(input("Price of car: ").strip())
    car_id = max([car['car_id'] for car in cars], default=0) + 1
    cars.append({
        "car_id": car_id, 
        "brand": brand, 
        "car_name": car_name, 
        "car_year": car_year, 
        "price": price
    })
    save_car(cars)
    print(f'{car_name} added!')

def find_car(cars, car_id):
    for car in cars:
        if car["car_id"] == car_id:
            return car
    return None

def apply_discount(car):
    brand = car["brand"].lower()

    if brand in discounts:
        discount = discounts[brand]
        discounted_price = car["price"] * (1 - discount)
        return discounted_price, discount
    return car["price"], 0

def buy_car(users, cars, current_user):
    purchase = []
    total = 0

    if current_user is None:
        print("You need an account to access this.")
        return None
    
    while True:
        choice = input("Choose the car you want by the ID or press L to leave: ").strip().lower()
        if choice == "l":
            break
        try:
            car_id = int(choice)
            car = find_car(cars, car_id)

            if car is None:
                print("Car not found.")
                continue

            purchase.append(car)
            final_price, discount = apply_discount(car)
            total += final_price
            
            if discount > 0:
                print(f'\n{car["car_name"]} added for {car["price"]:.3f}. A special discount for {car["brand"]} cars has been applied.')
            else:
                print(f'\n{car["car_name"]} added for {car["price"]:.3f}!')

        except ValueError:
            print("Invalid input.")

        if not purchase:
            print("No car selected.")
            return current_user
        
        print(f'Total price is: ${total:.3f}')
        print(f'Your current balance is: ${current_user["balance"]:.3f}')

        #check if the user has enough balance to buy the chosen car.
        if current_user["balance"] < total:
            print("You don't have enough money.")
            return current_user
        
        confirm = input("\nAre you sure you want to buy this car? (Y/N): ").strip().lower()
        if confirm == "n":
            print("Purchase cancelled.")
            return current_user
        elif confirm == "y":
            for u in users:
                if u["user_id"] == current_user["user_id"]:
                    u["owned_cars"].extend([{
                        "brand": car["brand"],
                        "car_name": car["car_name"],
                        "car_year": car["car_year"],
                        "price": final_price,
                    } 
                    for car in purchase])
                    u["balance"] -= total
                    current_user["balance"] = u["balance"]
                    break
            save_user(users)
            print(f'\nPurchase completed. Congratulations, you bought {car["car_name"]}!')
            return current_user
        else:
            print("Wrong input.")
            continue

def main():
    users = load_users()
    cars = load_cars()
    current_user = None

    while True:
        if current_user is None:
            print("\n---Welcome to our car dealership! Please feel free to choose any option below.---")
            print("1. Create an account")
            print("2. Enter with your account")
            print("3. Leave")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                add_user(users)
            elif choice == "2":
                current_user = login_user(users)
            elif choice == "3":
                print("Have a good day!")
                break
            else:
                print("Invalid choice. Try again.")
        
        else:
            print("\n---Options---")
            print("1. View cars available")
            if current_user.get("is_admin", False):
                print("2. Add car(Only admins)")
            print("3. Buy car")
            print("4. Add money")
            print("5. Logout")

            choice = input("Choose the option you want: ").strip()

            if choice == "1":
                print("\n---Cars available---")
                show_cars(cars, current_user)
            elif choice == "2":
                add_car(cars, current_user)
            elif choice == "3":
                buy_car(users, cars, current_user)
            elif choice == "4":
                add_balance(users, current_user)
            elif choice == "5":
                print("Have a nice day!")
                current_user = None
                continue
main()