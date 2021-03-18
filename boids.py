import math
    #main boid class, takes care of boid processing and creation
class boid():
    def __init__(self,pos,speed,direction,behaviors = []):
        self.p = pos
        self.s = speed
        self.d = direction
        self.behaviors = behaviors
    def set_behavior(self,behaviors):
        self.behaviors = behaviors
    def move(self):
        self.p = (self.p[0]+math.acos(self.d)*self.s,self.p[1]+math.asin(self.d)*self.s)
    def step(self,info):
        direction = self.d
        for behavior in self.behaviors:
            behavior.run(self,info)
        b = self
        b.move()
        return b

    #Subclass this to add more behaviors
class behavior():
    @staticmethod
    def followPoint(boid : boid,strength : float,info : dict, *keys):
                                                                    # key[n] refers to:
        point = info[keys[0]]                                       # (x coord, y coord)
        pos = boid.p
        rel = [point[i]-pos[i] for i in [0,1]]
        angle = math.atan2(rel[1], rel[0])
        theta_diff = angle - boid.d
        if theta_diff > math.pi:
            theta_diff -= math.tau
        elif theta_diff < -math.pi:
            theta_diff += math.tau
        if abs(theta_diff) > strength:
            boid.d += math.copysign(strength,theta_diff)
        else:
            boid.d = angle
    
    @staticmethod
    def avoidPoint(boid : boid, strength : float, info : dict, *keys):
                                                                    # key[n] refers to:
        point = info[keys[0]]                                       # (x coord, y coord)
        t_distance = info[keys[1]]                                  # float
        turn_dir = {'left': 1, 'right': -1}[info[keys[2]].lower()]  # either 'left' or 'right'
        whirlpool = [info[keys[3]]]                                 # boolean (enables whirlpool behavior)
        
        pos = boid.p
        x, y = (pos[0]-point[0]) , (pos[1]-point[1])
        distance = math.sqrt(x*x+y*y)
        
        if distance < t_distance:
            boid.d += strength*turn_dir
        elif whirlpool:
            boid.d += strength*turn_dir * (t_distance/(2*distance))


    def __init__(self,strength,callback,*keys):
        self.s = strength
        self.c = callback
        self.k = keys
    def run(self,boid,info):
        self.c(boid,self.s,info,*self.k)