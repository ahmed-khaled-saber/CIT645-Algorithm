# Inputs
courses = [("Math101", 30), ("CS102", 60), ("Bio201", 50)]  # (course, students)
rooms = [("R1", 50), ("R2", 100)]  # (room, capacity)
time_slots = [1, 2, 3]  # Time slots: 9:00-10:00, 10:00-11:00, 11:00-12:00
prof_availability = {"Math101": [2, 3], "CS102": [1, 2], "Bio201": [1, 3]}  # Professors' availability
conflicts = [("CS102", "Bio201")]  # Courses that cannot overlap

# Sorting rooms (Greedy Choice)
rooms.sort(key=lambda x: x[1])  # Sort rooms by capacity (small to large)

# DP Table: Initialize
n = len(courses)
m = len(rooms)
k = len(time_slots)
dp = [[[False for _ in range(k)] for _ in range(m)] for _ in range(n)]

# Build the DP table
for i in range(n):  # Iterate over courses
    course, students = courses[i]
    for j in range(m):  # Iterate over rooms
        room, capacity = rooms[j]
        if students <= capacity:  # Room must be large enough
            for t in range(k):  # Iterate over time slots
                # Check professor availability
                if t + 1 in prof_availability[course]:
                    # Check for course conflicts
                    conflict_free = True
                    for conflict_course in conflicts:
                        if course in conflict_course:
                            other_course = conflict_course[0] if course == conflict_course[1] else conflict_course[1]
                            # Find index of the conflicting course
                            conflict_index = next((idx for idx, c in enumerate(courses) if c[0] == other_course), -1)
                            # Check if conflicting course is scheduled at the same time
                            if conflict_index != -1:
                                conflict_free = all(
                                    not dp[conflict_index][room_idx][t]
                                    for room_idx in range(m)
                                )
                    if conflict_free:
                        dp[i][j][t] = True  # Course can be scheduled in this room and time slot

# Assign courses greedily using the DP table
schedule = []  # Final schedule
used_slots = set()  # To track used room-time combinations

for i in range(n):  # Iterate over courses
    for j in range(m):  # Iterate over rooms
        for t in range(k):  # Iterate over time slots
            if dp[i][j][t] and (j, t) not in used_slots:
                course, _ = courses[i]
                room, _ = rooms[j]
                schedule.append((course, room, t + 1))  # Add course, room, and time slot to schedule
                used_slots.add((j, t))  # Mark the room and time slot as used
                break

# Output the schedule
print("Final Schedule:")
for course, room, time_slot in schedule:
    print(f"Course: {course}, Room: {room}, Time Slot: {time_slot}")
