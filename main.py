from tkinter import *
from math import sqrt
from time import sleep

WIDTH = 1400
HEIGHT = 800

class Planet:
    def __init__(self, canvas, size, mass, color, x, y):
        self.canvas = canvas

        self.size = size
        self.mass = mass
        self.color = color

        self.x = x
        self.y = y

        self.dx = 0
        self.dy = 0

        self.ax = 0
        self.ay = 0

    def draw(self, scale, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt

        x1 = (self.x - self.size) / scale + WIDTH / 2
        y1 = (self.y - self.size) / scale + HEIGHT / 2
        x2 = (self.x + self.size) / scale + WIDTH / 2
        y2 = (self.y + self.size) / scale + HEIGHT / 2

        self.canvas.create_oval(x1, y1, x2, y2, fill=self.color)

    def calculate_acceleration(self, planet):
        G = 6.67 * pow(10, -11)
        dx = planet.x - self.x
        dy = planet.y - self.y
        d = sqrt(dx ** 2 + dy ** 2)

        if d == 0:
            return (0, 0)

        F = G * self.mass * planet.mass / d ** 2

        self.ax += F * dx / (d * self.mass)
        self.ay += F * dy / (d * self.mass)
    
    def update_velocity(self, dt):
        self.dx += self.ax * dt
        self.dy += self.ay * dt

        self.ax = 0
        self.ay = 0

    def set_initial_velocity(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def orbit(self, planet):
        G = 6.67e-11
        M = planet.mass
        r = sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        v = sqrt(G * M / r)

        vec_x = (self.x - planet.x) / r
        vec_y = (self.y - planet.y) / r

        n_x = vec_y * -1
        n_y = vec_x * 1

        n_len = sqrt(n_x ** 2 + n_y ** 2)

        n_x /= n_len
        n_y /= n_len

        self.set_initial_velocity(n_x * v, n_y * v)

class System():
    def __init__(self, canvas):
        self.planets = []
        self.canvas = canvas

    def add(self, planet):
        self.planets.append(planet)

    def update_all(self, dt, scale):
        for planet1 in self.planets:
            for planet2 in self.planets:
                if planet1 != planet2:
                    planet1.calculate_acceleration(planet2)

            planet1.update_velocity(dt)

        self.canvas.delete("all")

        for planet in self.planets:
            planet.draw(scale, dt)

def main():
    window = Tk()
    window.title("Simple Grav Sim")

    canvas = Canvas(window, bg="black", width=WIDTH, height=HEIGHT)
    canvas.pack()

    time = Scale(window, from_=1, to=1_000_000, orient=HORIZONTAL, length=400)
    time.pack()

    scale = Scale(window, to=1, from_=5_000_000, orient=HORIZONTAL, length=400)
    scale.pack()
    scale.set(460_000)

    fps = Scale(window, from_=1, to=1000, orient=HORIZONTAL)
    fps.pack()
    fps.set(75)

    system = System(canvas)

    earth = Planet(canvas, 6_371_000, 5.972e24, "green", 0, 0)
    moon = Planet(canvas, 1_737_400, 7.348e22, "grey", 384_400_000, 80_000_000)
    blue_moon = Planet(canvas, 837_400, 10_000, "blue", 400_000, 80_000_000)

    system.add(earth)
    system.add(moon)
    system.add(blue_moon)

    moon.orbit(earth)
    blue_moon.orbit(earth)

    while True:
        system.update_all(time.get() / fps.get(), scale.get())
        window.update_idletasks()
        window.update()
        sleep(1 / fps.get())


if __name__ == "__main__":
    main()