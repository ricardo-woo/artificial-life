import json
import csv
import os

from Brain.Genome import Genome
from organism import Organism
from settings import SAVE_FILE_PATH, CSV_LOG_PATH, FLOAT_ROUND_PRECISION, JSON_INDENT


class SaveManager:
    def __init__(self):
        pass

    def log_generation_to_csv(self, gen, gen_time, organisms_list):

        file_exists = os.path.exists(CSV_LOG_PATH)

        if organisms_list:

            # Fitness
            total_fitness = sum(org.fitness for org in organisms_list)
            avg_fitness = total_fitness / len(organisms_list)
            best_fitness = organisms_list[0].fitness

            # Speed
            total_speed = sum(org.speed for org in organisms_list)
            avg_speed = total_speed / len(organisms_list)
            best_speed = max(org.speed for org in organisms_list)

            # Vision
            total_vision = sum(org.vision for org in organisms_list)
            avg_vision = total_vision / len(organisms_list)
            best_vision = max(org.vision for org in organisms_list)

            # Age
            total_age = sum(org.age for org in organisms_list)
            avg_age = total_age / len(organisms_list)
            best_age = max(org.age for org in organisms_list)

            # Food eaten
            total_food = sum(org.food_eaten for org in organisms_list)
            avg_food = total_food / len(organisms_list)
            best_food = max(org.food_eaten for org in organisms_list)

        else:

            avg_fitness = 0
            best_fitness = 0

            avg_speed = 0
            best_speed = 0

            avg_vision = 0
            best_vision = 0

            avg_age = 0
            best_age = 0

            avg_food = 0
            best_food = 0

        with open(CSV_LOG_PATH, mode="a", newline="") as f:

            writer = csv.writer(f)

            if not file_exists:

                writer.writerow(
                    [
                        "Generation",
                        "Time Seconds",
                        "Best Fitness",
                        "Avg Fitness",
                        "Best Speed",
                        "Average Speed",
                        "Best Vision",
                        "Average Vision",
                        "Best Age",
                        "Average Age",
                        "Best Food Eaten",
                        "Average Food Eaten",
                    ]
                )

            writer.writerow(
                [
                    gen,
                    round(gen_time, FLOAT_ROUND_PRECISION),
                    round(best_fitness, FLOAT_ROUND_PRECISION),
                    round(avg_fitness, FLOAT_ROUND_PRECISION),
                    round(best_speed, FLOAT_ROUND_PRECISION),
                    round(avg_speed, FLOAT_ROUND_PRECISION),
                    round(best_vision, FLOAT_ROUND_PRECISION),
                    round(avg_vision, FLOAT_ROUND_PRECISION),
                    round(best_age, FLOAT_ROUND_PRECISION),
                    round(avg_age, FLOAT_ROUND_PRECISION),
                    best_food,
                    round(avg_food, FLOAT_ROUND_PRECISION),
                ]
            )

    def save_game(self, organisms, generation, sim_time):
        data = {
            "generation": generation,
            "organisms": [organism.get_data() for organism in organisms],
            "generation_simulation_time": sim_time,
        }

        with open(SAVE_FILE_PATH, "w") as file:
            json.dump(data, file, indent=JSON_INDENT)

    def load_game(self):
        with open(SAVE_FILE_PATH, "r") as file:
            data = json.load(file)

        generation_simulation_time = data.get("generation_simulation_time", 0)

        organisms = []

        for organism_data in data["organisms"]:
            genome = Genome.from_data(organism_data["genome"])

            organism = Organism(organism_data["x"], organism_data["y"], genome)

            organism.energy = organism_data["energy"]
            organism.age = organism_data["age"]
            organism.food_eaten = organism_data["food_eaten"]
            organism.angle = organism_data["angle"]

            # Falls back to the default set in Organism.__init__ for save
            # files created before reproduction tracking existed.
            if "next_reproduction_age" in organism_data:
                organism.next_reproduction_age = organism_data["next_reproduction_age"]

            organisms.append(organism)

        return organisms, data["generation"], generation_simulation_time
