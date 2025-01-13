class Timetabling:
    def __init__(self, courses, professors, rooms, time_slots, constraints):
        self.courses = courses
        self.professors = professors
        self.rooms = rooms
        self.time_slots = time_slots
        self.constraints = constraints
        self.schedule = {}
        self.energy_usage = 0   

    def is_valid_assignment(self, course, professor, room, time_slot):
        # Check specific room constraints
        if course in self.constraints.get("room_constraints", {}):
            required_room = self.constraints["room_constraints"][course]
            if room != required_room:
                return False

        # Check professor availability
        if time_slot not in self.professors[professor]:
            return False

        # Check room availability
        for assigned_course, details in self.schedule.items():
            if details["room"] == room and details["time_slot"] == time_slot:
                return False

        # Check professor assignment conflicts
        for assigned_course, details in self.schedule.items():
            if details["professor"] == professor and details["time_slot"] == time_slot:
                return False

        # Check "no overlap" constraints
        for conflict_pair in self.constraints.get("no_overlap", []):
            if course in conflict_pair:
                other_course = conflict_pair[0] if conflict_pair[1] == course else conflict_pair[1]
                if other_course in self.schedule and self.schedule[other_course]["time_slot"] == time_slot:
                    return False

        return True

    def calculate_energy_savings(self):
        baseline_energy = sum(room["capacity"] for room in self.rooms for _ in self.time_slots)
        optimized_energy = self.energy_usage
        return round((baseline_energy - optimized_energy) / baseline_energy * 100, 2)

    def backtrack(self, course_index=0):
        if course_index == len(self.courses):
            return True  # All courses scheduled successfully

        course = self.courses[course_index]
        for time_slot in self.time_slots:
            for room in self.rooms:
                for professor in self.professors:
                    if self.is_valid_assignment(course, professor, room["name"], time_slot):
                        # Assign the course
                        self.schedule[course] = {
                            "professor": professor,
                            "room": room["name"],
                            "time_slot": time_slot,
                        }
                        self.energy_usage += room["capacity"]

                        # Recurse to the next course
                        if self.backtrack(course_index + 1):
                            return True

                        # Backtrack
                        del self.schedule[course]
                        self.energy_usage -= room["capacity"]

        return False

    def solve(self):
        if self.backtrack():
            energy_savings = self.calculate_energy_savings()
            return self.schedule, energy_savings
        else:
            return "No feasible solution found", 0


# Example Input
courses = ["Math101", "CS102", "Bio201"]
professors = {
    "P1": ["10:00-11:00", "11:00-12:00"],
    "P2": ["9:00-10:00", "10:00-11:0x0"],
    "P3": ["9:00-10:00", "11:00-12:00"]
}
rooms = [{"name": "R1", "capacity": 50}, {"name": "R2", "capacity": 100}]
time_slots = ["9:00-10:00", "10:00-11:00", "11:00-12:00"]
constraints = {
    "room_constraints": {"Math101": "R1"},
    "no_overlap": [("CS102", "Bio201")]
}

# Solve Timetabling
timetabling = Timetabling(courses, professors, rooms, time_slots, constraints)
solution, energy_savings = timetabling.solve()

# Output
print("Generated Timetable:")
if solution != "No feasible solution found":
    for course, details in solution.items():
        print(f"{details['time_slot']}: {course} in {details['room']} with {details['professor']}")
    print(f"Energy Savings: {energy_savings}%")
else:
    print(solution)
        