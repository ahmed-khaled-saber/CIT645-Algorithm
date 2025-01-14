#DFS
from collections import deque

# Input Data
conflicts1 = {
    "CS102": ["Bio201"],
    "Bio201": ["CS102"],
    "Math101": [],  # Math101 has no conflicts
}

time_slots1 = ["9:00-10:00", "10:00-11:00", "11:00-12:00"]
rooms1 = {"R1": 50, "R2": 100}  # Room capacities
professor_availability1 = {
    "P1": ["10:00-11:00", "11:00-12:00"],  # P1 is only available during these times
    "P2": time_slots1,  # P2 is available all day
    "P3": time_slots1,  # P3 is available all day
}

course_details1 = {
    "CS102": {"students": 30},
    "Bio201": {"students": 80},
    "Math101": {"students": 40, "room": "R1"},  # Math101 must use R1
}

def dfs_schedule(conflicts, time_slots, rooms, professor_availability, course_details):
    # Initialize course schedule
    course_schedule1 = {}

    def dfs(course):
        # Find unavailable slots (used by neighbors)
        unavailable_slots = set(
            course_schedule1[neighbor]["time_slot"]
            for neighbor in conflicts1[course]
            if neighbor in course_schedule1
        )

        # Assign time slot, room, and professor
        for slot in time_slots1:
            if slot in unavailable_slots:
                continue  # Skip unavailable slots

            # Check room availability
            for room, capacity in rooms1.items():
                if course_details[course]["students"] > capacity:
                    continue  # Room too small

                # Check professor availability
                for professor, available_slots in professor_availability.items():
                    if slot not in available_slots:
                        continue  # Professor unavailable

                    # If all constraints are satisfied, assign the course
                    course_schedule1[course] = {
                        "time_slot": slot,
                        "room": room,
                        "professor": professor,
                    }
                    break
                else:
                    # No professor found; try another room
                    continue
                break
            else:
                # No room found; try another slot
                continue
            break

        # Visit neighbors
        for neighbor in conflicts1[course]:
            if neighbor not in course_schedule1:
                dfs(neighbor)

    # Start DFS for each course
    for course in conflicts1:
        if course not in course_schedule1:
            dfs(course)

    return course_schedule1
schedule1 = dfs_schedule(conflicts1, time_slots1, rooms1, professor_availability1, course_details1)


# Output the schedule
print("Course Schedule:")
for course, details in schedule1.items():
    print(f"{course}: Time Slot: {details['time_slot']}, Room: {details['room']}, Professor: {details['professor']}")