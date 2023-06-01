#!/usr/bin/env python3 
import os, sys

import random
import hashlib
import argparse

import requests, requests.exceptions

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grabber_modules

def input_in_range(prompt, error_message='Input not in range', min=0, max=0):
	inpt = int(input(prompt))
	while (inpt > max and max > min) or inpt < min:
		print(error_message)
		inpt = int(input('> '))
	return inpt

class Grabber(grabber_modules.Grabber_base):
	"""class container for all code; needed for importing into main program"""

	module_description = 'RandomImgur\nRandom images from imgur (DobriniaMerk; base by umahmood)'

	def __init__(self):
		pass

	def get_image_url(self, ext = "jpg"):
		"""
		Builds an imgur url in the form http://i.imgur.com/{5 characters}.{ext}. 

		@return: (tuple) - url (string), file name (string) 
		"""
		base_url = "http://i.imgur.com/"
		r1 = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
		r2 = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
		r3 = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
		r4 = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
		r5 = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

		file_name = r1 + r2 + r3 + r4 + r5 
		full_url = base_url + file_name + "." + ext

		return (full_url, file_name)

	def is_placeholder_image(self, img_data):
		"""
		Checks for the placeholder image. If an imgur url is not valid (such as 
		http//i.imgur.com/12345.jpg), imgur returns a blank placeholder image. 

		@param: img_data (bytes) - bytes representing the image.

		@return: (boolean) True if placeholder image otherwise False
		"""
		sha256_placeholder = "9b5936f4006146e4e1e9025b474c02863c0b5614132ad40db4b925a10e8bfbb9"
		m = hashlib.sha256()
		m.update(img_data)
		return 	m.hexdigest() == sha256_placeholder

	def save_image(self, download_dir, file_name, file_ext, img_data):
		"""
		Saves an image to the download directory with a given file name and extension.

		@param: img_data     (bytes) - bytes representing the image.
		@param: file_name    (string) - name to the save the file as i.e. foo.jpg.
		@param: download_dir (string) - path to the download directory.

		@return: None
		"""
		try:
			file_path = "{0}{1}{2}.{3}".format(download_dir, os.sep, file_name, file_ext)
			with open(file_path, "wb") as f:
				f.write(img_data)
		except FileNotFoundError as e:
			raise e

	def download_image(self, url):
		"""
		Downloads an image from imgur.

		@param: url (string) - Imgur url to download i.e. http://i.imgur.com/1a2b3c.jpg.

		@return: None if the download fails else images binary data and content type.
		"""
		try:
			r = requests.get(url)
			if not r.ok:
				return None
			sub_type = r.headers["content-type"][6:] # turns image/gif to gif
			file_type = "jpg" if sub_type not in ["gif", "webm", "png"] else sub_type
			return r.content, file_type
		except (exceptions.ConnectionError, exceptions.HTTPError) as e:
			pass

	def run(self, args, workdir):
		"""
		args consists of {img_num, verbose}
		"""
		count = 0
		while count < args[0]:
			imgur_url, file_name = self.get_image_url()
			img_data, file_type = self.download_image(imgur_url)
			if not img_data or self.is_placeholder_image(img_data):
				continue
			self.save_image(workdir, file_name, file_type, img_data)
			if args[1]: print('Downloaded image', imgur_url)
			count += 1

	def setup(self):
		print('imgur_grabber settings:')
		block_size = input_in_range('Number of images in one block: ', error_message='Size must be larger than 0', min=1)
		verb = (input('Should every downloaded image be announced [Y/(N)]: ').upper() == 'Y')
		return (block_size, verb)
