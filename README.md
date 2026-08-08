# Artificial Life

An evolutionary artificial life simulation built with Python and Pygame.

The Organisms live in a 2D world, search for food, manage their energy and evolve over generations. Their behavior is controlled by neural networks whose weights and physical traits mutate between generations.

This project started as a way for me to learn about neural networks, so expect some mistakes. Feedback on the network architecture, mutation logic or really anything are very welcome!

![Simulation](assets/simulation_ss.png)

## Instructions if you want to try it

### Requirements
- Python 3.10+
- Pygame

### Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/ricardo-woo/artificial-life.git
cd artificial-life
pip install -r requirements.txt
```

### How you can tweak the projects parameters

The simulations main parameters can be configured in `settings.py`.

Adjusting `settings.py` allows experiments to be run without changing the core simulation code.

### Running the simulation

```bash
python main.py
```

## How the simulation works at the moment

Each organism has:
* Energy
* Age
* Speed
* Vision
* Radius
* Turning ability
* A neural network

The neural network receives information about the organism environment and produces movement decisions.

Organisms that survive longer and find more food have higher fitness and are more likely to contribute to the next generation.

### Evolution

Physical traits and neural network parameters mutate between generations.

The fitness function currently rewards food consumption, survival and movement:

```python
fitness = (
            self.food_eaten * FITNESS_FOOD_WEIGHT
            + min(self.age, FITNESS_AGE_CAP) / FITNESS_AGE_DIVISOR
        )
```

### Neural Network

Each organism has a small neural network that receives information about its environment and produces movement decisions.

#### Inputs
* Energy
* Food detected
* Distance to closest food
* Sin(angle to closest food)
* Cos(angle to closest food)
* Time since food was detected
* Exploration signal using Ornstein-Uhlenbeck process

#### Outputs
* Turn
* Movement

![Neural Network Architecture](assets/neural_network.svg)

## Project Status

This is an ongoing project. The simulation and evolutionary system are still being developed and tested.
