## Problem
Creating a hardware-software system to control the movement of a "pan & tilt" system with an attached video camera🎥 in order to track an object (a ping-pong ball 🏓) within the area of interest.
## Solution
### Hardware development
1. I have cut the axes for the camera mount.
2. I have installed the servo motors that provide mobility.
3. Connecting the servo-motors to the Raspberry Pi board.
4. Mounting the camera on the holder.
**Photos**

![Picture3](https://github.com/AgacheAndrei/hackathon-aciee-2021-1st-place/assets/36128809/d57adf3b-1573-4f89-8747-2c8f1b3eb693)
![Picture4](https://github.com/AgacheAndrei/hackathon-aciee-2021-1st-place/assets/36128809/195c0ac2-7db0-4352-bcb7-a51a441e1617)

### Sofware development
1. Developing the code for controlling the servo motors' movement. 
   <pre>
     Library: RPI.GPIO 
     Setting the initial position: 90°x-90°y 
     Moving the servos based on the object's position 
     Tracking the object within given parameters (500x500)

   </pre>
     ![image5](https://github.com/AgacheAndrei/hackathon-aciee-2021-1st-place/assets/36128809/e180c679-c8bc-4c19-8cf0-1e223e1e097b)

2. Developing the code for object motion detection.
   <pre>
     Libraries: OpenCV, NumPy, Collections, Imutils, argparse, time
     Detection of object color range
     Image processing for efficient object detection
     Object detection based on color and shape
     Displaying the object's trajectory and its position graphically
     **For the video demo go to -> demo_software.gif
     **For the video demo where the system of tracking the trajectory can be seen better go to -> demo_software_2.mp4
   </pre>
3. Integration of codes for simultaneous execution of functions.
   <pre>
    Real-time detection of the ball using the Raspberry Pi camera and tracking it with the Pan Tilt assembly.
    For the video demo go to -> demo_final_full_integration.mp4
   </pre>
