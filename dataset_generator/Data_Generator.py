import matplotlib.pyplot as plt
import cv2
import random
import numpy as np
from numpy.linalg import inv
import os
import re


def read_resize(path, image_name, size=(400, 300)):
	img = cv2.imread(path + image_name)
	img = cv2.resize(img, size)

	_name = image_name.split('.')
	pure_name = _name[0]
	cv2.imwrite('./data/input/images/resized_images/resized_' + pure_name + '.png', img)


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
	img = cv2.imread(dir + name)
	return img

def rotate_image(img, points, range_start=-50, range_end=50):
	rotated_points = []
	points_list = []
	for point in points:
		tmp_point0 = point[0] + random.randint(range_start, range_end)
		tmp_point1 = point[1] + random.randint(range_start, range_end)

		rotated_points.append([tmp_point0, tmp_point1])
		points_list.append([point[0], point[1]])
	
	H = cv2.getPerspectiveTransform(np.array(points_list, dtype="float32"), np.array(rotated_points, dtype="float32"))


	warped_image = cv2.warpPerspective(img, H, (400, 300))

	return warped_image, rotated_points


def generate_dataset(resized_img_dir, point_data_path, num_per_img=50):
	if(number_match(resized_img_dir, point_data_path)):
		img_name_list = os.listdir(resized_img_dir)
		warped_points_outfile = open('./data/out/points/warped_points.txt', 'a')
		img_index = 0;
		num = 0;
		for img_name in img_name_list:
			img = read_images(resized_img_dir, img_name)
			points = read_pointData(point_data_path)

			for i in range(num_per_img):
				warped_img, rotated_points = rotate_image(img, points[img_index], range_start=-25, range_end=25)
				cv2.imwrite('./data/out/warped_images/' + 'warped_image_' + str(num + i) + '.png', warped_img)
				points_string = str(rotated_points[0]) + ';' + str(rotated_points[1]) + ';' + str(rotated_points[2]) + ';' + str(rotated_points[3]) + '\n'
				warped_points_outfile.write(points_string)
			
			num += num_per_img
			
			img_index += 1
		
		return "Dataset generated!\n"
	else:
		return "Points data dismatch image number, please complete the data of resized image pivot points!\n"







if __name__ == '__main__':
	point_data_path = './data/input/points/points_1.txt'
	img_dir = './data/input/images/text_images/'
	resized_img_dir = './data/input/images/resized_images/'

	img_names = os.listdir(img_dir)
	for img_name in img_names:
		read_resize(img_dir, img_name)
	
	print(generate_dataset('./data/input/images/resized_images/', './data/input/points/points_1.txt', num_per_img=1000))

	

		




