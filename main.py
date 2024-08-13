from tkinter import *
from math import sqrt
from time import sleep

WIDTH = 900
HEIGHT = 600

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

        x1 = (self.x + self.size) / scale + WIDTH / 2
        y1 = (self.y + self.size) / scale + HEIGHT / 2
        x2 = (self.x + self.size * 3) / scale + WIDTH / 2
        y2 = (self.y + self.size * 3) / scale + HEIGHT / 2

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

        print(r)

        v = sqrt(G * M / r)

        self.set_initial_velocity(0, v)

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

    fps_limit = 75

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

    earth = Planet(canvas, 6371000, 5.972e24, "green", 4_000_000, 30_000_000)
    moon = Planet(canvas, 1737400, 7.348e22, "grey", 4_000_000 + 384_400_000, 30_000_000)
    iss = Planet(canvas, 1737400, 400_000, "grey", 4_000_000 + 408_000, 30_000_000)

    system.add(earth)
    system.add(moon)
    system.add(iss)

    iss.orbit(earth)
    moon.orbit(earth)

    while True:
        system.update_all(time.get() / fps_limit, scale.get())
        window.update_idletasks()
        window.update()
        sleep(1 / fps_limit)


if __name__ == "__main__":
    main()