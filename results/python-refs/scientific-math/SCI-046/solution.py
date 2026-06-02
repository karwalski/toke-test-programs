import random

def simulate_monty_hall(n_trials):
    stay_wins = 0
    switch_wins = 0
    
    for _ in range(n_trials):
        # Setup: 3 doors, car is behind one of them
        car_door = random.randint(0, 2)
        
        # Player picks a door
        player_choice = random.randint(0, 2)
        
        # Host opens a door with a goat (not the car door, not the player's choice)
        doors = [0, 1, 2]
        doors.remove(car_door)
        if player_choice in doors:
            doors.remove(player_choice)
        host_opens = random.choice(doors)
        
        # Stay strategy: player keeps original choice
        if player_choice == car_door:
            stay_wins += 1
            
        # Switch strategy: player switches to the remaining door
        remaining_doors = [0, 1, 2]
        remaining_doors.remove(player_choice)
        remaining_doors.remove(host_opens)
        switch_choice = remaining_doors[0]
        
        if switch_choice == car_door:
            switch_wins += 1
    
    stay_percentage = (stay_wins / n_trials) * 100
    switch_percentage = (switch_wins / n_trials) * 100
    
    print(f"Stay wins: {stay_wins} ({stay_percentage:.2f}%)")
    print(f"Switch wins: {switch_wins} ({switch_percentage:.2f}%)")

# Read input
n = int(input())
simulate_monty_hall(n)