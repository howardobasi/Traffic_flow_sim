#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 14:41:50 2023

@author: howardobasi
"""

import numpy as np
import pygame, sys
import random 


''' Car simulation constants '''


N = 15                   # number of cars on road

car_width = 20           # pygame car sizes 
car_height = 10

max_speed = 22.22        # upper and lower speed limits 
min_speed = 15     
                   
brake_dist = 40          # distances for when to apply brake


p = 0.3                  # random braking probability


''' pygame simulation size and colours '''


screen_width = 1420       # screen size
screen_height = 400                 


driving_lane = 260        # road positions 
opposite_lane = 282
lane_height = 20

green = (61,145,64)       # colour codes 
red = (205,38,38)
grey = (73, 75, 73)
white = (255,255,255)


''' defining functions for simulation '''


def create_car(screen_width, screen_height, car_width, car_height, colour, x, y, speed, accel, max_speed,brake_dist,delta_speed):
    
    image = pygame.Surface((car_width, car_height))  # creating a surface in pygame to represent the car
    image.fill(colour)
    rect = image.get_rect()
    position = np.array([x], dtype=np.float64)       # creating an array for the cars x position along the road 
    rect.y = y                                       # creating an array for the lane of the car 
    speed = np.array(speed, dtype=np.float64)
    accel = np.array(accel, dtype=np.float64)        # creating an array for the car's speed and acceleration
    delta_speed = np.array(delta_speed, dtype=int)
    
    
    car = {                                          # Creating a dictionary to represent the car and its defining attributes
        "image": image,
        "rect": rect,
        "position": position,
        "speed": speed,
        "accel": accel,
        "max_speed": max_speed,
        "delta_speed":delta_speed,
        "brake_dist":brake_dist,
        "car_width": car_width,
        "car_height": car_height,
        "screen_width": screen_width,
        "screen_height": screen_height,
        "y": rect.y,
        
    }
    return car                                       # Return the car dictionary

def updated_car(car):
    
    car["position"] += car["speed"]                  # Move the car according to its speed
             
    if car["speed"] < car["max_speed"]:#+car["delta_speed"]:              # Increase the speed of the car if it is less than the maximum speed 
                                                                          # additional delta speed to include over /under speeding in model
    #if random.random()<0.6:                                              # probability of acceleration when testign adverse weatehr conditions                    
        car["speed"] += car["accel"]                                      
        
    x = car["position"]                              # Update the cars x-position along the road 
    
    if x > car["screen_width"]:                      # If the car goes out of the screen, wrap it around back to the start (treating road as closed circle)
        car["position"][0] = 0
        x = 0      
        
        
    car["rect"].x = x                                # update the x-position of the car's rectangle (pygame image)

def car_braking(cars):                      # cars - a list of car dictionaries , base_deaccel - deceleration rate of car braking , p - probability of a car randomly braking

    for car in cars:                                       # loop through each car
        for car2 in cars:                                  # loop through each other car
        
            if car["position"] == car2["position"]:        # if the cars are in the same position do nothing (i.e loop comparing the same car)       
                pass
            
            if car["y"] == car2["y"]:                      # check to see if the cars are in the same lane
            
                if car2["position"] > car["position"]:     # check to see if the second car is ahead of the first car
                    
                        if car2["position"] - car["position"] < car["brake_dist"] + car["car_width"]:    # check to see if the two cars are within the set minimum distance
                            car["speed"] = car2["speed"]-1                                                 # apply brakes hence deaccelerate, reducing speed                               
                            
                if car2["position"] < car["position"]:                                                   
                                               
                        if car["screen_width"] + car2["position"] - car["position"] < car["brake_dist"] + car["car_width"]:  # as the above condition but for when comparing cars at very start to very end of road  
                            car["speed"] = car2["speed"]-1                                                              # apply brakes hence deaccelerate, reducing speed 
                             
                    
                if car["speed"] < 0:                               # make sure that the car's speed is not less than 1 (avoids issues of stationary cars)
                    car["speed"] = 0
    
def random_braking(cars,p): 
    if iterations > 34:                                    # allows cars to reach max speed before introducing random braking 
        if random.random() < p:                                   # with probability p randomly cause a car to brake 
          car["speed"] = max( car["speed"] - 1, min_speed)                # apply brake, reducing speed  
    
    
''' starting simulation in pygame '''

 
pygame.init()                                                         # Initialize pygame module
screen = pygame.display.set_mode([screen_width, screen_height])       # Set screen size

cars = []                                                             # Create an empty list to store the cars

for i in range(N):                                                    # Create N number of cars with random position, speed, and acceleration
    x = np.random.randint(0, screen_width + 1)                        # each car given random position along road 
    if random.random()<0.24:
        delta_speed = random.uniform(0,1.49)                          # based on respective probability allows car to speed by a chosen value between two regions
    elif random.random()<0.14:                  
        delta_speed = random.uniform(1.49,2.98)
    elif random.random()<0.10:    
        delta_speed = random.uniform(2.98,4.47)
    elif random.random()<0.24:
        delta_speed = random.uniform(-1.49,0)
    elif random.random()<1:                                          # if none of above satisfied car will not over / under speed
        delta_speed =0
    speed = 0                                                        # sets initial speed at rest
    accel = 0.6667                                                   # sets acceleration rate of cars  
    car = create_car(screen_width, screen_height, car_width, car_height, red, x,driving_lane, speed, accel,max_speed,brake_dist,delta_speed)
    cars.append(car)


clock = pygame.time.Clock()                                           # Create a Pygame clock object
pygame.display.set_caption("Traffic Simulation")                      # Set the caption of the Pygame window

pygame.font.init()                                                    # Initialize Pygame font and create a font object
font = pygame.font.SysFont("Arial", 18)

    

flow_iteration_count = -80           # counts how many iterations there has been to count flow starts at -80 as a delay 
total_flow = []                      # empty list to store measurements of flow 
cars_passed = 0                     
cars_passed2 = 0
cars_passed3 = 0
iterations = 0#                     # counts how many iterations to act as a trigger for random braking 

for i in range(560):                # main loop iterates 560 times - 140 time steps

    flow_iteration_count += 1       # both count the iterations 
    iterations +=1
    
    if flow_iteration_count == 80:   # 80 iterations is 20 time steps, used to measure flow 
        flow = cars_passed           # number of cars passed in 20 time steps
        flow2 = cars_passed2         
        flow3 = cars_passed3         # ^
        total_flow.append(flow)      # store flow calculation in the empty list 
        total_flow.append(flow2)     
        total_flow.append(flow3)     # ^
        flow_iteration_count = 0     # reset counters 
        cars_passed = 0
        cars_passed2 = 0
        cars_passed3 =0              # ^

    for event in pygame.event.get():       # iterate over events in pygame 
        if event.type==pygame.QUIT:        # check if user/other triggered quit 
           sys.exit()                      # exit the program if the quit detected
           
    screen.fill(green)                                                # fill the screen with background colour
        

    pygame.draw.rect(screen, grey,(0,driving_lane-4, screen_width, lane_height))  # draw the driving lanes
    pygame.draw.rect(screen, grey,(0,opposite_lane, screen_width,lane_height))    # draw the opposite lane 
     
    car_braking(cars)                                  # check for car braking based on distance between cars
     
    random_braking(cars,p)

    for car in cars:                                                  # update car positions on the screen
        screen.blit(car["image"], car["rect"])                        

        updated_car(car)                                              # update car position based on its speed 

        if car["position"] <= 1065 and car["position"] + car["speed"] >= 1065 and iterations >80:  # confirms and counts a car has passed certain point on the road for measurement of flow
            cars_passed += 1
            
        if car["position"] <= 355 and car["position"] + car["speed"] >= 355 and iterations >80:   # ^
            cars_passed2 += 1
            
        if car["position"] <= 710 and car["position"] + car["speed"] >= 710 and iterations >80:   # ^
            cars_passed3 += 1 

        car_braking(cars)                              # check for car braking based on distance between cars

        random_braking(cars,p)

    pygame.display.update()                                           # update display and set the fps
    clock.tick(20)
        

''' flow vs density calculations '''


print()
print()
print('flow = ',total_flow)                        # prints the flow measurements taken for a run of the simulation
print()
print('density = ',(N*car_width)/screen_width)     # prints the corresponding density for a run of the simulation








