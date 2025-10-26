
from pygame.math import Vector2
from pygame.draw import circle, line, rect
import random, math

class Agent:
    def __init__(self, position, radius, color):
        self.circle_color = color
        self.radius = radius
        self.position = position
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.mass = 1.0
        self.EYE_SIGHT = 300
        self.STOP_DIST = 5
        self.current_waypoint = 0     # Start index for waypoint tracking
        self.waypoint_radius = 10
        self.target = Vector2(0,0)
        self.center_of_mass = Vector2(0,0)
        self.hunger = 100  # start full
        self.hungry_threshold = 40
        self.wander_angle = random.uniform(0, 2*math.pi)
        self.food_target = None


    
    def set_waypoints(self, waypoint_list):
        self.waypoints = waypoint_list
        self.current_waypoint = 0
    
    def follow_waypoints(self):
        if not self.waypoints:
            return
        target = self.waypoints[self.current_waypoint]
        dist = (target - self.position).length_squared()

        if dist < self.waypoint_radius * self.waypoint_radius:
        # Move to the next waypoint
            self.current_waypoint += 1
            if self.current_waypoint >= len(self.waypoints):
                self.current_waypoint = 0  # Loop back to start (optional)
        self.arrive_to(target)

        
    def seek_to(self, target_pos):
        self.target = target_pos

        MAX_FORCE = 2
        d = target_pos - self.position
        if d.length_squared() == 0:
            return
        
        desired = d.normalize() * MAX_FORCE
        steering = desired - self.vel
        
        if steering.length() > MAX_FORCE:
            steering.scale_to_length(MAX_FORCE)

        self.apply_force(steering)


    def seek_food_direct(self, food_list):
        if self.hunger > self.hungry_threshold:
            self.food_target = None
            return

        # Find closest visible food
        closest_food = None
        closest_dist = float('inf')
        for food in food_list:
            dist = (food - self.position).length_squared()
            if dist < closest_dist and dist < 200*200:  #vision range
                closest_food = food
                closest_dist = dist

        if closest_food:
            self.food_target = closest_food
            #directly set velocity toward food
            direction = (closest_food - self.position).normalize()
            MAX_SPEED = 150
            self.vel = direction * MAX_SPEED

            #Check if fish reached the food
            if (closest_food - self.position).length() < self.radius + 5:
                if closest_food in food_list:
                    food_list.remove(closest_food)
                self.hunger = 100
                print("yummers")
                self.food_target = None



    def avoid_walls(self, width, height, margin=50, strength=5):
        force = Vector2(0, 0)

        if self.position.x < margin:
            force.x = strength * (1 - self.position.x / margin)
        elif self.position.x > width - margin:
            force.x = -strength * (1 - (width - self.position.x) / margin)

        if self.position.y < margin:
            force.y = strength * (1 - self.position.y / margin)
        elif self.position.y > height - margin:
            force.y = -strength * (1 - (height - self.position.y) / margin)

        return force
    
    def wander(self, wander_radius=15, wander_distance=30, change_angle=0.2):
        self.wander_angle += random.uniform(-change_angle, change_angle)
        circle_center = self.vel.normalize()*wander_distance if self.vel.length() > 0 else Vector2(1,0)
        displacement = Vector2(wander_radius * math.cos(self.wander_angle),
                            wander_radius * math.sin(self.wander_angle))
        
        return circle_center + displacement

    def arrive_to(self, target_pos):
        MAX_FORCE = 5
        d = target_pos - self.position
        if d.length_squared() == 0:
            return
        
        desired = d.normalize() * MAX_FORCE
        steering = desired - self.vel
        
        if steering.length() > MAX_FORCE:
            steering.scale_to_length(MAX_FORCE)
 
        self.apply_force(steering)        

    def flee_from(self, target_pos):
        MAX_FORCE = 7
        d = (target_pos - self.position)
        if d.length_squared() == 0:
            return
        
        dist = d.length_squared()
        if dist > self.EYE_SIGHT * self.EYE_SIGHT:
            desired = Vector2(0, 0)
        else:
            desired = (-d).normalize() * (MAX_FORCE * ((self.EYE_SIGHT - dist)/self.EYE_SIGHT))
        
        steering = desired - self.vel
         
        if steering.length() > MAX_FORCE:
            steering.scale_to_length(MAX_FORCE)
        self.apply_force(steering)     

    def apply_force(self, force):
        self.acc += force / self.mass


    def get_cohesion_force(self, agents): #group up multiple agents
        center_of_mass = Vector2(0,0)
        count = 0
        for agent in agents:

            dist = (agent.position - self.position).length_squared()
            if 0 < dist < 400*400:
                center_of_mass += agent.position
                count +=1

        if count > 0:
            center_of_mass /= count
            d = center_of_mass - self.position
            d.scale_to_length(2)
            self.center_of_mass = center_of_mass
            return d
        return Vector2()
    
    def get_separation_force(self,agents):
        s = Vector2()
        count = 0
        for agent in agents:
            dist = (agent.position - self.position).length_squared()
            if dist < 100*100 and dist != 0:
                d = self.position - agent.position
                s += d
                count+=1

        if count>0:
            s.scale_to_length(2)
            return s
        
        return Vector2()

    def get_align_force(self,agents):
        s = Vector2()
        count = 0
        for agent in agents:
            dist = (agent.position - self.position).length_squared()
            if dist < 100*100 and dist != 0:
                s += agent.vel
                count+=1

        if count>0 and s != Vector2():
            s /= count
            s.scale_to_length(2)
            return s
        
        return Vector2()

    def update(self, dt, width, height):
        self.vel += self.acc

        MAX_SPEED = 100
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.position += self.vel * dt
        self.vel *= 0.95
        self.acc = Vector2(0, 0)
        self.hunger -= 5 * dt
        self.hunger = max(self.hunger, 0)

        #keep inside tank
        if self.position.x < self.radius:
            self.position.x = self.radius
            self.vel.x *= -0.5
        elif self.position.x > width - self.radius:
            self.position.x = width - self.radius
            self.vel.x *= -0.5

        if self.position.y < self.radius:
            self.position.y = self.radius
            self.vel.y *= -0.5
        elif self.position.y > height - self.radius:
            self.position.y = height - self.radius
            self.vel.y *= -0.5

    def draw(self, screen):

        circle(screen, self.circle_color, self.position, self.radius)
        #line(screen, (100,100,100),self.position,self.center_of_mass)