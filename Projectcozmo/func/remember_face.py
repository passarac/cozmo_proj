import cozmo, time, asyncio
import settings
from cozmo.util import degrees, Pose, distance_mm, speed_mmps

def cozmo_program(robot: cozmo.robot.Robot):  
    robot.world.request_nav_memory_map(0.5)
    deg = 45 
    mode = 0
    faces_memory = [] #create an empty list to store face id
    
    cozmo.faces.erase_all_enrolled_faces(robot.conn) 
    robot.say_text("Remember Mode").wait_for_completed() #the first mode is remember mode which is to remember the faces of ppl
    while(True): #infinite loop starts
        print("do the loop")

        try :
            print ("Check mode")
            robot.world.wait_for_observed_light_cube(timeout=5) #if a lightcube is found, the mode changes from remember mode to operational mode
            print("Found lightcube")
            if(mode == 0) :
                mode = 1
                print("Op")
                robot.say_text("Operation Mode").wait_for_completed() #cozmo says operation mode
            else :
                mode = 0 #otherwise, the mode is back to remember mode
                print("Re")
                robot.say_text("Remember Mode").wait_for_completed() #cozmo says remember mode
        except asyncio.TimeoutError :
            print("Didn't find a cube")


        if(mode == 0) :
            try :
                print ("Do faces detection") 
                robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
                face_event = robot.world.wait_for(cozmo.faces.EvtFaceObserved, timeout=5)
                print("Face found %s" %face_event.face.face_id)
                if not(face_event.face.face_id in faces_memory) :
                    robot.say_text("Hi").wait_for_completed()
                    faces_memory.append(face_event.face.face_id) #the face id of the person is added into the empty list
                
            except asyncio.TimeoutError :
                print("Not found any new face") 
                
        else :
            
            try :
                print ("Do faces detection") 
                robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
                face_event = robot.world.wait_for(cozmo.faces.EvtFaceObserved, timeout=5)
                print("Face found %s" %face_event.face.face_id)
                if not(face_event.face.face_id in faces_memory) :
                    robot.say_text("I don't know you").wait_for_completed()
                
            except asyncio.TimeoutError :
                print("Not found any new face")
        
                


        try :
            print ("Do objects detection")
            robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE / 2).wait_for_completed()
            event = robot.world.wait_for(cozmo.nav_memory_map.EvtNewNavMemoryMap, timeout=2)
            #print ("event = %s" % event)
            nav_map = event.nav_memory_map

            _posX = robot.pose.position.x #x position
            _posY = robot.pose.position.y #y position
            anglez = str(robot.pose.rotation.angle_z)
            atemp = anglez.split("(")
            atemp2 = atemp[1].split(" degree")
            _angle = float(atemp2[0])
            
            print("Robot info : x="+str(_posX)+" y="+str(_posY)+" angle="+str(_angle))
            state = scan_block(_posX, _posY, _angle, nav_map)
            #state = scan_block_test(-40.29963302612305, -199.53224182128906, -87.09, nav_map)
            if state[2] > 4:
                robot.turn_in_place(degrees(45)).wait_for_completed()
                print ("Turn")
                
            else :
                print ("Go")
                robot.drive_straight(distance_mm(100), speed_mmps(100)).wait_for_completed()
                
        except asyncio.TimeoutError :
            print("Time out waiting for map")
        time.sleep(0.2)
        if deg == 45:
            deg = 90
        else:
            deg = 45
        #robot.go_to_pose(Pose(100, 100, 0, angle_z=degrees(deg)), relative_to_robot=False).wait_for_completed()


def scan_block (posx, posy, angle, nav_map) : #
    posx = int(posx) #x position
    posy = int(posy) #y position
    state = [0,0,0] #state is a list with three elements; will determine if cozmo is in front of an obstacle or not
    sampling = 7
    #the following code is to see in which direction/angle cozmo is turened in to scan the block in front of it
    if (angle >= 0 and angle <23) or (angle < 0 and angle > -23) :
        for i in range(posx, posx + 150, sampling) :
           for j in range(posy-25, posy+25, sampling) :
               #print ("scan "+str(i)+","+str(j)+" : "+str(convert_content(str(nav_map.get_content(i,j)))))
               content = str(nav_map.get_content(i,j))
               state[convert_content(content)] += 1
                                  
               
    elif (angle >= 23 and angle <65) :
        for i in range(posx-10, posx + 120, sampling) :
           for j in range((posy-25)+(posx-i), (posy+25)+(posx-i), sampling) :
               #print ("scan "+str(i)+","+str(j)+" : "+str(nav_map.get_content(i,j)))
               content = str(nav_map.get_content(i,j))
               state[convert_content(content)] += 1

               
    elif (angle >= 65 and angle <115) :
        for i in range(posx-25, posx + 25, sampling) :
           for j in range((posy), (posy+150), sampling) :
               #print ("scan "+str(i)+","+str(j)+" : "+str(nav_map.get_content(i,j)))
               content = str(nav_map.get_content(i,j))
               state[convert_content(content)] += 1
               
    elif (angle >= 115 and angle <158) :
        for i in range(posx-120, posx + 10, sampling) :
           for j in range((posy-25), (posy+25), sampling) :
               #print ("scan "+str(i)+","+str(j)+" : "+str(nav_map.get_content(i,j)))
               content = str(nav_map.get_content(i,j))
               state[convert_content(content)] += 1
    
    elif (angle >= 158 and angle <180) or (angle < -158 and angle > -180) :
        for i in range(posx - 150, posx + 0, sampling) :
           for j in range(posy-25, posy+25, sampling) :
               #print ("scan "+str(i)+","+str(j)+" : "+str(nav_map.get_content(i,j)))
               content = str(nav_map.get_content(i,j))
               state[convert_content(content)] += 1
               
    elif (angle >= -158 and angle <-115) :
        for i in range(posx-120, posx+10, sampling ) :
           for j in range((posy-25)-(posx-i), (posy+25)-(posx-i), sampling) :
               #print ("scan "+str(i)+","+str(j)+" : "+str(nav_map.get_content(i,j)))
               content = str(nav_map.get_content(i,j))
               state[convert_content(content)] += 1
    
    elif (angle >= -115 and angle < -65) :
        for i in range(posx-25, posx + 25, sampling) :
            for j in range((posy-150), (posy), sampling) :
                #print ("scan "+str(i)+","+str(j)+" : "+str(nav_map.get_content(i,j)))
                content = str(nav_map.get_content(i,j))
                state[convert_content(content)] += 1
    
    elif (angle >= -65 and angle <-23) :
        for i in range(posx-10, posx + 120, sampling) :
           for j in range((posy-25)-(posx-i), (posy+25)-(posx-i), sampling) :
               #print ("scan "+str(i)+","+str(j)+" : "+str(nav_map.get_content(i,j)))
               content = str(nav_map.get_content(i,j))
               state[convert_content(content)] += 1
    print(state)
    return state #function returns the state cozmo is in


    
def convert_content (content) : #to decide whether cozmo should turn or go straight
    if(content == "NodeContentTypes.ClearOfObstacle" or content == "NodeContentTypes.ClearOfCliff") :
        return 1 #NO OBSTACLE BLOCK IS GREEN
    elif(content == "NodeContentTypes.Unknown") :
        return 0 #NOT SURE OF THE STATE
    else :
        return 2 #THERE IS AN OBSTACLE
    
cozmo.run_program(cozmo_program, use_3d_viewer=True, use_viewer=True)
