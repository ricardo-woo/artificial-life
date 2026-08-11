# Contributing

Thanks for your interest in contributing to Artificial Life!

## Setting Up the Project

### Requirements

* Python 3.10 or newer

### Installation

Clone the repository:

```bash
git clone https://github.com/ricardo-woo/artificial-life.git
cd artificial-life
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

### Running the Simulation

Once the dependencies are installed, run:

```bash
python main.py
```

### Making Changes

Most simulation parameters can be adjusted in `settings.py`. If you're experimenting with the simulation, changing these values is preferable to modifying the core logic when possible.

For larger changes, try to keep different systems separated into their existing modules. For example:

* `organism.py` — common organism behavior
* `prey.py` — prey-specific behavior
* `predator.py` — predator-specific behavior
* `Population.py` — population and reproduction management
* `spatialgrid.py` — spatial partitioning
* `Brain/` — neural network and genome logic
* `poissondisk.py` — Poisson disk sampling

### Pull Requests

When submitting a pull request:

1. Explain what you changed.
2. Explain why the change was needed.
3. Test the simulation before submitting.
4. Keep changes focused when possible.
5. Include any relevant observations from experiments or simulations.

For changes to the neural network, evolution, reproduction, or sensing systems, describing the reasoning behind the change is especially helpful.
