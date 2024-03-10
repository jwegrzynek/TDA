import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon

# Generate a random 2D point cloud
num_points = 7
points = np.random.rand(num_points, 2)
radius = np.zeros(num_points)

# Create the figure and axes
fig, ax = plt.subplots(figsize=(8, 7.25))
plt.subplots_adjust(left=0.2, right=0.8, bottom=0.25)

# Plot initial 2D scatter plot
scatter = ax.scatter(points[:, 0], points[:, 1], s=30, color='red')

# Plotting circles
circle_patches = [Circle(center, radius, color='blue', alpha=0.5) for center, radius in zip(points, radius)]
circles = PatchCollection(circle_patches, match_original=True)
ax.add_collection(circles)

# Lines to connect intersecting circles
lines = []

# Polygons
polygons = []

# Add sliders
ax_radius = plt.axes([0.2, 0.02, 0.65, 0.03])
radius_slider = Slider(ax_radius, 'Radius', 0.0, 1, valinit=0.0)


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
                if circles_intersect_rips(circle_patches[i], circle_patches[j], circle_patches[k]):
                    vertices = np.array([points[i], points[j], points[k]])
                    polygon = Polygon(vertices, closed=True, facecolor='green', alpha=0.3)
                    polygons.append(polygon)
                    ax.add_patch(polygon)


def circles_intersect(circle1, circle2):
    distance = np.linalg.norm(np.array(circle1.center) - np.array(circle2.center))
    return distance < circle1.radius + circle2.radius


def circles_intersect_cech(circle1, circle2, circle3):
    pass


def circles_intersect_rips(circle1, circle2, circle3):
    intersection_1_2 = circles_intersect(circle1, circle2)
    intersection_2_3 = circles_intersect(circle2, circle3)
    intersection_1_3 = circles_intersect(circle1, circle3)

    return intersection_1_2 and intersection_2_3 and intersection_1_3


# Connect sliders to update function
radius_slider.on_changed(update)

# Reset button
reset_button_ax = plt.axes([0.8, 0.08, 0.1, 0.04])
reset_button = Button(reset_button_ax, 'Reset', color='lightgoldenrodyellow', hovercolor='0.975')


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

# Set plot parameters
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

plt.show()
