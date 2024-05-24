import pygame
from pygame.locals import *
import random
import os

# Initialize Pygame
pygame.init()

# Initialize the mixer for background and crash sounds
pygame.mixer.init()

# Load the background sound
background_sound = pygame.mixer.Sound("C:/Users/KIIT0001/Downloads/doom-2-1036-2-1429.mp3")
background_sound.play(-1)  # -1 means the sound will loop indefinitely

# Load the crash sound
crash_sound = pygame.mixer.Sound("C:/Users/KIIT0001/Downloads/TunePocket-Impact-With-Glass-Debris-Preview.mp3")

# Load the crash explosion image
crash_image = pygame.image.load("C:/Users/KIIT0001/Documents/pngtree-crash-comic-explosion-speech-pop-bubble-vector-png-image_1197095.jpg")

# Screen dimensions and setup
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Bisu ka car")

# Color definitions
gray = (100, 100, 100)
green = (0, 255, 0)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)
orange = (255,100,10)

# Game variables
gameover = False
speed = 2
score = 0

# Marker dimensions
marker_width = 10
marker_height = 50

# Road and lane definitions
road_width = 300
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# Lanes positions (dividing the road into 3 equal lanes)
lane_width = road_width // 3
left_lane_center = 100 + lane_width // 2
center_lane_center = 100 + lane_width + lane_width // 2
right_lane_center = 100 + 2 * lane_width + lane_width // 2

# Define the lanes list
lanes = [left_lane_center, center_lane_center, right_lane_center]

lane_marker_move_y = 0

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Scale the image down so that it fits in the lane
        image_scale = 45 / image.get_rect().width
        new_width = int(image.get_rect().width * image_scale)
        new_height = int(image.get_rect().height * image_scale)
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load("C:/Users/KIIT0001/Documents/new car.png").convert_alpha()
        super().__init__(image, x, y)

# Player car coordinates
player_x = 250
player_y = 400

# Create player car
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Load the obstacle vehicles
image_filenames = [
    "gray-pickup-truck-white-background-view-top-passenger-body-automobile-car-121750749.jpg",
    "2d-car-game-free-racing-formula-one-auto-racing-race-car.jpg",
    "cargo-van-transparent-background-3d-rendering-illustration_494250-61690.jpg",
    "png-transparent-taxi-car-simulator-3d-dodge-sprite-sprite-s-rectangle-car-video-game-thumbnail.png",
    "bus-top-view-clip-art-bus-icon-top-view-11562896756ifkgek2ydy.png",
    "pickup-vehicle_1308-83338.jpg"
]

# Directory where the images are stored
directory = "C:/Users/KIIT0001/Documents/"

# List to store loaded images
vehicle_images = []

# Load each image and append to the list
for image_filename in image_filenames:
    # Construct the full path using os.path.join
    full_path = os.path.join(directory, image_filename)
    print(f"Loading image: {full_path}")  # Debug print
    try:
        # Load the image with alpha transparency
        image = pygame.image.load(full_path).convert_alpha()
        # Append the image to the list
        vehicle_images.append(image)
    except pygame.error as e:
        print(f"Failed to load image {image_filename}: {e}")

vehicle_group = pygame.sprite.Group()

# Clock setup
clock = pygame.time.Clock()
fps = 120

# Main game loop
running = True
while running:
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # Keys to move the car left or right
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane_center:
                player.rect.x -= lane_width
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane_center:
                player.rect.x += lane_width

    screen.fill(green)
    pygame.draw.rect(screen, gray, road)
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0

    # Draw lane markers
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (100 + lane_width - marker_width // 2, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (100 + 2 * lane_width - marker_width // 2, y + lane_marker_move_y, marker_width, marker_height))
     
    # Draw player's car
    player_group.draw(screen)

    # Add vehicles
    if len(vehicle_group) < 2:
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, -image.get_height())
            vehicle_group.add(vehicle)

    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        if vehicle.rect.top >= height:
            vehicle.kill()
            score += 1
            if score > 0 and score % 5 == 0:
                speed += 1

    # Check for collisions
    collision = pygame.sprite.spritecollide(player, vehicle_group, True)
    if collision:
        gameover = True
        # Play the crash sound
        crash_sound.play()
        # Scale the crash image to fit the player's car
        crash_image_scaled = pygame.transform.scale(crash_image, (player.rect.width, player.rect.height))
        # Get the collision position and draw the crash explosion image
        screen.blit(crash_image_scaled, (player.rect.x, player.rect.y))
        pygame.display.update()
        pygame.time.wait(2000)

    # Draw the vehicles
    vehicle_group.draw(screen)

    # Display score
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'Score: {score}', True, red)
    screen.blit(text, (10, 10))

    if gameover:
        text = font.render('Tama gan re kie gadi chaleithila?', True, orange)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(2000)
        running = False

    pygame.display.update()

pygame.quit()
