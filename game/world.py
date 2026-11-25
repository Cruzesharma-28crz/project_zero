"""Static isometric arena cached once."""
import pygame
from .settings import TILE_W,TILE_H,WORLD_COLS,WORLD_ROWS

class World:
    def __init__(self):
        self.width=(WORLD_COLS+WORLD_ROWS)*TILE_W//2+TILE_W
        self.height=(WORLD_COLS+WORLD_ROWS)*TILE_H//2+TILE_H
        self.surface=pygame.Surface((self.width,self.height)).convert()
        self.surface.fill((12,18,27))
        self.origin_x=WORLD_ROWS*TILE_W//2
        self.origin_y=TILE_H
        self._build()
    def _build(self):
        for row in range(WORLD_ROWS):
            for col in range(WORLD_COLS):
                x=self.origin_x+(col-row)*TILE_W//2
                y=self.origin_y+(col+row)*TILE_H//2
                points=[(x,y),(x+TILE_W//2,y+TILE_H//2),(x,y+TILE_H),(x-TILE_W//2,y+TILE_H//2)]
                color=(24,36,47) if (col+row)%2 else (27,40,51)
                pygame.draw.polygon(self.surface,color,points)
                if col%4==0 and row%4==0:
                    pygame.draw.line(self.surface,(34,52,64),(x-9,y+16),(x+9,y+16),1)
    def project(self,x,y):
        return self.origin_x+(x-y)*0.5,self.origin_y+(x+y)*0.25
    def screen_position(self,x,y,camera,center):
        px,py=self.project(x,y); cx,cy=self.project(camera.x,camera.y)
        return center[0]+px-cx,center[1]+py-cy
    def draw(self,target,camera,center):
        cx,cy=self.project(camera.x,camera.y)
        target.blit(self.surface,(int(center[0]-cx),int(center[1]-cy)))
