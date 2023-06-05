from collections import defaultdict


class InvalidGradeError(Exception):
    """
    Exception raised for invalid grades (not in the range 1 to 5).
    """

    pass


def check_grade(grade: str) -> int:
    """
    Checks if the input string can be converted into a valid grade (1 to 5).
    Decimal numbers are rounded to the nearest integer.

    : param grade: the input string
    : return: the grade as an integer
    : raise ValueError: if the input string cannot be converted into a number
    : raise InvalidGradeError: if the input string cannot be converted into a valid grade
    """

    # If the input is not a number, this line throws a ValueError
    grade = float(grade)

    # Round to nearest integer, and output a warning if rounding was necessary
    grade_int = round(grade)
    if grade != grade_int:
        print(f"Warning: Rounding grade {grade} to {grade_int}")

    # Ensure that the number is a valid grade, and throw an InvalidGradeError if not
    if not (grade_int > 0 and grade_int < 6):
        raise InvalidGradeError(f"Invalid grade: {grade_int}")

    # Return the grade as an integer
    return grade_int


grade_count = defaultdict(int)
while True:
    # Read lines from the user until the user writes "exit"
    line = input("\nInput: ")
    if line == "exit":
        print("Exiting program")
        break

    # Don't process empty inputs, just prompt again
    if line == "":
        continue

    # The user can input multiple numbers/words separated by spaces, process them one by one
    for word in line.split(" "):
        try:
            # Convert the input string into a grade, and add it to the grade_count dictionary
            # If an error occurs here, print an error message and continue with the next word
            grade = check_grade(word)
            grade_count[grade] += 1
        except ValueError:
            print(f"Error: Input contains non-number {word}")
        except InvalidGradeError as e:
            print(f"Error: {e}")

    # Dictionary keys are not sorted by default, so sort them before printing
    sorted_entriess = sorted(grade_count.items())

    # All grades that have been recorded so far with their counts
    for grade, count in sorted_entries:
        print(f"Grade {grade}: {count}")

    # Calculate the average grade
    grades_total = sum(grade_count.values())
    grades_sum = sum(grade * count for grade, count in sorted_entries)

    if grades_total == 0:
        # Prevent division by zero if no grades have been entered yet
        continue

    # Print the average grade with one decimal place
    grade_avg = grades_sum / grades_total
    print(f"Average grade (out of {grades_total}): {grade_avg:.1f}")
