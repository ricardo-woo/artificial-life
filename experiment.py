import time
import random

from Population import Population
from food import Food
from settings import WORLD_WIDTH, WORLD_HEIGHT

FOOD_COUNT = 200
STEPS = 10_000
DT = 1 / 60

print("Creating population...")

population = Population()
organisms = population.create_initial_population([])

print(f"Organisms created: {len(organisms)}")

foods = [
    Food(random.uniform(0, WORLD_WIDTH), random.uniform(0, WORLD_HEIGHT))
    for _ in range(FOOD_COUNT)
]

print("Starting benchmark...")

start = time.perf_counter()

for step in range(STEPS):

    for organism in organisms:

        if not organism.is_dead():
            organism.update(foods, DT)

        for food in foods[:]:

            if organism.eat(food):

                organism.food_eaten += 1
                organism.energy = min(100, organism.energy + 30)

                foods.remove(food)
                break

    # Progress every 1,000 steps
    if step % 1000 == 0:
        print(f"Step {step}/{STEPS}")

elapsed = time.perf_counter() - start

steps_per_second = STEPS / elapsed
simulated_seconds_per_second = steps_per_second * DT

print()
print("==============================")
print("BENCHMARK COMPLETE")
print("==============================")
print(f"Steps: {STEPS}")
print(f"Real time: {elapsed:.2f} seconds")
print(f"Steps/sec: {steps_per_second:.0f}")
print(f"Simulated seconds/sec: {simulated_seconds_per_second:.2f}")
print("==============================")

input("Press ENTER to exit...")
