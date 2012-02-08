from math import *
import copy

from OpenGL.GL import *
import pygame
from pygame.locals import *


class RefFrame(object):
    def __init__(self,x=0.0,y=0.0,z=0.0,xr=0.0,yr=0.0,zr=0.0):
        super(RefFrame,self).__init__()

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.xr = float(xr)
        self.yr = float(yr)
        self.zr = float(zr)

    def __add__(self, other):
        ret = RefFrame()
        ret.x = self.x + other.x
        ret.y = self.y + other.y
        ret.z = self.z + other.z

        ret.xr = self.xr + other.xr
        if ret.xr > 360:
            remainder = ret.xr % 360
            ret.xr = remainder
        if ret.xr < 0:
            ret.xr += 360

        ret.yr = self.yr + other.yr
        if ret.yr > 360:
            remainder = ret.yr % 360
            ret.yr = remainder
        if ret.yr < 0:
            ret.yr += 360

        ret.zr = self.zr + other.zr
        if ret.zr > 360:
            remainder = ret.zr % 360
            ret.zr = remainder
        if ret.zr < 0:
            ret.zr += 360

        return ret

    def __sub__(self, other):
        ret = RefFrame()
        ret.x = self.x - other.x
        ret.y = self.y - other.y
        ret.z = self.z - other.z

        ret.xr = self.xr - other.xr
        if ret.xr > 360:
            remainder = ret.xr % 360
            ret.xr = remainder
        if ret.xr < 0:
            ret.xr += 360

        ret.yr = self.yr - other.yr
        if ret.yr > 360:
            remainder = ret.yr % 360
            ret.yr = remainder
        if ret.yr < 0:
            ret.yr += 360

        ret.zr = self.zr - other.zr
        if ret.zr > 360:
            remainder = ret.zr % 360
            ret.zr = remainder
        if ret.zr < 0:
            ret.zr += 360

        return ret


    def __str__(self):
        return str(self.x)+","+str(self.y)+","+str(self.z)+"|"+str(self.xr)+","+str(self.yr)+","+str(self.zr)

#Needs a change parent method
class Entity(object):

    def __init__(self,loc=None,glo=None,parent=None,children=None):
        super(Entity,self).__init__()
        self.glo = RefFrame()
        self.loc = RefFrame()

        if loc != None:
            self.loc = copy.copy(loc)
        if glo != None:
            self.glo = copy.copy(glo)

        self.children = []
        if children != None:
            self.children = children
        self.loc = loc
        self.parent = parent

    def __str__(self):
        info = ""
        info += "local: "+str(self.loc)+"\n"
        info += "global: "+str(self.glo)+"\n"
        if type(self.parent) == type(None):
            info += "parent: None\n"
        else:
            info += "parent: "+str(getattr(self.parent,"__init__"))+"\n"

        info += "children: "+str(self.children)+"\n"
        return info

    def removeChildren(self,to_remove):
        if type(to_remove) != list:
            raise TypeError("Children must be provided in a list")
        else:
            if to_remove == []:
                return
            else:
                for child in to_remove:
                    self.children.remove(child)
                    child.parent = None
                    child.updateLocalCoords()

    #takes a list of object type Entity to create children for a given parent
    def addChildren(self,to_add):
        if type(to_add) != list:
            raise TypeError("Children must be provided in a list")
        else:
            if to_add == []:
                return
            else:
                for child in to_add:
                    if hasattr(child,'parent'):
                        child.loc = RefFrame()
                        self.children.append(child)
                        #print "Appended "+str(child)
                        child.parent = self
                        if hasattr(child,"updateLocalCoords"):
                            child.updateLocalCoords()
                    else:
                        raise AttributeError("Child must have parent attributes")

    def setLocalCoords(self,x=None,y=None,z=None,xr=None,yr=None,zr=None):
        set_one = False
        if x != None:
            self.loc.x = x
            set_one = True
        if y != None:
            self.loc.y = y
            set_one = True
        if z != None:
            self.loc.z = z
            set_one = True
        if xr != None:
            self.loc.xr = xr
            set_one = True
        if yr != None:
            self.loc.yr = yr
            set_one = True
        if zr != None:
            self.loc.zr = zr
            set_one = True

        if set_one == True:
            self.updateGlobalCoords()


    def setGlobalCoords(self,x=None,y=None,z=None,xr=None,yr=None,zr=None):
        set_one = False
        if x != None:
            self.glo.x = x
            set_one = True
        if y != None:
            self.glo.y = y
            set_one = True
        if z != None:
            self.glo.z = z
            set_one = True
        if xr != None:
            self.glo.xr = xr
            set_one = True
        if yr != None:
            self.glo.yr = yr
            set_one = True
        if zr != None:
            self.glo.zr = zr
            set_one = True

        if set_one == True:
            self.updateLocalCoords()


    def updateLocalCoords(self):
        if self.parent == None:
            self.loc = copy.copy(self.glo)
        else:
            if self.loc == None:
                raise AttributeError("Cannot update local coordinates an Entity with no initial local coordinates")
            else:
                self.loc = self.glo - self.parent.glo

    def updateGlobalCoords(self):
        if self.parent == None:
            pass
        else:
            if self.loc == None:
                raise AttributeError("Cannot update global coordinates an Entity with no local coordinates")
            else:
                self.glo = self.loc + self.parent.glo


class Sphere(Entity):
    def __init__(self,size,pos,color):
        glColor(color[0],color[1],color[2])
        glutSolidSphere(size[0], size[1], size[2])
        if (pos.type == "global"):
            pass
        else:
            pass


class Camera(RefFrame):
    def __init__(self):
        super(Camera, self).__init__()
        self.mouse_smooth = 5
        self.mouse_cap = 100.0
        self.move_scale = 5


class Player(Camera):

    def __init__(self):
        super(Player,self).__init__()

    def getMove(self):
        mouse_x, mouse_y = pygame.mouse.get_rel()
        move_x = abs(mouse_x)

        if move_x > self.mouse_cap:
            move_x = self.mouse_cap

        move_x = (move_x / self.mouse_cap) * self.move_scale
        move_y = abs(mouse_y)

        if move_y > self.mouse_cap:
            move_y = self.mouse_cap

        move_y = (move_y / self.mouse_cap) * self.move_scale


        pressed = pygame.key.get_pressed()

        if mouse_x < -self.mouse_smooth:
            self.yr -= move_x
        if mouse_x > self.mouse_smooth:
            self.yr += move_x

        if self.yr > 360:
            remainder = self.yr % 360
            self.yr = remainder
        if self.yr < 0:
            self.yr += 360


        if mouse_y < -self.mouse_smooth:
            self.xr -= move_y
        if mouse_y > self.mouse_smooth:
            self.xr += move_y

        if self.xr > 360:
            remainder = self.xr % 360
            self.xr = remainder
        if self.xr < 0:
            self.xr += 360


        if pressed[K_a]:

            cam_rot_y_rad = radians(self.yr)

            self.x += cos(cam_rot_y_rad) * 1
            self.z += sin(cam_rot_y_rad) * 1


        if pressed[K_d]:
            cam_rot_y_rad = radians(self.yr)
            self.x -= cos(cam_rot_y_rad) * 1
            self.z -= sin(cam_rot_y_rad) * 1


        if pressed[K_w]:
            cam_rot_y_rad = radians(self.yr)
            cam_rot_x_rad = radians(self.xr)

            self.x -= sin(cam_rot_y_rad)
            self.y += sin(cam_rot_x_rad)
            self.z += cos(cam_rot_y_rad)



        if pressed[K_s]:
            cam_rot_y_rad = radians(self.yr)
            cam_rot_x_rad = radians(self.xr)

            self.x += sin(cam_rot_y_rad)
            self.y -= sin(cam_rot_x_rad)
            self.z -= cos(cam_rot_y_rad)

    def placePlayer(self):
        glRotate(self.xr,1,0,0)
        glRotate(self.yr,0,1,0)
        glTranslate(self.x,self.y,self.z)
