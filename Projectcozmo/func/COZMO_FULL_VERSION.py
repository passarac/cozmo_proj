import cozmo, time, asyncio
import os
from cozmo.util import degrees, Pose, distance_mm, speed_mmps
from PIL import Image
cwd = os.getcwd()
num= 1
take_pic = 0

#############################################################################################################################################

def inside_conference(robot: cozmo.robot.Robot) :
    count_distance = 0
    
    while True:
        for i in range(6):
            robot.drive_straight(distance_mm(300), speed_mmps(100)).wait_for_completed() #move foward
        
            count_distance = count_distance+300
            print (count_distance)
        
            robot.turn_in_place(degrees(90)).wait_for_completed() #robot turns 90 degrees
            robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed() #robot lifts head to max head angle
        
            try:
                face_event = robot.world.wait_for(cozmo.faces.EvtFaceObserved, timeout=6) #tries to find the face for 6 secs
                print ("Face found") #prints "face found"
                robot.set_all_backpack_lights(cozmo.lights.green_light)

                ###
                name_of_face = face_event.face.name
                if name_of_face == '':
                    cozmo_take_pic_conference(robot)
                    robot.say_text("beep beep").wait_for_completed()
                    robot.say_text("beep beep").wait_for_completed()
                    robot.say_text("beep beep").wait_for_completed()
                    robot.say_text("beep beep").wait_for_completed()
                ###
            
                robot.turn_in_place(degrees(90)).wait_for_completed() #turns 90 degrees
                robot.turn_in_place(degrees(90)).wait_for_completed() #turns 90 degrees to face the other side

            except asyncio.TimeoutError : #in the case that cozmo does not find a face
                print("New face not found") #prints "new face not found"
                robot.set_all_backpack_lights(cozmo.lights.red_light)

            
                robot.turn_in_place(degrees(90)).wait_for_completed() #turns 90 degrees
                robot.turn_in_place(degrees(90)).wait_for_completed() #turns 90 degrees to face the other side

                robot.set_all_backpack_lights(cozmo.lights.off_light)
            
            try:
                face_event = robot.world.wait_for(cozmo.faces.EvtFaceObserved, timeout=6) #tries to find the face for 6 seconds
                print ("Face found") #print "face found"
                robot.set_all_backpack_lights(cozmo.lights.green_light)

                ###
                name_of_face = face_event.face.name
                if name_of_face == '':
                    cozmo_take_pic_conference(robot)
                ###


                robot.set_all_backpack_lights(cozmo.lights.off_light)
            
            
                robot.turn_in_place(degrees(90)).wait_for_completed() #turns 90 degrees to initial position to keep walking
            
            except asyncio.TimeoutError : #in the case that cozmo does not find a face
                print("No new face found")
                robot.set_all_backpack_lights(cozmo.lights.red_light)
                
                robot.turn_in_place(degrees(90)).wait_for_completed() #turns 90 degrees to get back to inital position

                robot.set_all_backpack_lights(cozmo.lights.off_light)


        robot.turn_in_place(degrees(180)).wait_for_completed()


        for i in range(6):
            robot.drive_straight(distance_mm(300), speed_mmps(100)).wait_for_completed() #move foward
        
            count_distance = count_distance+300
            print (count_distance)
        
            robot.turn_in_place(degrees(90)).wait_for_completed() #robot turns 90 degrees
            robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed() #robot lifts head to max head angle
        
            try:
                face_event = robot.world.wait_for(cozmo.faces.EvtFaceObserved, timeout=6) #tries to find the face for 6 secs
                print ("Face found") #prints "face found"
                robot.set_all_backpack_lights(cozmo.lights.green_light)

                ###
                name_of_face = face_event.face.name
                if name_of_face == '':
                    cozmo_take_pic_conference()
                ###
            
                robot.turn_in_place(degrees(90)).wait_for_completed() #turns 90 degrees
                robot.turn_in_place(degrees(90)).wait_for_completed() #turns 90 degrees to face the other side

            except asyncio.TimeoutError : #in the case that cozmo does not find a face
                print("New face not found") #prints "new face not found"
                robot.set_all_backpack_lights(cozmo.lights.red_light)
            
                robot.turn_in_place(degrees(90)).wait_for_completed() #turns 90 degrees
                robot.turn_in_place(degrees(90)).wait_for_completed() #turns 90 degrees to face the other side
            
            try:
                face_event = robot.world.wait_for(cozmo.faces.EvtFaceObserved, timeout=6) #tries to find the face for 6 seconds
                print ("Face found") #print "face found"
                robot.set_all_backpack_lights(cozmo.lights.green_light)
    
                ###
                name_of_face = face_event.face.name
                if name_of_face == '':
                    cozmo_take_pic_conference()
                ###
            
                robot.turn_in_place(degrees(90)).wait_for_completed() #turns 90 degrees to initial position to keep walking
            
            except asyncio.TimeoutError : #in the case that cozmo does not find a face
                print("No new face found")
                robot.set_all_backpack_lights(cozmo.lights.red_light)

                
                robot.turn_in_place(degrees(90)).wait_for_completed() #turns 90 degrees to get back to inital position

#############################################################################################################################################

def remember_face(robot: cozmo.robot.Robot):
    faces = []
    names = []
    with open('/Users/passara/Desktop/face_id_s.txt',"r+") as file:
        readin = file.read().split(" ")
        
    for face_id in readin:
        faces.append(face_id)
        
    while True:
        robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
        try:
            face_event = robot.world.wait_for(cozmo.faces.EvtFaceObserved, timeout=6) #tries to find the face for 6 secs
            print ("Face found") #prints "face found"
            
            robot.set_all_backpack_lights(cozmo.lights.green_light)
            
            face_id = face_event.face.face_id #gets the face id of the person
            if not (str(face_id) in faces) :
                with open('/Users/passara/Desktop/face_id_s.txt',"a+") as file:
                    lines = file.write(str(face_id)+' ')
    
                faces.append(str(face_id)) #face id of the person is added to the empty list above
                faceName = input("enter name   ")
                face_event.face.name_face(faceName)
                print ("name = ", faceName)
                print("hi")
            
            else:
                global take_pic
                if take_pic ==0:
                   print(face_event.face.name)
                   cozmo_take_pic_remember(robot,face_event.face.name) #cozmo then takes a picture
                   print (faces) #prints face id inside the list
                   take_pic+=1
            

        except asyncio.TimeoutError : #in the case that cozmo does not find a face
            print("New face not found") #prints "new face not found"
                
            robot.set_all_backpack_lights(cozmo.lights.red_light)
            robot.set_all_backpack_lights(cozmo.lights.off_light)
            


############################################################################################################################################            

def cozmo_take_pic_conference(robot: cozmo.robot.Robot):
    global num
    cozmo.camera.Camera.image_stream_enabled = True #set to true so that images can be received
    latest_image = robot.world.latest_image #get the latest image from Cozmo's camera
    img = latest_image.annotate_image() #resize it, this will return an image
    img.save(cwd+'/pic/test%s.jpg' %num)
    print (latest_image) #not necessary
    img.show() #show the image
    num+=1

#############################################################################################################################################

def cozmo_take_pic_remember(robot: cozmo.robot.Robot,faceName):
    cozmo.camera.Camera.image_stream_enabled = True #set to true so that images can be received
    print(1)
    latest = robot.world.latest_image #get the latest image from Cozmo's camera
    print (latest)
    img = latest.annotate_image()
    print ('annotate')
    img.save(cwd+'/participants/%s.jpg' %faceName)
    img.show() #show the image
    print(5)

############################################################################################################################################

def erase_all(robot: cozmo.robot.Robot):
    cozmo.faces.erase_all_enrolled_faces(robot.conn)

############################################################################################################################################


#cozmo.run_program(erase_all, use_viewer=True)
#cozmo.run_program(remember_face, use_viewer=True)
cozmo.run_program(inside_conference, use_viewer=True)


