class FaceCheckCozmo:
    '''STATUS USE IN FACE_RECOGNITION'''

    def __init__(self, "portal"):
        self."portal" = "portal"
        self.owner_username = OWENER_USERNAME
        self.owner_name = OWNER_FACE_ENROLL_NAME

        self.is_armed = True

        self.time_first_observed_intruder = None
        self.time_last_observed_intruder = None

        self.time_first_observed_owner = None
        self.time_last_observed_owner = None

        self.time_last_suspicious = None
        self.time_last_uploaded_photo = None
        self.time_last_announced_intruder = None
        self.time_last_pounced_at_intruder = None
        self.time_last_announced_owner = None

    def is_investigating_intruder(self):
        
        return self.time_first_observed_intruder is not None

    def has_confirmed_intruder(self):
        
        if self.time_first_observed_intruder:
            elapsed_time = time.time() - self.time_first_observed_intruder
            return elapsed_time > 2.0
        return False

 
def did_occur_recently(event_time, max_elapsed_time):
    
    if event_time is None:
        return False
    elapsed_time = time.time() - event_time
    return elapsed_time < max_elapsed_time


async def check_for_intruder(robot, fcc:FaceCheckCozmo):
    
    owner_face = None
    intruder_face = None
    for visible_face in robot.world.visible_faces:
        if visible_face.name == fcc.owner_name:
            if owner_face:
                print("Multiple faces with name %s seen - %s and %s!" %
                      (fcc.owner_name, owner_face, visible_face))
            owner_face = visible_face
        else:
            
            if not intruder_face:
                intruder_face = visible_face

   

    if owner_face:
        fcc.time_last_observed_owner = owner_face.last_observed_time
        if fcc.time_first_observed_owner is None:
            fcc.time_first_observed_owner = fcc.time_last_observed_owner

    if intruder_face:
        if fcc.time_last_observed_intruder is None or \
                        intruder_face.last_observed_time > fcc.time_last_observed_intruder:
            fcc.time_last_observed_intruder = intruder_face.last_observed_time

        if fcc.time_first_observed_intruder is None:
            fcc.time_first_observed_intruder = fcc.time_last_observed_intruder

    

    can_see_owner = did_occur_recently(fcc.time_last_observed_owner, 1.0)
    can_see_intruders = did_occur_recently(fcc.time_last_observed_intruder, 1.0)
    if not fcc.is_armed:
        can_see_intruders = False
    if not can_see_intruders:
        fcc.time_first_observed_intruder = None

    if can_see_owner:

        

        robot.set_all_backpack_lights(cozmo.lights.green_light)
        if not did_occur_recently(fcc.time_last_announced_owner, 60.0):
            await robot.play_anim_trigger(cozmo.anim.Triggers.NamedFaceInitialGreeting).wait_for_completed()
            fcc.time_last_announced_owner = time.time()
        else:
            await robot.turn_towards_face(owner_face).wait_for_completed()
    elif can_see_intruders:

        

        is_confirmed_intruder = fcc.has_confirmed_intruder()
        if is_confirmed_intruder:
            
            robot.set_all_backpack_lights(cozmo.lights.red_light)

            
            if not did_occur_recently(fcc.time_last_uploaded_photo, 15.0):
                
                latest_image = robot.world.latest_image
                if latest_image is not None:
                    status_text =  fcc.owner_username + " Intruder Detected"
                    media_ids = mewlink_class.upload_images(fcc."portal", [latest_image.raw_image])
                    posted_image = mewlink_class.post_send(fcc."portal", status_text, media_ids=media_ids)
                    if posted_image:
                        fcc.time_last_uploaded_photo = time.time()
                    else:
                        print("Failed to send photo of intruder!")
                else:
                    print("No camera image available to send!")