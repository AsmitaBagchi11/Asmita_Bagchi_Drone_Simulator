import time
import random
import keyboard

position = {"x": 0, "y": 0, "z": 0}
battery = 100  
wind_force = 0  
is_flying = False
obstacles = [{"x": 5, "y": 5, "z": 0.5}, {"x": 10, "y": 10, "z": 1.5}]
log_file = open("drone_log.txt", "w")

def log(message):
    print(message)
    log_file.write(message + "\n")

def apply_wind():
    global wind_force
    wind_force = random.randint(-2, 2)
    position["x"] += wind_force

def move_drone(dx, dy, dz):
    position["x"] += dx
    position["y"] += dy
    position["z"] += dz
    if position["z"] < 0:
        position["z"] = 0
        crash()

def drain_battery():
    global battery
    battery -= random.uniform(0.3, 0.8)
    if battery < 0:
        battery = 0

def check_obstacles():
    for obs in obstacles:
        if (abs(position["x"] - obs["x"]) < 1 and
            abs(position["y"] - obs["y"]) < 1 and
            abs(position["z"] - obs["z"]) < 0.5):
            crash()

def crash():
    log("CRASH DETECTED at Position: " + str(position))
    land_drone()

def show_telemetry():
    log(f"Position: {position} | Battery: {battery:.2f}% | Wind: {wind_force}")

def takeoff_drone():
    global is_flying
    if not is_flying and battery > 0:
        is_flying = True
        position["z"] = 0.5
        log("Drone took off.")

def land_drone():
    global is_flying
    is_flying = False
    position["z"] = 0
    log("Drone landed.")

def control_drone():
    if keyboard.is_pressed("w"): move_drone(0, 1, 0)
    if keyboard.is_pressed("s"): move_drone(0, -1, 0)
    if keyboard.is_pressed("a"): move_drone(-1, 0, 0)
    if keyboard.is_pressed("d"): move_drone(1, 0, 0)
    if keyboard.is_pressed("up"): move_drone(0, 0, 0.5)
    if keyboard.is_pressed("down"): move_drone(0, 0, -0.5)
    if keyboard.is_pressed("t"): takeoff_drone()
    if keyboard.is_pressed("l"): land_drone()

def main():
    log("Starting Advanced Drone Simulation...")
    while battery > 0:
        control_drone()
        if is_flying:
            apply_wind()
            drain_battery()
            check_obstacles()
            show_telemetry()
        time.sleep(0.5)

    log("Battery Depleted. Drone landed safely.")
    log_file.close()

if __name__ == "__main__":
    main()
