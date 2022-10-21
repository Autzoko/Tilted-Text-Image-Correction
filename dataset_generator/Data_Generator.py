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

def read_images(dir, name):
	img = cv2.imread(dir + name + '.png')
	return img

def rotate_image(img, points, range_start=-50, range_end=50):
	rotated_points = []
	for point in points:
		rotated_points.append((point[0] + random.randint(range_start, range_end), point[1] + random.randint(range_start, range_end)))
	
	H = (np.float32(points), np.float32(rotated_points))
	H_inverse = inv(H)

	size = points[0].shape

	warped_image = cv2.warpPerspective(img, H_inverse, size)

	return warped_image, rotated_points


def generate_dataset(resized_img_dir, point_data_path, num):
	if(number_match(resized_img_dir, point_data_path)):
		img_name_list = os.listdir(resized_img_dir)
		warped_points_outfile = open('./data/out/points/warped_points.txt', 'a')
		for img_name in img_name_list:
			img = read_images(resized_img_dir, img_name)
			points = read_pointData(point_data_path)

			for i in range(num):
				warped_img, rotated_points = rotate_image(img, points)
				cv2.imwrite('./data/out/warped_images/' + 'warped_image_' + str(i) + '.png', warped_img)
				points_string = str(rotated_points[0]) + ';' + str(rotated_points[1]) + ';' + str(rotated_points[2]) + ';' + str(rotated_points[3]) + '\n'
				warped_points_outfile.write(points_string)







if __name__ == '__main__':
	point_data_path = './data/input/points/points_1.txt'
	img_dir = './data/input/images/'
	resized_img_dir = './data/input/images/resized_images/'

	if(number_match(img_dir, point_data_path)):
		print(read_pointData(point_data_path))

	else:
		print("NUMBER OF IMAGES AND LENGTH OF POINTS SET DISMATCHED!\n")
	

		




