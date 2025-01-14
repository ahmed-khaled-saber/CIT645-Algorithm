import random

# Define problem parameters
courses = ["Math101", "CS102", "Bio201"]
professors = ["P1", "P2", "P3"]

# Rooms and capacities
rooms = {"R1": 50, "R2": 100}

# Available time slots
time_slots = ["9:00-10:00", "10:00-11:00", "11:00-12:00"]

# Constraints Definition
constraints = {
    "room_assignment": {  # Fixed room assignments
        "Math101": "R1"
    },
    "professor_availability": {  # Professors' available time slots
        "P1": ["10:00-11:00", "11:00-12:00"],
        "P2": ["9:00-10:00", "10:00-11:00", "11:00-12:00"],
        "P3": ["9:00-10:00", "10:00-11:00", "11:00-12:00"],
    },
    "course_conflicts": [  # Courses that cannot occur simultaneously
        ("CS102", "Bio201"),
        # Add more conflicting course pairs as needed
    ],
    "room_capacity_constraints": {  # Optional: Define course sizes if needed
        "Math101": 40,
        "CS102": 60,
        "Bio201": 70,
        # Add more courses and their expected enrollment
    },
    # Additional constraints can be added here
}

# Genetic algorithm parameters
population_size = 100
mutation_rate = 0.1
generations = 100


def create_chromosome():
    """
    Create a single timetable (chromosome).
    Each course is assigned a (room, time_slot, professor) triple.
    Ensures that room assignments and professor availability constraints are respected.
    """
    chromosome = {}
    for course in courses:
        # Handle room assignments based on constraints
        if course in constraints["room_assignment"]:
            room = constraints["room_assignment"][course]
        else:
            room = random.choice(list(rooms.keys()))

        # Assign a random time slot
        time_slot = random.choice(time_slots)

        # Assign a professor based on availability
        possible_professors = [
            p for p in professors if time_slot in constraints["professor_availability"].get(p, [])
        ]
        if not possible_professors:
            # If no professor is available, assign randomly (fitness will penalize)
            professor = random.choice(professors)
        else:
            professor = random.choice(possible_professors)

        chromosome[course] = {
            "room": room,
            "time_slot": time_slot,
            "professor": professor
        }
    return chromosome


def calculate_fitness(chromosome):
    """
    Calculate the fitness of a chromosome.
    Higher fitness indicates a better schedule.
    Penalties are subtracted for constraint violations.
    """
    fitness = 10  # Base fitness

    # 1. Room Assignment Constraints
    for course, assigned_room in constraints["room_assignment"].items():
        if chromosome.get(course, {}).get("room") != assigned_room:
            fitness -= 5  # Penalty for incorrect room assignment

    # 2. Professor Availability Constraints
    for course, assignment in chromosome.items():
        prof = assignment["professor"]
        slot = assignment["time_slot"]
        available_slots = constraints["professor_availability"].get(prof, [])
        if slot not in available_slots:
            fitness -= 5  # Penalty for professor unavailability

    # 3. Course Conflicts
    for conflict_pair in constraints["course_conflicts"]:
        course1, course2 = conflict_pair
        if (
            course1 in chromosome and course2 in chromosome and
            chromosome[course1]["time_slot"] == chromosome[course2]["time_slot"]
        ):
            fitness -= 5  # Penalty for conflicting courses scheduled simultaneously

    # 4. Professor Scheduling Conflicts
    prof_timeslot_count = {}
    for assignment in chromosome.values():
        key = (assignment["professor"], assignment["time_slot"])
        prof_timeslot_count[key] = prof_timeslot_count.get(key, 0) + 1
    for count in prof_timeslot_count.values():
        if count > 1:
            fitness -= 5 * (count - 1)  # Penalty for multiple assignments

    # 5. Room Capacity Constraints (Optional)
    if "room_capacity_constraints" in constraints:
        room_usage = {}
        for course, assignment in chromosome.items():
            room = assignment["room"]
            time_slot = assignment["time_slot"]
            key = (room, time_slot)
            room_usage[key] = room_usage.get(key, 0) + constraints["room_capacity_constraints"].get(course, 0)

        for (room, time_slot), total_students in room_usage.items():
            capacity = rooms.get(room, 0)
            if total_students > capacity:
                fitness -= 5 * (total_students - capacity)  # Penalty for exceeding capacity

    # Additional constraints and rewards can be handled here

    return fitness


def selection(population):
    """
    Perform weighted random selection based on fitness.
    Returns two parents for crossover.
    """
    fitness_values = [calculate_fitness(chromosome) for chromosome in population]

    # Ensure all fitness values are positive
    min_fitness = min(fitness_values)
    if min_fitness <= 0:
        offset = 1 - min_fitness
        adjusted_fitness = [f + offset for f in fitness_values]
    else:
        adjusted_fitness = fitness_values.copy()

    # Select two parents based on adjusted fitness
    parents = random.choices(population, weights=adjusted_fitness, k=2)
    return parents[0], parents[1]


def crossover(parent1, parent2):
    """
    Perform uniform crossover between two parents.
    Each course has a 50% chance of inheriting from either parent.
    """
    offspring = {}
    for course in courses:
        if random.random() < 0.5:
            offspring[course] = parent1[course].copy()
        else:
            offspring[course] = parent2[course].copy()
    return offspring


def mutate(chromosome):
    """
    Mutate a chromosome by randomly changing assignments based on mutation rate.
    Ensures that room assignments and professor availability constraints are respected.
    """
    for course in courses:
        if random.random() < mutation_rate:
            # Handle room assignments based on constraints
            if course in constraints["room_assignment"]:
                chromosome[course]["room"] = constraints["room_assignment"][course]
            else:
                chromosome[course]["room"] = random.choice(list(rooms.keys()))

            # Assign a new time slot
            new_slot = random.choice(time_slots)
            chromosome[course]["time_slot"] = new_slot

            # Assign a professor based on new time slot availability
            possible_professors = [
                p for p in professors if new_slot in constraints["professor_availability"].get(p, [])
            ]
            if possible_professors:
                chromosome[course]["professor"] = random.choice(possible_professors)
            else:
                # If no professor is available, assign randomly (fitness will penalize)
                chromosome[course]["professor"] = random.choice(professors)

    return chromosome


def create_initial_population():
    """
    Generate the initial population of chromosomes.
    """
    return [create_chromosome() for _ in range(population_size)]


def genetic_algorithm():
    """
    Execute the genetic algorithm to optimize the timetable.
    """
    population = create_initial_population()
    best_chromosome = None
    best_fitness = float('-inf')

    for generation in range(generations):
        new_population = []

        # Generate offspring through selection, crossover, and mutation
        for _ in range(population_size // 2):
            parent1, parent2 = selection(population)
            offspring1 = crossover(parent1, parent2)
            offspring2 = crossover(parent2, parent1)
            offspring1 = mutate(offspring1)
            offspring2 = mutate(offspring2)
            new_population.extend([offspring1, offspring2])

        # Replace the old population with the new one
        population = new_population

        # Evaluate and track the best chromosome
        for chromosome in population:
            fitness = calculate_fitness(chromosome)
            if fitness > best_fitness:
                best_fitness = fitness
                best_chromosome = chromosome

        # Optional: Print progress every 10 generations
        if (generation + 1) % 10 == 0:
            print(f"Generation {generation + 1}: Best Fitness = {best_fitness}")

    return best_chromosome, best_fitness


if __name__ == "__main__":
    best_schedule, best_fitness = genetic_algorithm()
    print("\nOptimized Schedule:")
    for course, assignment in best_schedule.items():
        print(
            f"{assignment['time_slot']}: {course} in {assignment['room']} "
            f"with {assignment['professor']}"
        )
    print(f"Fitness: {best_fitness}")
