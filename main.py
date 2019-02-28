from camera import Camera
import credentials
from time import sleep

# --------------------------------------------------

cam_42 = Camera(
    credentials.ip42,
    credentials.port,
    credentials.login,
    credentials.password
)

# cam.get_debug_info()

# --------------------------------------------------

cam_42.get_ptz_position()
sleep(5)

# --------------------------------------------------

# Absolute Move
cam_42.move_absolute(0.1, -0.5, 1)
sleep(3)

# --------------------------------------------------

cam_42.get_ptz_position()

# --------------------------------------------------

# Absolute Move
cam_42.move_absolute(0, 0, 0)
sleep(3)

# --------------------------------------------------

cam_42.get_ptz_position()

# --------------------------------------------------

sleep(6)

# --------------------------------------------------

cam_43 = Camera(
    credentials.ip43,
    credentials.port,
    credentials.login,
    credentials.password
)

# cam.get_debug_info()

# --------------------------------------------------

# Continuous Move
cam_43.move_continuous_custom(-2, 1, 1, 2, 0.5, 1)

# --------------------------------------------------

cam_43.get_focus_options()

# --------------------------------------------------

# Focus change

cam_43.change_focus_continuous(-0.5, 1)

sleep(5)

cam_43.change_focus_continuous(0.5, 1)

sleep(5)

# Not working
cam_43.change_focus_absolute(0.5, 1)
