#!/usr/bin/env python3

# Copyright (c) 2016 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Display Cozmo's camera feed back on his face (like a mirror)
'''
import asyncio
import sys
import time

try:
    import numpy as np
except ImportError:
    sys.exit("Cannot import numpy: Do `pip3 install --user numpy` to install")

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

def get_in_position(robot: cozmo.robot.Robot):
    '''If necessary, Move Cozmo's Head and Lift to make it easy to see Cozmo's face.'''
    if (robot.lift_height.distance_mm > 45) or (robot.head_angle.degrees < 40):
        with robot.perform_off_charger():
            lift_action = robot.set_lift_height(0.0, in_parallel=True)
            head_action = robot.set_head_angle(degrees(20),
                                               in_parallel=True)
            lift_action.wait_for_completed()
            head_action.wait_for_completed()     


def calc_pixel_threshold(image: Image):
    '''Calculate a pixel threshold based on the image.

    Anything brighter than this will be shown on (light blue).
    Anything darker will be shown off (black).
    '''

    # Convert image to gray scale
    grayscale_image = image.convert('L')

    # Calculate the mean (average) value
    mean_value = np.mean(grayscale_image.getdata())
    return mean_value


def cozmo_face_mirror(robot: cozmo.robot.Robot):
    '''Continuously display Cozmo's camera feed back on his face.'''
    print("Do ps")
    robot.camera.image_stream_enabled = True
    robot.set_head_light(enable=True)
 #   get_in_position(robot)
    while(True) :
        face_dimensions = cozmo.oled_face.SCREEN_WIDTH, cozmo.oled_face.SCREEN_HALF_HEIGHT

        duration_s = 0.1  # time to display each camera frame on Cozmo's face

        latest_image = robot.world.latest_image

        if latest_image is not None:
                    
            # Scale the camera image down to fit on Cozmo's face
            resized_image = latest_image.raw_image.resize(face_dimensions,Image.BICUBIC)

            # Flip the image left/right so it displays mirrored
            rezed_image = resized_image.transpose(Image.FLIP_LEFT_RIGHT)

            # Calculate the pixel threshold for this image. This threshold
            # will define how bright a pixel needs to be in the source image
            # for it to be displayed as lit-up on Cozmo's face.
            pixel_threshold = calc_pixel_threshold(resized_image)  #so right now it's the value of the threshold

            print (pixel_threshold)
            if pixel_threshold < 85 or pixel_threshold > 120: #use the threshold values to see whether or not there are obstacles
                robot.turn_in_place(degrees(45)).wait_for_completed() #turn if there is an obstacle
                print ("Turn")
                
            else :
                print ("Go")  #move straight if there is not obstacle
                robot.drive_straight(distance_mm(40), speed_mmps(90)).wait_for_completed()
                    # Move lift down and tilt the head up
   
        time.sleep(1)   
            

cozmo.run_program(cozmo_face_mirror, use_3d_viewer=True, use_viewer=True)
