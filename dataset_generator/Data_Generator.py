import matplotlib.pyplot as plt
import cv2
import random
import numpy as np
from numpy.linalg import inv
import os
import re


def read_resize(path, image_name, size=(400, 300)):
	img = cv2.imread(path + image_name + '.png')
	img = cv2.resize(img, size)

	resized_name = image_name + '_resized.png'
	cv2.imwrite(read_path + 'resized/' + resized_name, img)


def read_pointData(filepath):
	point_set = []
	datafile = open(filepath, 'r')
	for line in datafile:
		tmp = line.split(';')
		cord_list = []
		for str in tmp:
			_cord = re.findall("\d+", str)
			a = int(_cord[0])
			b = int(_cord[1])
			cord_list.append((a, b))

		point_set.append(cord_list)

	datafile.close()
	return point_set

def number_match(img_dir, point_file):
	num_img = 0;
	file = open(point_file, 'r')
	num_pointset = len(file.readlines())
	file.close()

	for dirpath, dirnames, filenames in os.walk(img_dir):
		num_img = len(filenames)
	
	if num_img == num_pointset:
		return True
	else:
		return False


if __name__ == '__main__':
	point_data_path = './data/input/points/points_1.txt'
	img_dir = './data/input/images/'

	if(number_match(img_dir, point_data_path)):
		print(read_pointData(point_data_path))

	else:
		print("NUMBER OF IMAGES AND LENGTH OF POINTS SET DISMATCHED!\n")

		




