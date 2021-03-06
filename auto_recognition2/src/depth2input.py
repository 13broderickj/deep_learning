#!/usr/bin/env python2

# MIT License
#
# Copyright (c) 2016 Zhiang Chen

'''
Receive the depth image from "depth_image", and crop the image by a 34x34 window. 
Then publish the cropped image to "cropped_depth_image" with 10hz.
'''
from __future__ import print_function
import rospy
import roslib
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import matplotlib.pyplot as plt
import numpy as np
import sys


lf_x = rospy.get_param("tplf_x")
lf_y = rospy.get_param("tplf_y")
rt_x = rospy.get_param("btrt_x")
rt_y = rospy.get_param("btrt_y")
image_size = rospy.get_param("image_size")

class image_converter:

	def __init__(self):
		'''Initialize ros publisher, subscriber'''
		self.pub = rospy.Publisher('/cropped_depth_image',Image,queue_size=1)
		self.sub = rospy.Subscriber('/depth_image',Image,self.callback,queue_size=1)
		self.bridge = CvBridge()
		rospy.loginfo("Initialized!")

	def callback(self,data):
		cv_image = self.bridge.imgmsg_to_cv2(data, desired_encoding="mono8")
		cropped_image = cv2.resize(cv_image[lf_y:rt_y,lf_x:rt_x],(image_size,image_size))
		#cv2.imwrite('cropped_image.bmp',cropped_image)
		ros_image = self.bridge.cv2_to_imgmsg(cropped_image, encoding="mono8")
		self.pub.publish(ros_image)

if __name__ == '__main__':
	rospy.init_node('depth2input',anonymous=True)
	ic = image_converter()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down ROS node depth2input")
