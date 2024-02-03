import pgzrun
import os
import time

WIDTH = 800
HEIGHT = 600

Number = 1
Clicks = 0
TotalClicks = 0
Achievements = {'TOP 10': False, 'FIRST CLICK': False, 'SPAMMER': False, 'MEGA CLICKER': False}

# Variable to store achievement unlock messages and their expiration time
achievement_messages = []

# Variable to store click times for spammer achievement
click_times = []

def draw():
    screen.fill((0, 0, 0))
    text = f"Clicks: {Clicks} out of {Number}"
    screen.draw.text(text, center=(screen.width / 2, screen.height / 2 - 30), fontsize=30, color="white")

    # Display achievements when 'a' key is pressed
    if keyboard.a:
        achievements_text = "\n".join([f"{achievement}: {'Unlocked' if unlocked else 'Locked'}" for achievement, unlocked in Achievements.items()])
        achievements_text = f"Achievements:\n{achievements_text}"
        screen.draw.text(achievements_text, center=(screen.width / 2, screen.height / 2 + 30), fontsize=20, color="white")

    # Display achievement unlock messages
    for msg, expiration_time in achievement_messages:
        screen.draw.text(msg, center=(screen.width / 2, screen.height / 2 + 60), fontsize=20, color="green")
        if time.time() > expiration_time:
            achievement_messages.remove((msg, expiration_time))

def on_mouse_down(pos, button):
    global Clicks, click_times, TotalClicks

    if button == 1:
        Clicks += 1
        TotalClicks += 1
        click_times.append(time.time())

        # Remove click times older than one second
        click_times = [click_time for click_time in click_times if time.time() - click_time <= 1]

def update():
    global Clicks, Number, TotalClicks
    if Clicks >= Number:
        Number += 1
        Clicks = 0
        check_achievements()

def on_key_down(key):
    if key == keys.S:
        save_game()
    elif key == keys.A:
        check_achievements()

def save_game():
    with open(get_file_path("saved_game.txt"), "w") as file:
        file.write(f"{Clicks}\n{Number}\n{TotalClicks}\n")
        # Save achievements
        for achievement, unlocked in Achievements.items():
            file.write(f"{achievement}:{unlocked}\n")

def load_game():
    try:
        with open(get_file_path("saved_game.txt"), "r") as file:
            global Clicks, Number, Achievements, TotalClicks
            lines = file.readlines()
            Clicks = int(lines[0].strip())
            Number = int(lines[1].strip())
            TotalClicks = int(lines[2])
            # Load achievements
            for line in lines[3:]:
                achievement, unlocked_str = line.strip().split(":")
                Achievements[achievement] = unlocked_str.lower() == 'true'
    except FileNotFoundError:
        # Handle the case where the file is not found (first run or deleted file)
        pass

def initialize_game():
    load_game()

def get_file_path(filename):
    return os.path.join(os.getcwd(), filename)

def check_achievements():
    global Clicks, Achievements, achievement_messages, click_times, TotalClicks
    if Number == 10 and not Achievements['TOP 10']:
        Achievements['TOP 10'] = True
        achievement_messages.append(("Achievement Unlocked: TOP 10", time.time() + 5))
    if Number == 2 and not Achievements['FIRST CLICK']:
        Achievements['FIRST CLICK'] = True
        achievement_messages.append(("Achievement Unlocked: FIRST CLICK", time.time() + 5))
    if len(click_times) >= 10 and not Achievements['SPAMMER']:
        Achievements['SPAMMER'] = True
        achievement_messages.append(("Achievement Unlocked: SPAMMER", time.time() + 5))
    if TotalClicks == 1000 and not Achievements['MEGA CLICKER']:
        Achievements['MEGA CLICKER'] = True
        achievement_messages.append(("Achievement Unlocked: MEGA CLICKER", time.time() + 5))

initialize_game()  # Load existing data before starting the game loop
pgzrun.go()
save_game()  # Save the initial values and achievements after loading
