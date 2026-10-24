import tkinter as tk
import math


window = tk.Tk()
window.title("我的小车模拟器")
window.geometry("600x400")
canvas = tk.Canvas(window, width=600, height=400, bg="white")
canvas.pack()

car = canvas.create_polygon(
    270, 185,
    330, 185,
    330, 215,
    270, 215,
    fill="blue"
)
heading_line = canvas.create_line(
    300, 200, 330, 200,
    fill="red",
    width=3,
    arrow=tk.LAST
)
obstacle = canvas.create_rectangle(
    100, 250, 180, 300,
    fill="darkgray"
)
obstacle2 = canvas.create_rectangle(
    450, 150, 500, 250,
    fill="darkgray"
)
obstacle3 = canvas.create_rectangle(260,60,340,100,fill="darkgrey")

obstacles = [obstacle, obstacle2, obstacle3]
state = {"step":0,"angle":0, "distance":0, "paused":False}
def turn_car(change):
    coords = canvas.coords(car)
    center_x, center_y = get_center(coords)

    new_angle = (state["angle"] + change) % 360
    new_points = get_car_points(center_x, center_y, new_angle)

    if can_move(new_points, 0, 0):
        state["angle"] = new_angle
        canvas.coords(car, *new_points)


def turn_left(event):
    turn_car(-10)


def turn_right(event):
    turn_car(10)


def toggle_pause(event):
    state["paused"] = not state["paused"]
def get_bounds(coords):
    xs = coords[0::2]
    ys = coords[1::2]

    return [min(xs), min(ys), max(xs), max(ys)]

def get_center(coords):
    left,top, right, bottom = get_bounds(coords)
    return(left + right) / 2, (top + bottom) / 2

def get_end(center_x, center_y, radians, arrow_length):
    end_x = center_x + arrow_length * math.cos(radians)
    end_y = center_y + arrow_length * math.sin(radians)
    return end_x, end_y
def get_car_points(center_x, center_y, angle):
    radians = math.radians(angle)
    corners = [(-30, -15), (30, -15), (30, 15), (-30, 15)]
    points = []

    for x, y in corners:
        rotated_x = x * math.cos(radians) - y * math.sin(radians)
        rotated_y = x * math.sin(radians) + y * math.cos(radians)

        points.extend([
            center_x + rotated_x,
            center_y + rotated_y
        ])

    return points

def update_heading():
    coords = canvas.coords(car)
    radians = math.radians(state["angle"])
    arrow_length = 35
    center_x, center_y = get_center(coords)
    end_x, end_y = get_end(center_x, center_y, radians, arrow_length)
    canvas.coords(heading_line,center_x,center_y,end_x,end_y)
def update_display(coords,dx,dy):
    center_x, center_y = get_center(coords)
    if state["paused"]:
        status = "Paused"
    elif state["step"] == 0:
        status = "Stopped"
    elif not can_move(coords, dx, dy):
        status = "Blocked"
    elif state["step"] < 0:
        status = "Reversing"
    else:
        status = "Moving"

    canvas.itemconfig(
        step_text,
        text=f"Step: {state['step']} px | Angle: {state['angle']}° | {status} |pos: {center_x:.0f}, {center_y:.0f}"
        f"|Distance:{state["distance"]:.1f}px")
def overlaps(a, b):
    separated = (
        a[2] <= b[0]
        or a[0] >= b[2]
        or a[3] <= b[1]
        or a[1] >= b[3]
    )
    return not separated
def can_move(coords, dx, dy):
    coords = get_bounds(coords)
    next_coords = [
        coords[0] + dx,
        coords[1] + dy,
        coords[2] + dx,
        coords[3] + dy
    ]

    inside_canvas = (
        next_coords[0] >= 0
        and next_coords[2] <= 600
        and next_coords[1] >= 0
        and next_coords[3] <= 400
    )
    if not inside_canvas:
       return False

    for item in obstacles:
        obstacle_coords = canvas.coords(item)
        if overlaps(next_coords, obstacle_coords):
            return False

    return True



def auto_move():
    coords = canvas.coords(car)
    radians = math.radians(state["angle"])

    dx = state["step"] * math.cos(radians)
    dy = state["step"] * math.sin(radians)


    if not state["paused"] and can_move(coords,dx,dy):
        state["distance"] += math.hypot(dx,dy)
        old_x, old_y = get_center(coords)
        canvas.move(car,dx,dy)

        new_coords = canvas.coords(car)
        new_x, new_y = get_center(new_coords)

        if state["step"] != 0:
            canvas.create_line(
                old_x, old_y,
                new_x, new_y,
                fill="gray",
                tags="trail"
        )

    update_heading()
    coords = canvas.coords(car)
    update_display(coords,dx,dy)
    window.after(50,auto_move)

def speed_up(event):
    state["step"] += 1
    if state["step"]>10:
        state["step"]=10

def slow_down(event):
    state["step"] -= 1

    if state["step"] < -5:
        state["step"] = -5

def reset_car(event):
    canvas.coords(car, *get_car_points(300, 200, 0))
    state["step"] = 0
    state["angle"]=0
    state["distance"] = 0
    canvas.delete("trail")
    state["paused"] = False

def stop_car(event):
    state["step"] = 0


step_text = canvas.create_text(
    300, 20,
    text="step: 0",
    fill="black"
)


window.bind("<Left>", turn_left)
window.bind("<Right>", turn_right)
window.bind("<KeyPress-w>", speed_up)
window.bind("<KeyPress-s>", slow_down)
window.bind("<KeyPress-p>", toggle_pause)
window.bind("<KeyPress-r>", reset_car)
window.bind("<space>", stop_car)


window.after(50, auto_move)
window.mainloop()
