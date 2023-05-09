import datetime
import random
import csv
import os

# Define the Exercise class with attributes: date_time, name, reps, and weight
class Exercise:
    def __init__(self, date_time, name, reps, weight):
        self.date_time = date_time
        self.name = name
        self.reps = reps
        self.weight = weight

    # Define a string representation for the Exercise class
    def __str__(self):
        if self.name == "Plank":
            return f"{self.name}: {self.reps} reps, {int(self.weight)} seconds"
        elif self.name in ["Push-ups", "Lunges"]:
            return f"{self.name}: {int(self.reps)} reps"
        else:
            return f"{self.name}: {int(self.reps)} reps, {int(self.weight)} lbs"

# List of possible exercises
exercise_list = [
    "Squats",
    "Deadlifts",
    "Bench Press",
    "Close-grip Bench Press"
    "Incline Bench Press",
    "Pull-ups",
    "Chin-ups",
    "Dips",
    "Rows",
    "Lunges",
    "Push-ups",
    "Plank",
    "Leg Press",
    "Calf Raises",
    "Shoulder Press",
    "Bicep Curls",
    "Tricep Extensions"
    "Face Pulls",
    "Romanian Deadlifts",
    "Glute Bridges or Hip Thrusts",
    "Lateral Raises",
]

# Function to suggest exercises for the workout
def suggest_exercises():
    # Randomly select 6 exercises
    selected_exercises = random.sample(exercise_list, 6)
    # Ensure the "Leg Press" and "Calf Raises" exercises are together, if both are selected
    if "Leg Press" in selected_exercises and "Calf Raises" in selected_exercises:
        selected_exercises.remove("Leg Press")
        selected_exercises.remove("Calf Raises")
        selected_exercises = ["Leg Press", "Calf Raises"] + selected_exercises
    return selected_exercises

# Function to read previous exercise data from a .csv file
def read_previous_exercises(file_path):
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return [Exercise(row[0], row[1], int(row[2]), float(row[3])) for row in reader]

# Function to find the closest previous exercise with a similar rep count
def find_closest_previous_exercise(exercise_name, reps, previous_exercises):
    if reps is None:
        return None

    # Filter the previous exercises to find those with the same name as the current exercise
    matching_exercises = [e for e in previous_exercises if e.name == exercise_name]
    if not matching_exercises:
        return None

    # Find the previous exercise with the closest rep count
    return min(matching_exercises, key=lambda e: abs(e.reps - reps))

# Function to write exercise data to a .csv file
def write_exercises_to_csv(file_path, exercises):
    header = ["Date/Time", "Exercise", "Reps", "Weight"]
    rows = [[e.date_time, e.name, e.reps, e.weight] for e in exercises]

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

# Function to get user input for weight or reps
def get_weight_or_reps(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

# Main function to run the workout program
def main():
    output_file = "workout_history.csv"
    # Read previous exercises from the .csv file
    previous_exercises = read_previous_exercises(output_file)

    # Get suggested exercises for the current workout
    suggested = suggest_exercises()
    print("Suggested Exercises:")
    print("\n".join(suggested))

    session = []
    skipped_exercises = []

    while suggested:
        exercise_name = suggested.pop(0)

        print()  # Add a blank line before each workout output
        reps = random.randint(7, 12) if exercise_name not in ["Plank", "Push-ups", "Lunges"] else 3 if exercise_name == "Plank" else None
        if reps is not None:
            print(f"{exercise_name} - {reps} reps")
        
        # Find the closest previous exercise with a similar rep count
        closest_previous = find_closest_previous_exercise(exercise_name, reps, previous_exercises)

        if closest_previous:
            closest_previous_str = f"{int(closest_previous.reps)} reps, {int(closest_previous.weight)}"
            if exercise_name != "Plank":
                closest_previous_str += " lbs"
            print(f"Previous: {closest_previous_str}")

        try:
            if exercise_name == "Plank":
                weight = int(input(f"Enter the time in seconds for {exercise_name}: "))
            elif exercise_name in ["Push-ups", "Lunges"]:
                reps = int(input(f"Enter the number of reps for {exercise_name}: "))
                weight = 0
            else:
                weight = int(input(f"Enter the weight in lbs for {exercise_name}: "))
            
            # Record the current date and time
            date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            exercise = Exercise(date_time, exercise_name, reps, weight)
            session.append(exercise)
        except ValueError:
            print("Invalid input. Exercise will be moved to the end.")
            suggested.append(exercise_name)

    # Print the workout summary
    print("\nCurrent Workout Summary:")  # Add a blank line before the workout summary
    print("\n".join(str(exercise) for exercise in session))

    # Write the updated exercise data to the .csv file
    write_exercises_to_csv(output_file, previous_exercises + session)

if __name__ == "__main__":
    main()
