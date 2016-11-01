#!/usr/bin/env python

from PIL import Image
from io import StringIO, BytesIO
import base64

def mandelbrot_base64(width, initial, final):
    height = int(float(width)/(final[0] - initial[0]) * (initial[1] - final[1]))
    mandel = Image.new("RGBA", (width, height), "white")
    output = BytesIO()
    mandelbrot(mandel)
    mandel.save(output, "PNG")
    contents = output.getvalue()
    output.close()
    return base64.b64encode(contents).decode("utf-8")

def mandelbrot(image, initial = (-2.5, 1), final = (1, -1)):
    width, height = image.size
    pixels = image.load()
    for i in range(width):
        x0 = float(final[0]-initial[0])*i/width + initial[0]
        for j in range(height):
            # Implementation from pseudo-code in wikipedia
            y0 = float(initial[1] - final[1])*j/height - initial[1]
            x, y = 0, 0
            iteration = 0
            max_iters = 10

            while x*x + y*y < 2*2 and iteration < max_iters:
                x, y = x*x - y*y + x0, 2*x*y + y0
                iteration += 1

            lightness = int(iteration*255.0/max_iters)
            pixels[i,j] = (int(lightness*i/width), int(lightness*(i+j)/(width+height)/2), int(lightness*j/height), 255)

if __name__ == "__main__":
    mandel = Image.new("RGBA", (3500, 2000), "white")
    # pixels = mandel.load()
    mandelbrot(mandel)
    mandel.save("7_mandel.png")
