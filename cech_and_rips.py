import warnings
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon

warnings.filterwarnings("ignore", category=RuntimeWarning)

# Generate a random 2D point cloud
num_points = 7
points = np.random.rand(num_points, 2)
radius = np.zeros(num_points)
cech = True
rips = False

# Create the figure and axes
fig, ax = plt.subplots(figsize=(8, 7.25))
plt.subplots_adjust(left=0.2, right=0.8, bottom=0.25)
fig.suptitle("Visualisation of Cech Complex", y=0.94, fontsize=20)

# Plot initial scatter plot
scatter = ax.scatter(points[:, 0], points[:, 1], s=30, color='red', zorder=10)

# Plotting circles
circle_patches = [Circle(center, radius, color='blue', alpha=0.5) for center, radius in zip(points, radius)]
circles = PatchCollection(circle_patches, match_original=True)
ax.add_collection(circles)

# Array to store lines and polygons
lines = []
polygons = []

# Add sliders
ax_radius = plt.axes([0.2, 0.06, 0.65, 0.03])
radius_slider = Slider(ax_radius, 'Radius', 0.0, 1, valinit=0.0)

# Reset button
reset_button_ax = plt.axes([0.71, 0.13, 0.1, 0.04])
reset_button = Button(reset_button_ax, 'Reset', color='lightgoldenrodyellow', hovercolor='0.975')

# Cech button
cech_button_ax = plt.axes([0.19, 0.13, 0.2, 0.04])
cech_button = Button(cech_button_ax, 'Switch To Cech', color='lightgoldenrodyellow', hovercolor='0.975')

# Rips button
rips_button_ax = plt.axes([0.45, 0.13, 0.2, 0.04])
rips_button = Button(rips_button_ax, 'Switch To Rips', color='lightgoldenrodyellow', hovercolor='0.975')


# Update function for sliders
def update(val):
    new_radius = radius_slider.val

    # Update circle properties directly
    for circle in circle_patches:
        circle.set_radius(new_radius)

    # Check for circle intersections and draw lines
    update_lines()

    # Update the collection
    circles.set_paths(circle_patches)

    fig.canvas.draw_idle()


def switch_to_cech(event):
    global cech, rips
    cech = True
    rips = False
    fig.suptitle("Visualisation of Cech Complex", y=0.94, fontsize=20)
    update(event)
    fig.canvas.draw_idle()


def switch_to_rips(event):
    global cech, rips
    cech = False
    rips = True
    fig.suptitle("Visualisation of Rips Complex", y=0.94, fontsize=20)
    update(event)
    fig.canvas.draw_idle()


def update_lines():
    # Remove existing lines
    for line in lines:
        line.remove()

    lines.clear()

    for polygon in polygons:
        polygon.remove()

    polygons.clear()

    # Check for circle intersections and draw lines
    for i in range(num_points):
        for j in range(i + 1, num_points):
            if circles_intersect(circle_patches[i], circle_patches[j]):
                line = Line2D([points[i, 0], points[j, 0]], [points[i, 1], points[j, 1]], color='red')
                lines.append(line)
                ax.add_line(line)

    # Plot triangles between centers of intersecting circles
    for i in range(num_points):
        for j in range(i + 1, num_points):
            for k in range(j + 1, num_points):
                if cech is True:
                    if circles_intersect_cech(circle_patches[i], circle_patches[j], circle_patches[k]):
                        vertices = np.array([points[i], points[j], points[k]])
                        polygon = Polygon(vertices, closed=True, facecolor='green', alpha=0.3)
                        polygons.append(polygon)
                        ax.add_patch(polygon)
                if rips is True:
                    if circles_intersect_rips(circle_patches[i], circle_patches[j], circle_patches[k]):
                        vertices = np.array([points[i], points[j], points[k]])
                        polygon = Polygon(vertices, closed=True, facecolor='green', alpha=0.3)
                        polygons.append(polygon)
                        ax.add_patch(polygon)


def circles_intersect(circle1, circle2):
    distance = np.linalg.norm(np.array(circle1.center) - np.array(circle2.center))
    return distance < circle1.radius + circle2.radius


def point_inside_circle(point, circle):
    x, y = point
    return (x - circle.center[0]) ** 2 + (y - circle.center[1]) ** 2 <= circle.radius ** 2


def circles_intersect_cech(circle1, circle2, circle3):
    # Find the intersection points of circle1 and circle2
    x1, y1, r1 = circle1.center[0], circle1.center[1], circle1.radius
    x2, y2, r2 = circle2.center[0], circle2.center[1], circle2.radius

    d = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h = np.sqrt(r1 ** 2 - a ** 2)
    x3 = x1 + a * (x2 - x1) / d
    y3 = y1 + a * (y2 - y1) / d

    intersection_1_2 = [(x3 + h * (y2 - y1) / d, y3 - h * (x2 - x1) / d),
                        (x3 - h * (y2 - y1) / d, y3 + h * (x2 - x1) / d)]

    # Check if any of the intersection points lying on circle3
    for point in intersection_1_2:
        if point_inside_circle(point, circle3):
            return True

    return False


def circles_intersect_rips(circle1, circle2, circle3):
    intersection_1_2 = circles_intersect(circle1, circle2)
    intersection_2_3 = circles_intersect(circle2, circle3)
    intersection_1_3 = circles_intersect(circle1, circle3)

    return intersection_1_2 and intersection_2_3 and intersection_1_3


# Connect sliders to update function
radius_slider.on_changed(update)


def reset(event):
    global points, circle_patches

    # Generate new random points
    points = np.random.rand(num_points, 2)

    # Update scatter plot with new points
    scatter.set_offsets(points)

    # Update circle patches with new points
    circle_patches = [Circle(center, radius, color='blue', alpha=0.5) for center, radius in zip(points, radius)]
    circles.set_paths(circle_patches)

    # Clear existing lines
    for line in lines:
        line.remove()
    lines.clear()

    for polygon in polygons:
        polygon.remove()

    polygons.clear()

    fig.canvas.draw_idle()


reset_button.on_clicked(reset)
rips_button.on_clicked(switch_to_rips)
cech_button.on_clicked(switch_to_cech)

# Set plot parameters
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

plt.show()
