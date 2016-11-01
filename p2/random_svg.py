#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

def random_color():
    return random.sample([
        "blue",
        "lightblue",
        "cyan",
        "teal",
        "orange",
        "red",
        "yellow",
        "green",
        "aqua",
        "fuchsia",
        "gray",
        "silver",
        "black"
    ], 1)[0]

def random_rect():
    return """
    <rect x="{}", y="{}", height="{}", width="{}" fill="{}" />
    """.format(
        random.uniform(0, 800),
        random.uniform(0, 600),
        random.uniform(0, 600),
        random.uniform(0, 800),
        random_color()
    )

def random_circle():
    return """
    <circle r="{}", cx="{}", cy="{}", fill="{}" />
    """.format(
        random.uniform(0, 120),
        random.uniform(0, 800),
        random.uniform(0, 600),
        random_color()
    )

def random_svg():
    svg = """
<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    """
    num_objects = random.randint(2, 100)
    shapes = [
        random_rect,
        random_circle
    ]
    for _ in range(num_objects):
        svg += random.sample(shapes, 1)[0]()

    svg += "</svg>"
    return svg

if __name__ == "__main__":
    with open("random_svg.svg", "w") as f:
        f.write(random_svg())
