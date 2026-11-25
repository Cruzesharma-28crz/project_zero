"""Lightweight entities with fixed-size slots."""
import math

class Projectile:
    __slots__ = ("x", "y", "vx", "vy", "life", "active", "team", "damage")
    def __init__(self):
        self.x=self.y=self.vx=self.vy=0.0; self.life=0.0; self.active=False; self.team="player"; self.damage=1
    def launch(self,x,y,vx,vy,team="player",damage=1):
        self.x,self.y,self.vx,self.vy=x,y,vx,vy; self.life=1.8; self.team=team; self.damage=damage; self.active=True
    def update(self,dt):
        self.x+=self.vx*dt; self.y+=self.vy*dt; self.life-=dt
        if self.life<=0: self.active=False

class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "radius", "active", "color")
    def __init__(self):
        self.x=self.y=self.vx=self.vy=0.0; self.life=0.0; self.max_life=0.0; self.radius=2; self.active=False; self.color=(80,220,255)
    def spawn(self,x,y,vx,vy,life,radius,color):
        self.x,self.y,self.vx,self.vy=x,y,vx,vy; self.life=life; self.max_life=life; self.radius=radius; self.color=color; self.active=True
    def update(self,dt):
        self.x+=self.vx*dt; self.y+=self.vy*dt; self.life-=dt
        if self.life<=0: self.active=False

class Player:
    def __init__(self):
        self.x=0.0; self.y=0.0; self.radius=13; self.speed=190.0; self.hp=100; self.max_hp=100; self.cooldown=0.0; self.pulse_cd=0.0; self.angle=0.0; self.invuln=0.0
    def update(self,dt,move):
        length=math.hypot(move[0],move[1])
        if length>0:
            self.x+=move[0]/length*self.speed*dt; self.y+=move[1]/length*self.speed*dt
        self.cooldown=max(0.0,self.cooldown-dt); self.pulse_cd=max(0.0,self.pulse_cd-dt); self.invuln=max(0.0,self.invuln-dt)

class Drone:
    def __init__(self,x,y):
        self.x=float(x); self.y=float(y); self.hp=3; self.radius=12; self.speed=62.0; self.fire_cd=0.7; self.active=True; self.phase=0.0
    def update(self,dt,player,fire_callback):
        dx,dy=player.x-self.x,player.y-self.y; dist=max(1.0,math.hypot(dx,dy)); self.phase+=dt
        if dist>105:
            self.x+=dx/dist*self.speed*dt; self.y+=dy/dist*self.speed*dt
        self.fire_cd-=dt
        if self.fire_cd<=0 and dist<390:
            fire_callback(self.x,self.y,dx/dist,dy/dist); self.fire_cd=1.35

class Camera:
    def __init__(self): self.x=0.0; self.y=0.0
    def follow(self,target,dt):
        k=min(1.0,dt*7.0); self.x+=(target.x-self.x)*k; self.y+=(target.y-self.y)*k

def distance_sq(ax,ay,bx,by):
    dx=ax-bx; dy=ay-by; return dx*dx+dy*dy
