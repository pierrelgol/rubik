# Rubik

A Rubik's cube solver.

## Setup

```bash
just setup
```

## Usage

```bash
# Run with default input file (input.txt)
just run

# Run with custom scramble from command line
just run-custom "F R U2 B' L' D'"

# Run with custom input file
just run-custom --input my_scrambles.txt

# Watch mode (auto-restart on file changes)
just watch
```

## Development

```bash
just fmt      # Format code
just check    # Check code style
just test     # Run tests
just clean    # Clean caches
```
