import json
import csv
import os

from Brain.Genome import Genome
from organism import Organism


class SaveManager:
    def __init__(self):
        pass

    def log_generation_to_csv(self, gen, gen_time, organisms_list):

        file_exists = os.path.exists("experiment_log.csv")

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

        with open("experiment_log.csv", mode="a", newline="") as f:

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
                    round(gen_time, 2),
                    round(best_fitness, 2),
                    round(avg_fitness, 2),
                    round(best_speed, 2),
                    round(avg_speed, 2),
                    round(best_vision, 2),
                    round(avg_vision, 2),
                    round(best_age, 2),
                    round(avg_age, 2),
                    best_food,
                    round(avg_food, 2),
                ]
            )

    def save_game(self, organisms, generation, sim_time):
        data = {
            "generation": generation,
            "organisms": [organism.get_data() for organism in organisms],
            "generation_simulation_time": sim_time,
        }

        with open("save.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_game(self):
        with open("save.json", "r") as file:
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
            organism.distance_traveled = organism_data.get("distance_traveled", 0)

            organisms.append(organism)

        return organisms, data["generation"], generation_simulation_time
