# coding: utf8
import os
import pygame as pg
import numpy as np

# import custom lib for Rocket DNA
from rocketlib.dna import DNA

# Rocket Sprites Class


class Rocket(pg.sprite.Sprite):
    """
    Description:
    ------------
        Initializes Sprites and Update them.
    Parameters:
    -----------
        imgFolder: string
            filepath of the sprite image
        resolution: tuple
            tuple of width and height of the screen
        id: int
            number of created sprites
    """

    def __init__(self, imgFolder, resolution, id, dna=None, king=False):
        img = "rocket_small_rgb.png"
        if(dna is None):
            self.dna = DNA()
            self.dna.generateNewRandomDNA()
        else:
            self.dna = dna
            if king:
                img = "rocket_small_green.png"

        # create pygame sprite
        pg.sprite.Sprite.__init__(self)

        # load rocket image for sprite
        self.original_image = pg.image.load(os.path.join(
            imgFolder, img)).convert()

        # (0,0,0) := BLACK, set_colorkey removes the opaque part of the sprite
        self.original_image.set_colorkey((0, 0, 0))

        # keep original_image to create rotated copies to image
        self.image = self.original_image
        self.image.set_colorkey((0, 0, 0))

        # used to turn the spirtes
        self.rot_angle = 0

        # position and speed
        self.rect = self.image.get_rect()
        self.initialPos = (resolution[0]/2, resolution[1]-self.rect.height/2)
        self.curSpeed = (0., 0.)
        self.rect.center = self.initialPos

        self.fitness = 0
        # path history for trajectory lines
        self.trajectory = [self.initialPos]
        
        self.resolution = resolution
        self.updateCounter = 0
        self.dnaCounter = 0
        self.killFlag = False

    def getInitialPos(self):
        return self.initialPos

    def getPos(self):
        return self.rect.center

    def rot_center(self, angle=None):
        """ 
        rotates the sprite while keeping its center
        Parameters
        ----------
            angle : float, optional
                rotation angle in degree
        Returns
        ------
            None
        """
        # get angle from object
        if angle is None:
            angle = self.rot_angle
            # permanent rotation in 45° steps, used when out of fuel
            self.rot_angle += 45 % 360
        # rotate
        self.image = pg.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_rotangle(self, newPos):
        """
        calulate the rotation angle of sprites based on current
        path of object
        Parameters
        ----------
            newPos : tuple
                new Postion of sprite, format like (xPos,yPos)
        Returns
        ------- 
            angle : float 
                rotation angle in degree 
        """
        vec_old = self.rect.center[0]+1j*self.rect.center[1]
        vec_new = newPos[0]+1j*newPos[1]
        vec = vec_new - vec_old
        angle = np.angle(-vec, deg=1)

        return -angle+90

    def update(self, simulate=False):
        """
        Description:
        ------------
            perform next acceleration step and update Rockets position and speed
        Parameters:
        ----------
            simulate : boolean
                True: skip calculation of rotation angle (only needed for drawing)
                Default: False
        """
        self.updateCounter += 1
        # check if rocket is dead
        if (self.killFlag == True):
            return
        
        # movement description
        gravity = 9.81
        time = 1./2
        # check if there are further acceleration steps
        if (self.dnaCounter >= self.dna.accSteps):
            xDiff = 0
            yDiff = 0.5*(gravity)*time**2
        # calculate new acceleration
        else:
            xDiff = 0.5*(-1*self.dna.path[0, self.dnaCounter])*time**2
            yDiff = 0.5*(-1*self.dna.path[1, self.dnaCounter]+gravity)*time**2
        # calculate new position
        # s = s_0 + 1/2*(a-g)*t^2 + v*t
        xPos = self.rect.center[0] + xDiff + self.curSpeed[0]*time
        yPos = self.rect.center[1] + yDiff + self.curSpeed[1]*time

        # save trajectory history (used for drawing)
        self.trajectory.append((xPos, yPos))

        # only needed for drawing rockets
        if not simulate:
            # rotate based on new position
            self.rot_center(self.get_rotangle((xPos, yPos)))

        # collision detection, rocket reached the ground
        if(yPos >= self.resolution[1]):
            self.killFlag = True
            return

        # calculate current speed
        curSpeedX = (xPos - self.rect.center[0])/(time)
        curSpeedY = (yPos - self.rect.center[1])/(time)

        # updating the position and speed
        self.curSpeed = (curSpeedX, curSpeedY)
        self.rect.center = (xPos, yPos)

        self.dnaCounter += 1

        return
