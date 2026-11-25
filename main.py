"""PROJECT ZERO: COMBAT SIMULATION. Run with: python main.py"""
import math
import random
import pygame
from game.settings import Settings, INTERNAL_WIDTH, INTERNAL_HEIGHT, WORLD_COLS, WORLD_ROWS
from game.entities import Player, Drone, Camera, Projectile, Particle, distance_sq
from game.pool import Pool
from game.world import World
from game.renderer import Renderer


def main():
    pygame.init()
    pygame.display.set_caption("PROJECT ZERO | Combat Simulation")
    window=pygame.display.set_mode((960,540),pygame.RESIZABLE)
    clock=pygame.time.Clock()
    settings=Settings(); settings.apply_preset("balanced")
    renderer=Renderer(settings); renderer.resize_window(window.get_size())
    world=World(); player=Player(); camera=Camera()
    player.x=player.y=(WORLD_COLS*32)
    bullets=Pool(Projectile,96); particles=Pool(Particle,120)
    enemies=[]; score=0; wave=1; spawn_left=0; spawn_timer=0.0
    paused=False; game_over=False; running=True; pulse_flash=0.0
    joysticks=[]
    try:
        pygame.joystick.init()
        for i in range(pygame.joystick.get_count()):
            stick=pygame.joystick.Joystick(i); stick.init(); joysticks.append(stick)
    except pygame.error:
        joysticks=[]

    def burst(x,y,count=8,color=(90,220,255)):
        limit={"low":2,"medium":5,"high":9}.get(settings.particles,5)
        for _ in range(min(count,limit)):
            p=particles.acquire()
            if p is None: break
            angle=random.random()*math.tau; speed=random.uniform(35,115)
            p.spawn(x,y,math.cos(angle)*speed,math.sin(angle)*speed,random.uniform(.18,.42),random.randint(2,4),color)

    def enemy_shot(x,y,dx,dy):
        p=bullets.acquire()
        if p: p.launch(x,y,dx*205,dy*205,"enemy",1)

    def reset():
        nonlocal player,camera,enemies,score,wave,spawn_left,spawn_timer,paused,game_over
        player=Player(); player.x=player.y=WORLD_COLS*32; camera=Camera(); enemies.clear()
        for b in bullets.items: b.active=False
        for p in particles.items: p.active=False
        score=0; wave=1; spawn_left=5; spawn_timer=.4; paused=False; game_over=False

    spawn_left=5
    while running:
        dt=min(clock.tick(settings.fps_cap)/1000.0,0.05)
        for event in pygame.event.get():
            if event.type==pygame.QUIT: running=False
            elif event.type==pygame.VIDEORESIZE:
                window=pygame.display.set_mode((max(640,event.w),max(360,event.h)),pygame.RESIZABLE)
                renderer.resize_window(window.get_size())
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE and not game_over: paused=not paused
                elif event.key==pygame.K_F3: settings.show_performance=not settings.show_performance
                elif event.key==pygame.K_1: settings.apply_preset("performance")
                elif event.key==pygame.K_2: settings.apply_preset("balanced")
                elif event.key==pygame.K_3: settings.apply_preset("quality")
                elif event.key==pygame.K_r and game_over: reset()
            elif event.type==pygame.JOYBUTTONDOWN:
                if event.button==7 and not game_over: paused=not paused
                if event.button==3 and not paused and not game_over and player.pulse_cd<=0: pulse_flash=.22; player.pulse_cd=4.0

        if not paused and not game_over:
            keys=pygame.key.get_pressed(); mx=keys[pygame.K_d] or keys[pygame.K_RIGHT]; nx=keys[pygame.K_a] or keys[pygame.K_LEFT]
            my=keys[pygame.K_s] or keys[pygame.K_DOWN]; ny=keys[pygame.K_w] or keys[pygame.K_UP]
            move_x=float(bool(mx))-float(bool(nx)); move_y=float(bool(my))-float(bool(ny))
            aim_x,aim_y=0.0,0.0; firing=keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]
            if joysticks:
                stick=joysticks[0]
                try:
                    ax=stick.get_axis(0); ay=stick.get_axis(1)
                    if abs(ax)>.18: move_x=ax
                    if abs(ay)>.18: move_y=ay
                    rx=stick.get_axis(2) if stick.get_numaxes()>2 else 0.0
                    ry=stick.get_axis(3) if stick.get_numaxes()>3 else 0.0
                    if abs(rx)>.22 or abs(ry)>.22: aim_x,aim_y=rx,ry
                    if stick.get_numaxes()>4 and stick.get_axis(4)<-.45: firing=True
                    firing=firing or stick.get_button(0)
                except pygame.error: pass
            player.update(dt,(move_x,move_y)); player.x=max(35,min(WORLD_COLS*64-35,player.x)); player.y=max(35,min(WORLD_ROWS*64-35,player.y)); camera.follow(player,dt)
            center=(INTERNAL_WIDTH//2,INTERNAL_HEIGHT//2)
            if aim_x==0.0 and aim_y==0.0:
                mouse=pygame.mouse.get_pos(); ww,wh=window.get_size()
                sx=mouse[0]*INTERNAL_WIDTH/max(1,ww); sy=mouse[1]*INTERNAL_HEIGHT/max(1,wh)
                dx,dy=sx-center[0],sy-center[1]
                # Inverse of the isometric projection, in world-space units.
                aim_x=2.0*dx+2.0*dy; aim_y=2.0*dy-2.0*dx
            if abs(aim_x)+abs(aim_y)>.001: player.angle=math.atan2(aim_y,aim_x)
            if firing and player.cooldown<=0:
                p=bullets.acquire()
                if p:
                    p.launch(player.x,player.y,math.cos(player.angle)*430,math.sin(player.angle)*430,"player",1)
                    player.cooldown=.16
            if (keys[pygame.K_e] or (joysticks and joysticks[0].get_numbuttons()>3 and joysticks[0].get_button(3))) and player.pulse_cd<=0:
                pulse_flash=.22; player.pulse_cd=4.0
                for enemy in enemies:
                    if distance_sq(player.x,player.y,enemy.x,enemy.y)<210*210:
                        enemy.hp-=2
                burst(player.x,player.y,24,(75,225,255))
            pulse_flash=max(0.0,pulse_flash-dt)
            spawn_timer-=dt
            if spawn_left>0 and spawn_timer<=0:
                angle=random.random()*math.tau; dist=random.randint(330,470)
                ex=max(35,min(WORLD_COLS*64-35,player.x+math.cos(angle)*dist))
                ey=max(35,min(WORLD_ROWS*64-35,player.y+math.sin(angle)*dist))
                enemies.append(Drone(ex,ey)); spawn_left-=1; spawn_timer=.55
            for enemy in enemies:
                # Distant AI is intentionally updated less often to save CPU.
                d2=distance_sq(player.x,player.y,enemy.x,enemy.y)
                if d2<560*560 or int(pygame.time.get_ticks()/120)%3==0:
                    enemy.update(dt,player,enemy_shot)
                if d2<(enemy.radius+player.radius)**2 and player.invuln<=0:
                    player.hp-=10; player.invuln=.65; burst(enemy.x,enemy.y,5,(255,100,100))
            for bullet in bullets.active_items():
                bullet.update(dt)
                if not bullet.active: continue
                if bullet.team=="enemy":
                    if distance_sq(bullet.x,bullet.y,player.x,player.y)<(player.radius+4)**2 and player.invuln<=0:
                        player.hp=max(0,player.hp-8); player.invuln=.5; bullet.active=False; burst(player.x,player.y,4,(255,100,100))
                else:
                    for enemy in enemies:
                        if enemy.active and distance_sq(bullet.x,bullet.y,enemy.x,enemy.y)<(enemy.radius+4)**2:
                            enemy.hp-=bullet.damage; bullet.active=False; burst(bullet.x,bullet.y,3)
                            if enemy.hp<=0:
                                enemy.active=False; score+=100; burst(enemy.x,enemy.y,10,(255,135,100))
                            break
            enemies[:]=[e for e in enemies if e.active]
            for particle in particles.active_items(): particle.update(dt)
            if player.hp<=0: game_over=True
            if spawn_left==0 and not enemies:
                wave+=1; spawn_left=min(5+wave*2,22); spawn_timer=1.0; player.hp=min(player.max_hp,player.hp+12)
        renderer.begin(); renderer.draw_world(world,camera)
        center=(INTERNAL_WIDTH//2,INTERNAL_HEIGHT//2)
        for enemy in enemies:
            pos=world.screen_position(enemy.x,enemy.y,camera,center)
            renderer.draw_drone(enemy,pos)
        for bullet in bullets.active_items():
            pos=world.screen_position(bullet.x,bullet.y,camera,center); renderer.draw_projectile(bullet,pos)
        for particle in particles.active_items():
            pos=world.screen_position(particle.x,particle.y,camera,center); renderer.draw_particle(particle,pos)
        renderer.draw_player(player)
        if pulse_flash>0: pygame.draw.circle(renderer.canvas,(75,220,255),(INTERNAL_WIDTH//2,INTERNAL_HEIGHT//2),int(45*(pulse_flash/.22)),2)
        renderer.hud(player,score,wave,len(enemies),paused,game_over)
        if settings.show_performance:
            ms=dt*1000.0; label=renderer.font.render(f"{clock.get_fps():.0f} FPS | {ms:.1f} ms | enemies {len(enemies)} | pool {sum(1 for b in bullets.active_items())}",True,(120,245,180))
            renderer.canvas.blit(label,(INTERNAL_WIDTH-260,12))
        renderer.present(window)
    pygame.quit()

if __name__=="__main__":
    main()
