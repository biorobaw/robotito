#!/usr/bin/env python  

import rospy 
import tf
from geometry_msgs.msg import Pose2D

map_frame = 'map'
marker_frame = 'ar_marker_0'
cam1frame = 'stingray1'
cam2frame = 'stingray2'
MAX_BLACKOUT = .2

if __name__ == "__main__":
  # Initialize TF listener
  rospy.init_node('hover')

  listener = tf.TransformListener(1)
  tf_pub = tf.TransformBroadcaster()

  # Initialize cmd_vel publisher
  pose_pub = rospy.Publisher('/robotito/pose', Pose2D, queue_size=1)

  # Control loop
  rate = rospy.Rate(50.0)
  while not rospy.is_shutdown():
    # Get oldest timestamp for transform
    latest_cam1 = None
    latest_cam2 = None
    try:
      latest_cam1 = listener.getLatestCommonTime(map_frame, cam1frame + '/' + marker_frame)
    except (tf.Exception):
      pass
    try:
      latest_cam2 = listener.getLatestCommonTime(map_frame, cam2frame + '/' + marker_frame)
    except (tf.Exception):
      pass
    
    # if there is at least one camera we can use
    if ((latest_cam1 != None and 
        rospy.Time.now() - latest_cam1 < rospy.Duration(MAX_BLACKOUT)) or 
        (latest_cam2 != None and
        rospy.Time.now() - latest_cam2 < rospy.Duration(MAX_BLACKOUT))):
      # If only seeing cam1 or cam2, use that one
      if ((latest_cam1 != None and 
          rospy.Time.now() - latest_cam1 < rospy.Duration(MAX_BLACKOUT))):
        frame_to_use = cam1frame
        time_to_use = latest_cam1
      elif ((latest_cam2 != None and 
          rospy.Time.now() - latest_cam2 < rospy.Duration(MAX_BLACKOUT))):
        frame_to_use = cam2frame
        time_to_use = latest_cam2
      # If both are valid, we have to choose one      
      else:
        (trans_c1,rot_c1) = listener.lookupTransform(map_frame, cam1frame + '/' + marker_frame, latest_cam1)
        if (trans_c1[0] > 0):
          frame_to_use = cam1frame
          time_to_use = latest_cam1
        else:
          frame_to_use = cam2frame
          time_to_use = latest_cam2
        
      try:
        # Obtain the transform using the selected camera
        if (time_to_use != None):
          (trans,rot) = listener.lookupTransform(map_frame, frame_to_use + '/' + marker_frame,  time_to_use)
          # Publish that transform to the marker for visualization
          tf_pub.sendTransform(trans, rot, time_to_use, marker_frame, map_frame)

          # Send the transform as a msg too for java nodes - 2d

          p = Pose2D()
          p.x = trans[0]
          p.y = trans[1]
          euler = tf.transformations.euler_from_quaternion(rot)
          p.theta = euler[2]
           
          pose_pub.publish(p)
      except (tf.ExtrapolationException):
        pass
            
    rate.sleep()

  
