"""Small-surface renderer with viewport culling and inexpensive primitives."""
import pygame
from .settings import INTERNAL_WIDTH,INTERNAL_HEIGHT

class Renderer:
    def __init__(self,settings):
        self.settings=settings
        self.canvas=pygame.Surface((INTERNAL_WIDTH,INTERNAL_HEIGHT)).convert()
        self.font=pygame.font.Font(None,18)
        self.big=pygame.font.Font(None,34)
    def resize_window(self,window_size):
        w=max(1,int(INTERNAL_WIDTH*self.settings.render_scale)); h=max(1,int(INTERNAL_HEIGHT*self.settings.render_scale))
        self.low=pygame.Surface((w,h)).convert()
        self.window_size=window_size
    def begin(self): self.canvas.fill((8,13,20))
    def visible(self,pos,pad=30):
        x,y=pos
        return -pad<=x<=INTERNAL_WIDTH+pad and -pad<=y<=INTERNAL_HEIGHT+pad
    def draw_world(self,world,camera): world.draw(self.canvas,camera,(INTERNAL_WIDTH//2,INTERNAL_HEIGHT//2))
    def draw_player(self,player):
        x,y=INTERNAL_WIDTH//2,INTERNAL_HEIGHT//2
        pygame.draw.ellipse(self.canvas,(5,9,14),(x-15,y+7,30,12))
        pygame.draw.circle(self.canvas,(45,205,235),(x,y),13)
        pygame.draw.circle(self.canvas,(170,250,255),(x,y-3),7)
        pygame.draw.line(self.canvas,(230,250,255),(x,y), (x+int(19*__import__('math').cos(player.angle)),y+int(19*__import__('math').sin(player.angle))),4)
    def draw_drone(self,drone,pos):
        if not self.visible(pos): return
        x,y=int(pos[0]),int(pos[1])
        pygame.draw.ellipse(self.canvas,(5,8,13),(x-14,y+6,28,10))
        pygame.draw.circle(self.canvas,(178,68,80),(x,y),11)
        pygame.draw.circle(self.canvas,(255,160,130),(x,y-2),4)
        pygame.draw.circle(self.canvas,(70,20,30),(x,y),11,1)
    def draw_projectile(self,item,pos):
        if self.visible(pos,8): pygame.draw.circle(self.canvas,(255,190,95) if item.team=="player" else (255,75,85),(int(pos[0]),int(pos[1])),3)
    def draw_particle(self,item,pos):
        if self.visible(pos,8):
            fade=max(1,int(item.radius*item.life/max(0.001,item.max_life)))
            pygame.draw.circle(self.canvas,item.color,(int(pos[0]),int(pos[1])),fade)
    def hud(self,player,score,wave,enemy_count,paused=False,game_over=False):
        pygame.draw.rect(self.canvas,(22,31,42),(12,12,156,12),border_radius=4)
        pygame.draw.rect(self.canvas,(55,215,175),(14,14,int(152*player.hp/player.max_hp),8),border_radius=3)
        self.canvas.blit(self.font.render(f"HP {player.hp:03d}",True,(225,240,245)),(14,29))
        self.canvas.blit(self.font.render(f"SCORE {score:05d}   WAVE {wave:02d}   HOSTILES {enemy_count:02d}",True,(190,215,230)),(12,50))
        self.canvas.blit(self.font.render("WASD MOVE  |  MOUSE AIM  |  SPACE FIRE  |  E PULSE  |  F3 PERF",True,(115,145,165)),(12,INTERNAL_HEIGHT-22))
        if paused or game_over:
            shade=pygame.Surface((INTERNAL_WIDTH,INTERNAL_HEIGHT),pygame.SRCALPHA); shade.fill((2,5,10,190)); self.canvas.blit(shade,(0,0))
            title="SIMULATION PAUSED" if paused else "SIGNAL LOST"
            msg="ESC TO RESUME" if paused else "R TO RESTART"
            a=self.big.render(title,True,(220,245,250)); b=self.font.render(msg,True,(135,205,220))
            self.canvas.blit(a,a.get_rect(center=(INTERNAL_WIDTH//2,INTERNAL_HEIGHT//2-10)))
            self.canvas.blit(b,b.get_rect(center=(INTERNAL_WIDTH//2,INTERNAL_HEIGHT//2+22)))
    def present(self,window):
        w,h=window.get_size(); lw,lh=self.low.get_size()
        pygame.transform.scale(self.canvas,(lw,lh),self.low)
        window.fill((0,0,0))
        scaled=pygame.transform.scale(self.low,(w,h))
        window.blit(scaled,(0,0)); pygame.display.flip()
