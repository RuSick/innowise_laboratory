def print_menu() -> None:
    print("\n--- Student Grade Analyzer ---")
    print("1. Add a new student")
    print("2. Add grades for a student")
    print("3. Show report (all students)")
    print("4. Find top performer")
    print("5. Exit")


def add_student(students: list[dict[str, list[int]]]) -> None:
    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    if any(student["name"].lower() == name.lower() for student in students):
        print(f"Student '{name}' already exists.")
        return

    students.append({"name": name, "grades": []})
    print(f"Student '{name}' added successfully.")


def add_grades(students: list[dict[str, list[int]]]) -> None:
    if not students:
        print("No students available. Add a student first.")
        return

    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    student = next((s for s in students if s["name"].lower() == name.lower()), None)
    if student is None:
        print(f"Student '{name}' not found. Please add this student first.")
        return

    print("Enter grades one by one. Type 'done' to finish.")
    while True:
        grade_input = input("Enter a grade (or 'done' to finish): ").strip().lower()
        if grade_input == "done":
            break

        try:
            grade = int(grade_input)
            if grade < 0 or grade > 100:
                raise ValueError("Grade must be between 0 and 100.")
            student["grades"].append(grade)
            print(f"Recorded grade {grade}.")
        except ValueError as exc:
            print(f"Invalid input. {exc}")


def show_report(students: list[dict[str, list[int]]]) -> None:
    if not students:
        print("No students to report.")
        return

    print("\n--- Student Report ---")
    overall_sum = 0
    overall_count = 0
    averages: list[float] = []

    for student in students:
        grades = student["grades"]
        try:
            average = sum(grades) / len(grades)
        except ZeroDivisionError:
            print(f"{student['name']}'s average grade is N/A.")
            continue

        averages.append(average)
        overall_sum += sum(grades)
        overall_count += len(grades)
        print(f"{student['name']}'s average grade is {average:.1f}.")

    if not averages:
        print("No grades recorded yet.")
        return

    print(f"Max Average: {max(averages):.1f}")
    print(f"Min Average: {min(averages):.1f}")
    try:
        overall_average = overall_sum / overall_count
    except ZeroDivisionError:
        overall_average = 0
    print(f"Overall Average: {overall_average:.1f}")


def find_top_performer(students: list[dict[str, list[int]]]) -> None:
    if not students:
        print("No students available.")
        return

    top_student = max(
        students,
        key=lambda student: sum(student["grades"]) / len(student["grades"])
        if student["grades"]
        else float("-inf"),
        default=None,
    )
    if top_student is None or not top_student["grades"]:
        print("No grades recorded to determine top performer.")
        return

    top_avg = sum(top_student["grades"]) / len(top_student["grades"])
    if top_avg == float("-inf"):
        print("No grades recorded to determine top performer.")
        return

    print(
        f"The student with the highest average is {top_student['name']} "
        f"with a grade of {top_avg:.1f}."
    )


def main() -> None:
    students: list[dict[str, list[int]]] = []

    while True:
        print_menu()
        try:
            choice = int(input("Enter your choice: ").strip())
        except ValueError:
            print("Invalid option. Please enter a number from 1 to 5.")
            continue

        if choice == 1:
            add_student(students)
        elif choice == 2:
            add_grades(students)
        elif choice == 3:
            show_report(students)
        elif choice == 4:
            find_top_performer(students)
        elif choice == 5:
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()

