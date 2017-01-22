#!/usr/bin/env python
import sys
import os

import rospy
from std_msgs.msg import String 

is_first = True

def cat(msg, pub):
	global is_first
	if msg.data == "OK":
		print("your turn!")
		s = raw_input()
		pub.publish(s)
	elif msg.data == "win":
		os.system("banner youwin!")
	elif msg.data == "lose":
		os.system("banner youlose!")

	elif msg.data == "NG":
		print("can not put here!\ntry again!")
		s = raw_input()
		pub.publish(s)
	elif msg.data == "error":
		print("input error!\ntry again!")
		s = raw_input()
		pub.publish(s)
	elif msg.data == "first" and is_first:
		is_first = False
		print("first your turn!")
		s = raw_input()
		pub.publish(s)

	elif msg.data == "first":
		pass
	else:
		os.system("clear")
		print(msg.data)

def main():	
	rospy.init_node(sys.argv[1])
	pub = rospy.Publisher(sys.argv[1] + '_set', String, queue_size = 1)
	sub = rospy.Subscriber(sys.argv[1] + '_cat', String, cat, callback_args = pub)
	rospy.spin()
	
if __name__ == "__main__":
	main()
