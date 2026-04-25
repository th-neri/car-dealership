import json

users_file = "users.json"
cars_file = "cars.json"

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

def add_user(users):
    name = input("Enter with your name: ").strip()
    email = input("Enter with your email: ").strip()
    password = input("Enter with your password: ").strip()
    user_id = max([u["user_id"] for u in users], default=0) + 1
    users.append({"user_id": user_id, "name": name, "email": email, "password": password, "car_bought": None})
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

#cars functions
def show_cars(cars):
    if not cars:
        print("No cars available.\n")
        return
    else:
        for car in cars:
            print(f'{car['car_id']}- Brand: {car['brand']} | Name: {car['car_name']} | Year: {car['car_year']} | Price: {car['price']:.3f}')

def add_car(cars):
    brand = input("Write the brand of car: ").strip()
    car_name = input("Write the name of car: ").strip()
    car_year = int(input("Write the year of car: ").strip())
    price = float(input("Write the price of car: ").strip())
    car_id = max([car['car_id'] for car in cars], default=0) + 1
    cars.append({"car_id": car_id, "brand": brand, "car_name": car_name, "car_year": car_year, "price": price})
    save_car(cars)
    print(f'{car_name} saved successfully!')

def main():
    users = load_users()
    current_user = None

    while True:
        if current_user is None:
            print("\n---Welcome to our car dealership! Please feel free to choose any option below.---")
            print("1. Create an account.")
            print("2. Enter with your account.")
            print("3. Leave.")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                add_user(users)
            elif choice == "2":
                current_user = login_user(users)
            elif choice == "3":
                print("\nHave a good day!")
                break
            else:
                print("Invalid choice. Try again.")
        
        else:
            cars = load_cars()
            print("\n---Options---")
            print("1. View cars available")
            print("2. Add car")
            print("3. Buy car")
            print("4. Logout")

            choice = input("Choose the option you want: ").strip()

            if choice == "1":
                print("\n---Cars available---")
                show_cars(cars)
            elif choice == "2":
                add_car(cars)
            elif choice == "4":
                print("Have a nice day!")
                current_user = None
                continue

main()