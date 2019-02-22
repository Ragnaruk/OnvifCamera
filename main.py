from camera import Camera

cam = Camera()

# Move to the right
cam.move_pan(1, 1)

# Move to the left
cam.move_pan(-1, 1)

# Move downwards
cam.move_tilt(-1, 1)

# Move upwards
cam.move_tilt(1, 1)

# Zoom in
cam.move_zoom(1, 1)

# Zoom out
cam.move_zoom(-1, 1)
