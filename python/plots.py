import pygame
import numpy as np
import matplotlib.pyplot as plt

# Initialize pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Braitenberg Vehicle Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Car properties
car_radius = 20
car_x = 100
car_y = 300
car_speed = 2

# Obstacle properties
num_obstacles = 5
obstacle_radius = 15
obstacle_positions = np.random.randint(50, screen_width - 50, size=(num_obstacles, 2))

# Lists to store car positions
car_positions = []

# Main loop
running = True
while running:
    screen.fill(BLACK)
    
    # Draw car
    pygame.draw.circle(screen, WHITE, (car_x, car_y), car_radius)
    
    # Draw obstacles
    for pos in obstacle_positions:
        pygame.draw.circle(screen, RED, pos, obstacle_radius)
    
    # Store car position
    car_positions.append((car_x, car_y))
    
    # Calculate direction towards the nearest obstacle
    min_distance = float('inf')
    nearest_obstacle = None
    for pos in obstacle_positions:
        distance = np.linalg.norm(np.array([car_x, car_y]) - np.array(pos))
        if distance < min_distance:
            min_distance = distance
            nearest_obstacle = pos
    direction = np.array(nearest_obstacle) - np.array([car_x, car_y])
    direction_magnitude = np.linalg.norm(direction)
    
    # Randomly change direction
    if direction_magnitude != 0:
        direction = (direction / direction_magnitude)  # Normalize vector
        new_car_x = car_x + int(direction[0] * car_speed)
        new_car_y = car_y + int(direction[1] * car_speed)
        
        # Check if the new position will cause a collision with the obstacles
        collision = False
        for pos in obstacle_positions:
            if np.linalg.norm(np.array(pos) - np.array([new_car_x, new_car_y])) < (car_radius + obstacle_radius):
                collision = True
                break
        
        if not collision:
            car_x = new_car_x
            car_y = new_car_y
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()

pygame.quit()

# Plot the path of the car
car_positions = np.array(car_positions)
plt.figure()
plt.plot(car_positions[:, 0], car_positions[:, 1], color='blue')
plt.scatter(car_positions[0, 0], car_positions[0, 1], color='red', label='Start')
plt.scatter(car_positions[-1, 0], car_positions[-1, 1], color='green', label='End')
plt.title('Path of the Car Avoiding Obstacles')
plt.xlabel('X position')
plt.ylabel('Y position')
plt.legend()
plt.show()
