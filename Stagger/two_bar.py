import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import fractions
from . import Anchor
from . import Bar

class Two_Bar(object):
    def __init__(self, drive1, drive2, bar1, bar2):
    
        self.drive1 = drive1
        self.drive2 = drive2
        self.bar1 = bar1
        self.bar2 = bar2
    
        if (drive1.distance_from(drive2.x, drive2.y)[0] + drive1.r + drive2.r) >= (bar1.joint + bar2.length):
            raise NameError('Bars too short!')
        if ((drive1.distance_from(drive2.x, drive2.y)[0] - drive1.r) + bar1.joint) < (bar2.length):
            raise NameError('Bars too long!')
        
        #identify speeds
        self.animationSpeed = self.lcm(drive1.speed, drive2.speed)
        
        
    def lcm(a,b): return abs(a * b) / fractions.gcd(a,b) if a and b else 0

    def cosine_law(A, B, C):
        out = np.arccos((A * A + B * B - C * C)/(2.0 * A * B))
        return out
        
    def line_end(X, Y, R, T):
        x = X + np.cos(T) * R
        y = Y + np.sin(T) * R
        return x, y
        
        
        
    def end_path(self, drive1, drive2, bar1, bar2, i):
        #drive 1
        Drive1X, Drive1Y = drive1.base_point(i)
        
        Drive1X = Drive1X + drive1.x
        Drive1Y = Drive1Y + drive1.y

        #drive 2
        Drive2X, Drive2Y = drive2.base_point(i)
        
        Drive2X = Drive2X + drive2.x
        Drive2Y = Drive2Y + drive2.y

        driveAngle = np.arctan((Drive1Y - Drive2Y) / (Drive1X - Drive2X))
        
        driveLengthR = np.sqrt((Drive2X - Drive1X)**2 + (Drive2Y - Drive1Y)**2)
        angle = self.cosine_law(bar1.joint, driveLengthR, bar2.length)
        
        return self.line_end(Drive1X, Drive1Y, drive1.r, angle + driveAngle)

    def define_speed(self):
        if drive1.speed == 0:
            animate['frames'] = 360 / np.abs(drive2.speed)
            animate['delay'] = 100 / np.abs(drive2.speed)
        elif drive2.speed == 0:
            animate['frames'] = 360 / np.abs(drive1.speed)
            animate['delay'] = 100 / np.abs(drive1.speed)
        elif np.abs(drive1.speed) > np.abs(drive2.speed):
            lcm = lcm(np.abs(drive1.speed), np.abs(drive2.speed))
            print(lcm)
            animate['frames'] = int(lcm)
            lowest = lcm / np.abs(drive2.speed)
            animate['frames'] = int(lowest) * 360
            
            drive2['interval'] = 360 * lowest * drive2.speed
            print(drive2['interval'])
            #drive2['interval'] = (lcm / drive1.speed) / 360
            
            drive1['interval'] = drive1.speed
            
            animate['delay'] = 100 # / np.abs(drive2.speed)
            #animate = { 'delay': 100 / np.abs(drive2.speed), 'frames':  np.abs(drive2.speed)}
            speed2 = 1
            speed1 = np.abs(drive1.speed / drive2.speed)
        else:
            lcm = lcm(np.abs(drive1.speed), np.abs(drive2.speed))
            print(lcm)
            animate = { 'delay': 100 / np.abs(drive1.speed), 'frames':  np.abs(drive1.speed)}
            speed1 = 1
            speed2 = np.abs(drive2.speed / drive1.speed)
    