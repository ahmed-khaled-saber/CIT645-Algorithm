#BFS
from collections import deque

# Input Data
conflicts = {
    "CS102": ["Bio201"],
    "Bio201": ["CS102"],
    "Math101": [],  # Math101 has no conflicts
}

time_slots = ["9:00-10:00", "10:00-11:00", "11:00-12:00"]
rooms = {"R1": 50, "R2": 100}  # Room capacities
professor_availability = {
    "P1": ["10:00-11:00", "11:00-12:00"],  # P1 is only available during these times
    "P2": time_slots,  # P2 is available all day
    "P3": time_slots,  # P3 is available all day
}

course_details = {
    "CS102": {"students": 30},
    "Bio201": {"students": 80},
    "Math101": {"students": 40, "room": "R1"},  # Math101 must use R1
}

# BFS-based scheduling
def bfs_schedule(conflicts, time_slots, rooms, professor_availability, course_details):
    # Initialize course schedule
    course_schedule = {}

    # Queue for BFS
    queue = deque()

    # Start with the first course
    for course in conflicts:
        if course not in course_schedule:
            queue.append(course)

            while queue:
                current_course = queue.popleft()

                # Get course details
                num_students = course_details[current_course]["students"]
                required_room = course_details[current_course].get("room")  # Fixed room?

                # Find unavailable slots (used by neighbors which is in conflicts)
                unavailable_slots = set(
                    course_schedule[neighbor]["time_slot"]
                    for neighbor in conflicts[current_course]
                    if neighbor in course_schedule
                )

                # Assign a time slot, room, and professor
                for slot in time_slots:
                    if slot not in unavailable_slots:
                        # Assign a room
                        for room, capacity in rooms.items():
                            if capacity >= num_students and (not required_room or room == required_room):
                                # Assign a professor
                                for professor, available_slots in professor_availability.items():
                                    if slot in available_slots:
                                        # Schedule the course
                                        course_schedule[current_course] = {
                                            "time_slot": slot,
                                            "room": room,
                                            "professor": professor,
                                        }
                                        break
                                if current_course in course_schedule:
                                    break
                        if current_course in course_schedule:
                            break

                # Add neighbors to the queue
                for neighbor in conflicts[current_course]:
                    if neighbor not in course_schedule:
                        queue.append(neighbor)

    return course_schedule


# Schedule courses
schedule = bfs_schedule(conflicts, time_slots, rooms, professor_availability, course_details)

# Output the schedule
print("Course Schedule:")
for course, details in schedule.items():
    print(f"{course}: Time Slot: {details['time_slot']}, Room: {details['room']}, Professor: {details['professor']}")
