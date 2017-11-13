import cozmo, time, asyncio
from cozmo.util import degrees, Pose, distance_mm, speed_mmps
faces_mem = []

def cozmo_program(robot: cozmo.robot.Robot) :
    robot.world.request_nav_memory_map(0.5)
    deg = 45
    mode = 0

    cozmo.faces.erase_all_enrolled_faces(robot.conn)
    robot.say_text("Remember Mode").wait_for_completed()
    while(True): 
        faces_mem.append('a')
        print("do the loop")

        try :
            print ("Check mode")
            robot.world.wait_for_observed_light_cube(timeout=5)
            print("Found lightcube")
            if(mode == 0) :
                mode = 1
                print("Op")
                robot.say_text("Operation Mode").wait_for_completed()
            else :
                mode = 0
                print("Re")
                robot.say_text("Remember Mode").wait_for_completed()
        except asyncio.TimeoutError :
            print("Didn't find a cube")


        if(mode == 0) :
            try :
                print ("Do faces detection")
                robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
                face_event = robot.world.wait_for(cozmo.faces.EvtFaceObserved, timeout=5)
                print("Face found %s" %face_event.face.face_id)
                if not(face_event.face.face_id in faces_mem) :
                    robot.say_text("Hi").wait_for_completed()
                    faces_mem.append(face_event.face.face_id)
                
            except asyncio.TimeoutError :
                print("Not found any new face")
                
        else :
            
            try :
                print ("Do faces detection")
                robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
                face_event = robot.world.wait_for(cozmo.faces.EvtFaceObserved, timeout=5)
                print("Face found %s" %face_event.face.face_id)
                if not(face_event.face.face_id in faces_mem) :
                    robot.say_text("I don't know you").wait_for_completed()
                
            except asyncio.TimeoutError :
                print("Not found any new face")
        
                


        try :
            print ("Do objects detection")
            robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE / 2).wait_for_completed()
            event = robot.world.wait_for(cozmo.nav_memory_map.EvtNewNavMemoryMap, timeout=2)
            #print ("event = %s" % event)
            nav_map = event.nav_memory_map

            _posX = robot.pose.position.x
            _posY = robot.pose.position.y
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
        return faces_mem


def scan_block (posx, posy, angle, nav_map) :
    posx = int(posx)
    posy = int(posy)
    state = [0,0,0]
    sampling = 7
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
    return state


    
def convert_content (content) :
    if(content == "NodeContentTypes.ClearOfObstacle" or content == "NodeContentTypes.ClearOfCliff") :
        return 1
    elif(content == "NodeContentTypes.Unknown") :
        return 0
    else :
        return 2
cozmo.run_program(cozmo_program, use_3d_viewer=False, use_viewer=False)
