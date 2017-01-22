#!/usr/bin/env python
import rospy
from std_msgs.msg import String 
import os

import numpy as np

import othello

model = othello.othello()
is_first = True

def put(msg, args):
	p = args[0]
	pub = args[1]
	global is_first
	is_first = False
	msg = msg.data.split(" ")
	if len(msg) == 2:
		log_msg = model.set(msg[0], msg[1], p)
		print("{0}-{1} {2}".format(model.white_cnt, model.brack_cnt,model.brank_cnt))
		if log_msg == 10:
			model.cat()
			pub[0].publish(model.board_str)
			pub[1].publish(model.board_str)
			res = [model.brack_cnt, model.white_cnt]
			winner = np.argmax(res)
			pub[winner].publish("win")
			pub[-1*(winner - 1)].publish("lose")
			os.system("banner {0}-{1}".format(res[0],res[1]))
			
		elif log_msg == 0:
			model.cat()
			nexts = model.next
			pub[0].publish(model.board_str)
			pub[1].publish(model.board_str)
			pub[int(-1 * (nexts + 1)/2)].publish("OK")
		elif log_msg == 1:
			pub[int(-1 * (model.next + 1)/2)].publish("NG")
		else:
			pub[int(-1 * (model.next + 1)/2)].publish("error")

def main():	
	rospy.init_node('sever')
	p1_pub = rospy.Publisher('p1_cat', String, queue_size = 2)
	p2_pub = rospy.Publisher('p2_cat', String, queue_size = 2)
	p1_sub = rospy.Subscriber('p1_set', String, put, callback_args = [-1, [p1_pub, p2_pub]])
	p2_sub = rospy.Subscriber('p2_set', String, put, callback_args = [1, [p1_pub, p2_pub]])
	while is_first:
		p1_pub.publish("first")
	rospy.spin()
	
if __name__ == "__main__":
	main()
