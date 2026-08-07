# Contributing

Thanks for your interest in contributing to Artificial Life!

## Getting Started

1. Fork the repository.
2. Create a branch for your changes.
3. Make your changes and test them.
4. Open a pull request with a short description of what you changed and why.

## Branch & Settings Guidelines

* **Do not commit local test values to `settings.py`.** If you adjusted constants (e.g., speed, mutation rates, UI flags) for personal testing, revert them before pushing.
* PRs that modify `settings.py` will only be approved if they:

  1. Add new feature configuration constants required by new code.
  2. Represent an agreed-upon balance pass discussed in an issue first.

### Local Settings

If you frequently experiment with values in `settings.py`, you can tell Git to locally ignore changes to the file:

```bash
git update-index --assume-unchanged settings.py
```

If you later need to make a legitimate change to `settings.py` that should be committed, re-enable tracking:

```bash
git update-index --no-assume-unchanged settings.py
```

This only affects your local Git repository. It does not change the repository or other contributors' settings.

## Pull Requests

Please include:

* What changed
* Why it changed
* How you tested it

For changes affecting evolution, include relevant observations or experiment results when possible.
