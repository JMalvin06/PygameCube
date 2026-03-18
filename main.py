import pygame
from pygame import Vector3
from pygame import Vector2
import math

bg_color = (50,50,50)

# Cube face colors 
colors = [(255, 0, 0), (255, 100, 0), 
          (255, 225, 0), (255, 255, 255), 
          (0, 187, 0), (0, 0, 187)]

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen.fill(bg_color)

        # Default cube variables
        self.cube_width = 120
        self.x_rot = math.pi/4
        self.y_rot = math.pi/4
        self.z_rot = 0

        # Mouse input variables
        self.mouse_wheel = 0
        self.last_mouse = (0,0)

        # Rendering variables
        self.polygon_faces = [] # Stores lists of coordinate points
        self.cull_vals = [] # Stores overall polygon z values for z-culling
        self.has_outline = True
        self.outline_color = (0,0,0)
        self.outline_width = 5
    
    def update(self):
        self.screen.fill(bg_color) # clear screen

        half_width = self.cube_width/2 # Simple helper variable

        # Reset polygon data
        self.polygon_faces = [[] for i in range(6)]
        self.cull_vals = [0 for i in range(6)]

        # Create faces
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                # Z faces
                self.register_point(i, j * i, 1, 0)
                self.register_point(i, j * i, -1, 1)

                # X faces
                self.register_point(1, i, i*j, 2)
                self.register_point(-1, i, i*j, 3)

                # Y faces
                self.register_point(i, 1, i*j, 4)
                self.register_point(i, -1, i*j, 5)
        
        for i in range(0, len(self.cull_vals)-1, 2):
            draw_face = i if self.cull_vals[i] > self.cull_vals[i+1] else i+1
            pygame.draw.polygon(self.screen, colors[draw_face], self.polygon_faces[draw_face])
            if self.has_outline: 
                scaled_width = int(self.outline_width * (self.cube_width/120)) if int(self.outline_width * (self.cube_width/120)) > 3 else 3
                pygame.draw.polygon(self.screen, self.outline_color, self.polygon_faces[draw_face],scaled_width)
        
        self.process_input()

       

    def process_input(self):
        pygame.mouse.get_pos()[0]

        if pygame.mouse.get_pressed()[0]:
            if self.last_mouse == (0,0):
                self.last_mouse = pygame.mouse.get_pos()
            delta_mouse = (self.last_mouse[0] - pygame.mouse.get_pos()[0], self.last_mouse[1] - pygame.mouse.get_pos()[1])
            self.y_rot -= delta_mouse[0] / 50
            self.x_rot += delta_mouse[1] / 50
            self.last_mouse = pygame.mouse.get_pos()
        elif self.last_mouse != (0,0):
            self.last_mouse = (0,0)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP]:
            self.x_rot += 0.04
        if pressed_keys[pygame.K_DOWN]:
            self.x_rot -= 0.04

        if pressed_keys[pygame.K_RIGHT]:
            self.y_rot += 0.04
        if pressed_keys[pygame.K_LEFT]:
            self.y_rot -= 0.04
        
        if self.cube_width + self.mouse_wheel * 6 > 0:
            self.cube_width += self.mouse_wheel * 6
        self.mouse_wheel = 0

    def register_point(self, i: int, j: int, k: int, id: int):
        coords = Vector3(i,j,k)
        face_point = Vector3(self.rotate_x(coords),self.rotate_y(coords),self.rotate_z(coords)) * self.cube_width/2
        self.polygon_faces[id].append((int(face_point.x + self.screen.get_width()/2), int(face_point.y + self.screen.get_height()/2)))
        self.cull_vals[id] += face_point.z

    def rotate_x(self, coords: Vector3):
        return coords.x*math.cos(self.z_rot)*math.cos(self.y_rot) + coords.y*(math.cos(self.z_rot)*math.sin(self.y_rot)*math.sin(self.x_rot) - math.sin(self.z_rot)*math.cos(self.x_rot)) + coords.z*(math.sin(self.z_rot)*math.sin(self.x_rot) + math.cos(self.z_rot)*math.sin(self.y_rot)*math.cos(self.x_rot))

    def rotate_y(self, coords: Vector3):
        return coords.x*math.sin(self.z_rot)*math.cos(self.y_rot) + coords.y*(math.cos(self.z_rot)*math.cos(self.x_rot) + math.sin(self.z_rot)*math.sin(self.y_rot)*math.sin(self.x_rot)) + coords.z*(-math.cos(self.z_rot)*math.sin(self.x_rot) + math.sin(self.z_rot)*math.sin(self.y_rot)*math.cos(self.x_rot))

    def rotate_z(self, coords: Vector3):
        return coords.x*(-math.sin(self.y_rot)) + coords.y*math.cos(self.y_rot)*math.sin(self.x_rot) + coords.z*math.cos(self.y_rot)*math.cos(self.x_rot)
        
    



if __name__ == "__main__":
    pygame.init()
    game = Game(pygame.display.set_mode((800,600), pygame.RESIZABLE))



clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.MOUSEWHEEL:
            game.mouse_wheel = event.y 
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o: game.has_outline = not game.has_outline
    pygame.display.set_caption(f'{clock.get_fps() :.1f}')
    pygame.display.flip()
    game.update()
    clock.tick(60)