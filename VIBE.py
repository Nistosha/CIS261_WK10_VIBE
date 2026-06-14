# Student Grade Calculator
# Data structure: Option A - list of dictionaries
# File format: name|id|test1|test2|test3|average|grade

import os

FILE_NAME = "student_grades.txt"


def calculate_average(scores):
    return round(sum(scores) / len(scores), 2)


def calculate_grade(average):
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def load_students(filename):
    students = []
    if not os.path.exists(filename):
        return students

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split("|")
                if len(parts) != 7:
                    print(f"Warning: skipping invalid record: {line}")
                    continue

                name, student_id, test1, test2, test3, average, grade = parts
                try:
                    students.append({
                        "name": name,
                        "id": student_id,
                        "test1": float(test1),
                        "test2": float(test2),
                        "test3": float(test3),
                        "average": float(average),
                        "grade": grade,
                    })
                except ValueError:
                    print(f"Warning: invalid numeric data in record: {line}")
    except IOError as error:
        print(f"Error reading {filename}: {error}")

    return students


def save_students(filename, students):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for student in students:
                file.write(
                    f"{student['name']}|{student['id']}|{student['test1']:.2f}|"
                    f"{student['test2']:.2f}|{student['test3']:.2f}|{student['average']:.2f}|{student['grade']}\n"
                )
        print(f"Saved {len(students)} student record(s) to {filename}.\n")
    except IOError as error:
        print(f"Error saving {filename}: {error}")


def get_float_input(prompt):
    while True:
        text = input(prompt).strip()
        if text.upper() == "ESC":
            return None
        try:
            value = float(text)
            if 0 <= value <= 100:
                return value
            print("Please enter a score between 0 and 100.")
        except ValueError:
            print("Invalid entry. Enter a numeric score or ESC to cancel.")


def add_student(students):
    print("\nAdd New Student Record")
    print("Enter ESC at any prompt to cancel.")

    name = input("Student name: ").strip()
    if name.upper() == "ESC" or not name:
        print("Add student canceled.\n")
        return

    student_id = input("Student ID: ").strip()
    if student_id.upper() == "ESC" or not student_id:
        print("Add student canceled.\n")
        return

    scores = []
    for i in range(1, 4):
        score = get_float_input(f"Test {i} score (0-100): ")
        if score is None:
            print("Add student canceled.\n")
            return
        scores.append(score)

    average = calculate_average(scores)
    grade = calculate_grade(average)

    students.append({
        "name": name,
        "id": student_id,
        "test1": scores[0],
        "test2": scores[1],
        "test3": scores[2],
        "average": average,
        "grade": grade,
    })

    print(f"Added {name} with average {average:.2f} and grade {grade}.\n")


def display_students(students):
    if not students:
        print("\nNo student records available.\n")
        return

    print("\nStudent Records")
    header = f"{'Name':<20} {'ID':<8} {'Test 1':>7} {'Test 2':>7} {'Test 3':>7} {'Average':>8} {'Grade':>6}"
    print(header)
    print("-" * len(header))

    for student in students:
        print(
            f"{student['name']:<20} {student['id']:<8} {student['test1']:>7.2f} "
            f"{student['test2']:>7.2f} {student['test3']:>7.2f} {student['average']:>8.2f} "
            f"{student['grade']:>6}"
        )
    print()


def display_statistics(students):
    if not students:
        print("\nNo student records available for statistics.\n")
        return

    averages = [student["average"] for student in students]
    highest = max(averages)
    lowest = min(averages)
    class_average = round(sum(averages) / len(averages), 2)

    print("\nClass Statistics")
    print(f"Highest average: {highest:.2f}")
    print(f"Lowest average:  {lowest:.2f}")
    print(f"Class average:   {class_average:.2f}\n")


def search_student(students):
    if not students:
        print("\nNo student records available to search.\n")
        return

    query = input("Enter student name to search: ").strip()
    if query.upper() == "ESC" or not query:
        print("Search canceled.\n")
        return

    matches = [
        student for student in students if query.lower() in student["name"].lower()
    ]

    if not matches:
        print(f"\nNo students found matching '{query}'.\n")
        return

    print(f"\nSearch results for '{query}':")
    header = f"{'Name':<20} {'ID':<8} {'Test 1':>7} {'Test 2':>7} {'Test 3':>7} {'Average':>8} {'Grade':>6}"
    print(header)
    print("-" * len(header))
    for student in matches:
        print(
            f"{student['name']:<20} {student['id']:<8} {student['test1']:>7.2f} "
            f"{student['test2']:>7.2f} {student['test3']:>7.2f} {student['average']:>8.2f} "
            f"{student['grade']:>6}"
        )
    print()


def main():
    students = load_students(FILE_NAME)
    print("Student Grade Calculator")
    print("Data will be loaded from and saved to student_grades.txt.")
    print(f"Loaded {len(students)} existing student record(s).\n")

    while True:
        print("Menu")
        print("1 - Add new student")
        print("2 - Display all students")
        print("3 - Display class statistics")
        print("4 - Search student by name")
        print("ESC - Save and exit")

        choice = input("Select an option: ").strip()
        if choice.upper() == "ESC":
            save_students(FILE_NAME, students)
            print("Exiting program. Goodbye!")
            break

        if choice == "1":
            add_student(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            display_statistics(students)
        elif choice == "4":
            search_student(students)
        else:
            print("Invalid choice. Please select 1-4 or ESC to exit.\n")


if __name__ == "__main__":
    main()
