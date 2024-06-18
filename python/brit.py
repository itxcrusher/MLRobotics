import pygame
import numpy as np
import numpy as np

class BraitenbergVehicle:
    def __init__(self, num_sensors, num_actuators):
        self.num_sensors = num_sensors
        self.num_actuators = num_actuators
        self.sensors = np.zeros(num_sensors)
        self.actuators = np.zeros(num_actuators)
        self.weights = np.random.rand(num_sensors, num_actuators)  # Initialize random synaptic weights
        self.threshold = 0.5  # Threshold for activating actuators
        self.learning_rate = 0.1  # Learning rate for synaptic homeostasis

    def sense(self, sensor_data):
        self.sensors = sensor_data

    def calculate_output(self):
        # Calculate activation levels of actuators based on sensor inputs and synaptic weights
        activations = np.dot(self.sensors, self.weights)
        # Apply threshold to determine actuator activation
        self.actuators = np.where(activations > self.threshold, 1, -1)

    def apply_homeostasis(self):
        # Homeostasis: Adjust synaptic weights to maintain stable behavior
        # Calculate mean activation for each actuator
        mean_activations = np.mean(self.actuators, axis=0)
        # Update weights based on the difference between actual and desired mean activations
        self.weights += self.learning_rate * (mean_activations - self.threshold) * np.transpose(self.sensors)

# Example usage
num_sensors = 2
num_actuators = 2
vehicle = BraitenbergVehicle(num_sensors, num_actuators)

# Simulate sensor inputs
sensor_data = np.array([0.8, 0.2])  # Example sensor inputs

# Main loop
for _ in range(100):
    vehicle.sense(sensor_data)
    vehicle.calculate_output()
    vehicle.apply_homeostasis()
    print("Sensor data:", sensor_data)
    print("Actuator output:", vehicle.actuators)

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Braitenberg Car Simulation")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define car parameters
car_width, car_height = 60, 30
car_speed = 3
car_turn_angle = np.pi / 30  # Angle by which car turns

# Define sensor parameters
sensor_length = 100
sensor_width = 5

# Define neuron parameters
num_neurons = 10
neuron_radius = 20

# Define initial car position and angle
car_x, car_y = screen_width // 2, screen_height // 2
car_angle = 0

# Generate random positions for neurons
neuron_positions = np.random.rand(num_neurons, 2) * [screen_width, screen_height]

# Main loop
running = True
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw neurons
    for neuron_pos in neuron_positions:
        pygame.draw.circle(screen, WHITE, (int(neuron_pos[0]), int(neuron_pos[1])), neuron_radius)

    # Calculate sensor endpoints
    sensor1_x = car_x + sensor_length * np.cos(car_angle - np.pi / 4)
    sensor1_y = car_y + sensor_length * np.sin(car_angle - np.pi / 4)
    sensor2_x = car_x + sensor_length * np.cos(car_angle + np.pi / 4)
    sensor2_y = car_y + sensor_length * np.sin(car_angle + np.pi / 4)

    # Draw sensors
    pygame.draw.line(screen, WHITE, (car_x, car_y), (sensor1_x, sensor1_y), sensor_width)
    pygame.draw.line(screen, WHITE, (car_x, car_y), (sensor2_x, sensor2_y), sensor_width)

    # Draw sensor endpoints
    pygame.draw.circle(screen, WHITE, (int(sensor1_x), int(sensor1_y)), 3)
    pygame.draw.circle(screen, WHITE, (int(sensor2_x), int(sensor2_y)), 3)

    # Check sensor collisions with neurons
    sensor_collisions = [False, False]
    for i, sensor in enumerate([(sensor1_x, sensor1_y), (sensor2_x, sensor2_y)]):
        for neuron_pos in neuron_positions:
            distance = np.linalg.norm(np.array(sensor) - neuron_pos)
            if distance < neuron_radius:
                sensor_collisions[i] = True

    # Adjust car angle based on sensor collisions
    if sensor_collisions[0] and not sensor_collisions[1]:  # Left sensor collision
        car_angle += car_turn_angle
    elif sensor_collisions[1] and not sensor_collisions[0]:  # Right sensor collision
        car_angle -= car_turn_angle
    elif sensor_collisions[0] and sensor_collisions[1]:  # Both sensors collided
        car_angle += np.pi / 2  # Rotate 90 degrees

    # Move the car forward
    car_x += car_speed * np.cos(car_angle)
    car_y += car_speed * np.sin(car_angle)

    # Check bounds
    if car_x < 0:
        car_x = screen_width
    elif car_x > screen_width:
        car_x = 0
    if car_y < 0:
        car_y = screen_height
    elif car_y > screen_height:
        car_y = 0

    # Draw car
    pygame.draw.rect(screen, RED, (car_x - car_width // 2, car_y - car_height // 2, car_width, car_height))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
