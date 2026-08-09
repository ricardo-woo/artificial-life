import os
import random
import sys
import time
import pygame

from Brain.Genome import Genome
from camera import Camera
from food import Food
from bush import Bush
from organism import Organism
from Population import Population
from SaveManager import SaveManager
from spatialgrid import SpatialGrid
from settings import (
    BACKGROUND_COLOR,
    FAST_FORWARD_SPEED,
    FOOD_COUNT,
    FOOD_ENERGY_VAL,
    SPATIAL_CELL_SIZE,
    FOOD_RESPAWN_INTERVAL,
    FPS,
    GENERATION_END_WAIT_TIME,
    HEIGHT,
    KEY_FAST_FORWARD,
    KEY_FOLLOW_ORGANISM,
    KEY_NEXT_GENERATION,
    KEY_PAUSE_SELECTION,
    MAX_ENERGY,
    BUSH_COUNT,
    SAVE_INTERVAL_MS,
    WIDTH,
    WORLD_HEIGHT,
    WORLD_WIDTH,
    SAVE_FILE_PATH,
    KEY_DEBUG,
)
from Simulation.SimulationClock import SimulationClock
from ui import UIManager

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Artificial Life")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)


save_manager = SaveManager()
save_timer = 0
population = Population()
camera = Camera()
ui_manager = UIManager(font)
generation = 1
waiting_for_next_gen = False
top_organism_snapshot = []
generation_end_time = 0
food_grid = SpatialGrid(SPATIAL_CELL_SIZE)
bush_grid = SpatialGrid(SPATIAL_CELL_SIZE)

simulation_clock = SimulationClock()
generation_simulation_time = 0
is_fast_forwarding = False

organisms = []

if os.path.exists(SAVE_FILE_PATH):
    organisms, generation, generation_simulation_time = save_manager.load_game()
else:
    generation = 1
    organisms = population.create_initial_population(organisms)

food_respawn_timer = 0
foods = []
bushes = []

for _ in range(BUSH_COUNT):
    bush = Bush(random.uniform(0, WORLD_WIDTH), random.uniform(0, WORLD_HEIGHT))
    bushes.append(bush)

bush_grid.clear()

for _ in range(FOOD_COUNT):
    food = Food(bushes)
    foods.append(food)

food_grid.clear()

for food in foods:
    food_grid.insert(food, food.x, food.y)

for bush in bushes:
    bush_grid.insert(bush, bush.x, bush.y)

selected_organism = None
running = True
debug_open = False

while running:
    save_timer += clock.get_time()

    if save_timer > SAVE_INTERVAL_MS:
        save_manager.save_game(organisms, generation, generation_simulation_time)
        save_timer = 0

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_manager.save_game(organisms, generation, generation_simulation_time)
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == KEY_DEBUG:
                debug_open = not debug_open
            if waiting_for_next_gen:
                if event.key == KEY_NEXT_GENERATION:
                    organisms = population.next_generation(organisms)
                    generation += 1
                    foods = []
                    food_grid.clear()

                    for _ in range(FOOD_COUNT):
                        new_food = Food(bushes)
                        foods.append(new_food)
                        food_grid.insert(new_food, new_food.x, new_food.y)

                    waiting_for_next_gen = False
                    generation_simulation_time = 0
                    food_respawn_timer = 0
            else:
                if event.key == KEY_PAUSE_SELECTION:
                    selected_organism = None
                    camera.following = None

                elif event.key == KEY_FOLLOW_ORGANISM:
                    if selected_organism is not None:
                        camera.following = selected_organism

                elif event.key == KEY_FAST_FORWARD:
                    # Toggle fast-forward state
                    is_fast_forwarding = not is_fast_forwarding
                    simulation_clock.speed = (
                        FAST_FORWARD_SPEED if is_fast_forwarding else 1
                    )

        elif not waiting_for_next_gen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    camera.start_drag()
                elif event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    world_x, world_y = camera.screen_to_world(mouse_x, mouse_y)
                    selected_organism = None
                    for organism in organisms:
                        if organism.contains_point(world_x, world_y):
                            selected_organism = organism
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    camera.stop_drag()
            elif event.type == pygame.MOUSEMOTION:
                camera.drag()
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    camera.zoom_in()
                elif event.y < 0:
                    camera.zoom_out()

    if waiting_for_next_gen:
        if time.time() - generation_end_time >= GENERATION_END_WAIT_TIME:
            organisms = population.next_generation(organisms)
            generation += 1
            foods = []
            food_grid.clear()
            for _ in range(FOOD_COUNT):
                new_food = Food(bushes)
                foods.append(new_food)
                food_grid.insert(new_food, new_food.x, new_food.y)
            waiting_for_next_gen = False
            generation_simulation_time = 0
            food_respawn_timer = 0

    if not waiting_for_next_gen:
        dt = simulation_clock.update()
        generation_simulation_time += dt
    else:
        dt = 0

    if not waiting_for_next_gen:
        for organism in organisms:
            if organism.is_dead():
                continue

            organism.update(food_grid, dt)

            nearby_food = food_grid.query(organism.x, organism.y, organism.vision)

            for food in nearby_food:

                if food not in foods:
                    continue

                if organism.eat(food):
                    organism.food_eaten += 1
                    organism.energy = min(MAX_ENERGY, organism.energy + FOOD_ENERGY_VAL)
                    organism.time_since_food = 0
                    foods.remove(food)
                    food_grid.remove(food, food.x, food.y)
                    break

        food_respawn_timer += dt
        while food_respawn_timer >= FOOD_RESPAWN_INTERVAL and len(foods) < FOOD_COUNT:
            new_food = Food(bushes)
            foods.append(new_food)
            food_grid.insert(new_food, new_food.x, new_food.y)
            food_respawn_timer -= FOOD_RESPAWN_INTERVAL

        if selected_organism is not None:
            if selected_organism not in organisms:
                selected_organism = None
                camera.following = None

        camera.update()

        # Check if generation has ended
        if all(organism.is_dead() for organism in organisms):
            organisms.sort(key=lambda organism: organism.fitness, reverse=True)
            top_organism_snapshot = list(organisms)
            waiting_for_next_gen = True
            generation_end_time = time.time()
            selected_organism = None
            camera.following = None
            save_manager.log_generation_to_csv(
                generation, generation_simulation_time, organisms
            )

    current_generation_time = generation_simulation_time

    # RENDERING
    screen.fill(BACKGROUND_COLOR)

    ui_manager.draw_world_border(screen, camera, WORLD_WIDTH, WORLD_HEIGHT)

    for food in foods:
        food.draw(screen, camera)

    for bush in bushes:
        bush.draw(screen, camera)

    for organism in organisms:
        organism.draw(screen, camera)

    ui_manager.draw_selection_and_hud(screen, camera, selected_organism, food_grid)

    if waiting_for_next_gen:
        ui_manager.draw_leaderboard(screen, top_organism_snapshot, generation)

    if debug_open:
        leaderboard_rows = ui_manager.draw_debug(
            screen,
            organisms,
            foods,
            generation,
            generation_simulation_time,
            clock.get_fps(),
        )

    pygame.display.flip()
    clock.tick(FPS)
