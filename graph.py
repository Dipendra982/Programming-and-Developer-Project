import matplotlib.pyplot as plt

def plot_repeater_coverage(points, title, line_indices=None):
    # Extract X and Y coordinates
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]

    if not points:
        raise ValueError("points must be a non-empty list")

    plt.figure(figsize=(6, 6))
    plt.scatter(x_coords, y_coords, color='blue', s=100, label='Customer Homes')

    # If we know which points form the best line, draw it
    if line_indices:
        line_x = [points[i][0] for i in line_indices]
        line_y = [points[i][1] for i in line_indices]
        # Draw the signal path line
        plt.plot(line_x, line_y, color='red', linestyle='--', linewidth=2, label='Optimal Repeater Path')

    # Formatting the grid
    plt.title(title)
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.xticks(range(min(x_coords)-1, max(x_coords)+2))
    plt.yticks(range(min(y_coords)-1, max(y_coords)+2))
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    # Save a PNG to make it viewable outside interactive mode as well
    safe_title = title.replace(" ", "_").replace(':', '')
    filename = f"plot_{safe_title}.png"
    plt.savefig(filename, bbox_inches='tight')
    try:
        plt.show()
    except Exception:
        # In headless environments plt.show() may fail; we already saved the file.
        pass

# --- EXAMPLE 1 ---
points1 = [[1,1], [2,2], [3,3]]
plot_repeater_coverage(points1, "Example 1: Ideal Placement (3 Homes)", line_indices=[0, 1, 2])

# --- EXAMPLE 2 ---
points2 = [[1,1], [3,2], [5,3], [4,1], [2,3], [1,4]]
# The 4 points that align are [1,4], [2,3], [3,2], and [4,1] 
# These are indices: 5, 4, 1, 3 in the list above
plot_repeater_coverage(points2, "Example 2: Optimal Coverage (4 Homes)", line_indices=[5, 4, 1, 3])