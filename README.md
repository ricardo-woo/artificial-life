# Artificial Life: An Evolutionary Simulation

Welcome to this artificial life simulation built using Python and Pygame. This project is a virtual ecosystem where organisms rely on neural networks to navigate, survive and evolve over time. 

The world is divided into two distinct species, the predators and prey. Because each species has its own unique genome and neural network, you get to watch entirely different survival strategies emerge through evolution.

## How the ecosystem works

The simulation takes place in a continuous 2D environment populated by food, prey and predators. 

Every creature here operates based on a personal genome that dictates its physical traits, paired with a neural network that acts as its brain. During each update cycle, an organism scans its surroundings by casting visual rays. It takes what it sees, translates that into numerical data and feeds it into its neural network. The network then decides two things: how fast to move, and how much to turn.

Moving and simply existing costs energy, which can only be replenished by eating. Once an organism lives long enough and hoards enough energy, it can reproduce. The offspring gets a copy of its parent's genome, usually with a few random mutations. 

To keep the simulation running smoothly, we cap the population size for each species by culling the weakest links when it gets too crowded.

---

## The organisms / entities

Everything stems from a base `Organism` class. This gives every creature a set of core attributes. It also houses the neural network, genome and ray casting sensors. 

The physical traits aren't hardcoded, they are drawn directly from the genome, meaning evolution shapes both the body and the mind.

### Prey
Prey's main goal is finding food and staying alive. They have a wide 200° field of view and use their ray sensors to detect food, obstacles, their peers and approaching predators. To help them survive, they reach reproductive age a bit earlier than the baseline organism settings.

### Predators
Predators share the same genetic building blocks but have entirely different habits. They have a narrower, more focused 120° field of view. Instead of scanning the grid for food, their sensors are tuned to detect prey, obstacles, and other predators. 

To actually have a meal, a predator has to catch a prey inside its 120° attack angle. If the attack succeeds, the prey dies and the predator absorbs its remaining energy.

---

## How the genome works

An organism's genome dictates everything about it. It stores physical traits alongside its behavioral traits. 

When a creature is spawned, its physical traits are randomized within set limits. When it reproduces, its whole genome is passed down. Because evolution tweaks both the physical and the neurological, you'll see changes in both what the creatures look like and how they behave.

## Neural networks

Each organism is driven by a simple neural network made up of an input layer, a hidden layer and an output layer. 

The neurons calculate a weighted sum of their inputs and pass it through a standard hyperbolic tangent (tanh) activation function. This squashes the neuron outputs to a value between `-1` and `1`. 

These brains aren't trained using traditional machine learning methods like backpropagation. Instead, they learn purely through Darwinian evolution weights and biases are inherited and mutated generation after generation.

### How they see and think
The network makes decisions based on a stream of inputs. First, it takes in the flattened data from the organism's ray sensors. Then, it mixes in three global inputs:
1. Current energy
2. How long it's been since it last saw food
3. An exploration noise signal 

Predators only use the exploration signal if they haven't spotted a prey.

Based on all this, the network spits out two outputs:
1. Turn: Scaled by the organism's max turn speed to dictate steering.
2. Movement: Converted from a `[-1, 1]` range to a `[0, 1]` range, then multiplied by the organism's max speed. 

### Ray sensors
To perceive the world, organisms cast a configurable number of rays spread evenly across their field of view. 

It calculates if a ray intersects with an object's radius, finding the exact distance to the closest obstacle, food, or creature. 

The network receives this as a normalized distance (`distance / vision`) and an encoded category:
* Food: `[1, 0, 0, 0]`
* Obstacle: `[0, 1, 0, 0]`
* Prey: `[0, 0, 1, 0]`
* Predator: `[0, 0, 0, 1]`

If a ray hits nothing, it just returns all zeros.

---

## Reproduction and mutation

Once an organism is old enough and has enough energy, it reproduces. This costs the parent some energy, and a new offspring spawns nearby. 

About 10% of the time, the offspring is an exact clone. The rest of the time, the genome mutates:
* Physical traits shift by a small random value.
* Neural network weights and biases each have a chance to mutate by a configured strength.

This slow accumulation of tiny changes is what drives the evolutionary behavior of the ecosystem.

---

## Optimizations & Math

* Spatial Partitioning: The map is divided into a grid. Organisms only check for objects in the specific grid cells they overlap with, keeping performance snappy even with large populations.
* Exploration Noise (Ornstein-Uhlenbeck): When an organism can't see anything useful, it relies on an exploration signal to wander around. Instead of giving random noise, the simulation uses an Ornstein-Uhlenbeck process. This creates a drifting random value, resulting in natural looking wandering rather than erratic twitching.
* Poisson Disk Sampling: When generating static objects like bushes, purely random placement often results in ugly clusters and empty spaces. Poisson disk sampling solves this by ensuring every generated point maintains a minimum distance from the others, creating a natural evenly distributed landscape.
