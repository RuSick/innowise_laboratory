def generate_profile(name: str, age: int, hobbies: list[str]) -> dict[str, str | int | list[str]]:
    """
    Generate a user profile with calculations and life stage determination.

    Args:
        name (str): The user's full name
        age (int): The user's current age
        hobbies (list[str]): List of user's hobbies

    Returns:
        dict: Complete user profile containing name, age, life_stage, and hobbies
    """
    # Determine life stage based on age
    if 0 <= age <= 12:
        life_stage: str = "Child"
    elif 13 <= age <= 19:
        life_stage = "Teenager"
    else:  # age >= 20
        life_stage = "Adult"

    # Create and return the profile dictionary
    profile: dict[str, str | int | list[str]] = {
        "name": name,
        "age": age,
        "life_stage": life_stage,
        "hobbies": hobbies
    }
    return profile


def main() -> None:
    """Main function to run the profile generator."""
    # Get user input
    user_name: str = input("Enter your full name: ")
    birth_year_str: str = input("Enter your birth year: ")
    birth_year: int = int(birth_year_str)

    # Calculate current age (assuming current year is 2025)
    current_age: int = 2025 - birth_year

    # Collect hobbies
    hobbies: list[str] = []
    while True:
        hobby_input: str = input("Enter a favorite hobby or type 'stop' to finish: ")
        if hobby_input.lower() == "stop":
            break
        hobbies.append(hobby_input)

    # Process and generate the profile
    user_profile: dict[str, str | int | list[str]] = generate_profile(
        user_name, current_age, hobbies
    )

    # Display the output
    print("\nProfile Summary:")
    print(f"Name: {user_profile['name']}")
    print(f"Age: {user_profile['age']}")
    print(f"Life Stage: {user_profile['life_stage']}")

    # Check and display hobbies
    if not user_profile['hobbies']:
        print("You didn't mention any hobbies.")
    else:
        print(f"Favorite Hobbies ({len(user_profile['hobbies'])}):")
        for hobby in user_profile['hobbies']:
            print(hobby)


if __name__ == "__main__":
    main()

