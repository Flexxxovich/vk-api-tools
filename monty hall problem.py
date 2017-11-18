import random

doors = ["goat", "goat", "goat"]
right_choices_with_change = 0
right_choices_without_change = 0

for attempt in range(0, 2000):

    car_position = random.randint(0, 2)
    doors[car_position] = "car"

    first_choice = random.randint(0, 2)

    for door_to_open in range(0, 3):
        if door_to_open != car_position and door_to_open != first_choice:
            doors[door_to_open] = "opened goat"
            break

    if attempt % 2 == 0:
        second_choice = [door_pos for door_pos in range(0, 3) if door_pos != first_choice and door_pos != door_to_open]
        if second_choice[0] == car_position:
            right_choices_with_change += 1

    if attempt % 2 == 1:
        if first_choice == car_position:
           right_choices_without_change += 1

print("winnings without change {0}%".format(right_choices_without_change/1000*100))
print("winnings with change {0}%".format(right_choices_with_change/1000*100))