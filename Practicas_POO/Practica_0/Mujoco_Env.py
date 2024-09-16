import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
import cv2

import time


# For callback functions
button_left = False
button_middle = False
button_right = False
lastx = 0
lasty = 0

# More legible printing from numpy.
np.set_printoptions(precision=3, suppress=True, linewidth=100)

xml_path = ["a1/xml/a1.xml", 
            "XML/test.xml", 
            "XML/Env.xml", 
            "", 
            ""][2]
simend = 10

def initMuJoCo():
    global model, data, scene, cam, window, opt, context

    # MuJoCo data structures
    model = mj.MjModel.from_xml_path(xml_path)  # MuJoCo model
    data = mj.MjData(model)                # MuJoCo data
    cam = mj.MjvCamera()                        # Abstract camera
    opt = mj.MjvOption()                        # visualization options

    # Init GLFW, create window, make OpenGL context current, request v-sync
    glfw.init()
    window = glfw.create_window(1200, 900, "Demo", None, None)
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    # initialize visualization data structures
    mj.mjv_defaultCamera(cam)
    mj.mjv_defaultOption(opt)
    scene = mj.MjvScene(model, maxgeom=10000)
    context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150.value)

    # install GLFW mouse and keyboard callbacks
    glfw.set_key_callback(window, keyboard)
    glfw.set_cursor_pos_callback(window, mouse_move)
    glfw.set_mouse_button_callback(window, mouse_button)
    glfw.set_scroll_callback(window, scroll)

def keyboard(window, key, scancode, act, mods):
    if act == glfw.PRESS and key == glfw.KEY_BACKSPACE:
        mj.mj_resetData(model, data)
        mj.mj_forward(model, data)
        # Reset to initial joint angles after reset
        for i in range(len(initial_joint_angles)):
            data.qpos[i] = initial_joint_angles[i]
        mj.mj_forward(model, data)

def mouse_button(window, button, act, mods):
    global button_left, button_middle, button_right
    # update button state
    button_left = (glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS)
    button_middle = (glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS)
    button_right = (glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS)

def mouse_move(window, xpos, ypos):
    global lastx, lasty
    # compute mouse displacement, save
    dx = xpos - lastx
    dy = ypos - lasty
    lastx = xpos
    lasty = ypos

    # no buttons down: nothing to do
    if not button_left and not button_middle and not button_right:
        return

    # get current window size
    width, height = glfw.get_window_size(window)

    # get shift key state
    mod_shift = (glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS or
                 glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS)

    # determine action based on mouse button
    if button_right:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_MOVE_H
        else:
            action = mj.mjtMouse.mjMOUSE_MOVE_V
    elif button_left:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_ROTATE_H
        else:
            action = mj.mjtMouse.mjMOUSE_ROTATE_V
    else:
        action = mj.mjtMouse.mjMOUSE_ZOOM

    mj.mjv_moveCamera(model, action, dx/height, dy/height, scene, cam)

def scroll(window, xoffset, yoffset):
    action = mj.mjtMouse.mjMOUSE_ZOOM
    mj.mjv_moveCamera(model, action, 0.0, -0.05 * yoffset, scene, cam)

# ----------------------------------------------------------


initMuJoCo()

# Set initial angles of the joints
initial_joint_angles = [0, 0, 0, 0, 0, 0]  # Replace with your desired initial angles
current_joint_angles = initial_joint_angles.copy()

#for i in range(len(current_joint_angles)):
#    data.qpos[i] = current_joint_angles[i]

# Set camera configuration
cam.azimuth = 89.608063
cam.elevation = -11.588379
cam.distance = 5.0
cam.lookat = np.array([0.0, 0.0, 0.0])  # Centering the camera on the origin

# use forward kinematics to set the position
mj.mj_forward(model, data)


realRobot = False


while not glfw.window_should_close(window):

    #current_joint_angles =  np.radians(ik_result)


    #for i in range(len(current_joint_angles)-1):
    #    data.qpos[i] = current_joint_angles[i]

    mj.mj_step(model, data)
   
    mj.mj_forward(model, data)

    # Get and print the current joint angles
    #current_joint_angles = data.qpos[:len(initial_joint_angles)]
    #print("Current Joint Angles:", current_joint_angles)

    # get framebuffer viewport
    viewport_width, viewport_height = glfw.get_framebuffer_size(window)
    viewport = mj.MjrRect(0, 0, viewport_width, viewport_height)

    # Update scene and render
    mj.mjv_updateScene(model, data, opt, None, cam, mj.mjtCatBit.mjCAT_ALL.value, scene)
    mj.mjr_render(viewport, scene, context)

    # Capture the image from the framebuffer
    rgb_buffer = np.zeros((viewport_height, viewport_width, 3), dtype=np.uint8)
    mj.mjr_readPixels(rgb_buffer, None, viewport, context)
    rgb_image = cv2.cvtColor(rgb_buffer, cv2.COLOR_RGB2BGR)

    # Process the image with OpenCV (example: convert to grayscale and detect edges)
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, 100, 200)

    # Show the processed image
    #cv2.imshow("Processed Image", gray_image)
    
    # swap OpenGL buffers (blocking call due to v-sync)
    glfw.swap_buffers(window)

    # process pending GUI events, call GLFW callbacks
    glfw.poll_events()

glfw.terminate()