from src.movement import Movement, Moves, Direction, Rotation
import random


def generate_random_moves(count: int) -> Moves:
    directions = list(Direction)
    rotations = list(Rotation)
    return [Movement(random.choice(directions), random.choice(rotations)) for _ in range(count)]
