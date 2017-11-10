import cozmo, time, asyncio
from cozmo.util import degrees, Pose, distance_mm, speed_mmps
from PIL import Image

def cozmo_take_pic(robot: cozmo.robot.Robot) :
    cozmo.camera.Camera.image_stream_enabled = True
    latest_image = robot.world.latest_image
    img = latest_image.annotate_image()
    print (latest_image)
    img.show()


cozmo.run_program(cozmo_take_pic,use_viewer=True)
