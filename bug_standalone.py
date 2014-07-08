import pygame
w,h=800,200
fps=60
pygame.init()
screen = pygame.display.set_mode([w, h])
color=pygame.Color("white")
clock=pygame.time.Clock()
radius=40
x,y=800,100
def get_bbox(x,y):
    left = x - radius
    top = y - radius
    width = radius * 2
    height = radius * 2
    return pygame.Rect((left, top), (width, height))

while True:
    pygame.event.pump()
    old_x=x
    x-=5
    screen.fill(pygame.Color("black"),get_bbox(old_x,y))
    pygame.draw.circle(screen, color, (x, y), radius, 1)
    pygame.display.update([get_bbox(x,y),get_bbox(old_x,y)])
##    pygame.display.flip()
    clock.tick(fps)
##    time_passed=clock.get_time()
##    print(time_passed)
