import os
import importlib
from grabber_modules import Grabber_base

print(
 """
	██████╗  █████╗ ██████╗      ██╗██████╗ ███████╗ ██████╗    
	██╔══██╗██╔══██╗██╔══██╗     ██║██╔══██╗██╔════╝██╔════╝    
	██████╔╝███████║██████╔╝     ██║██████╔╝█████╗  ██║  ███╗   
	██╔══██╗██╔══██║██╔══██╗██   ██║██╔═══╝ ██╔══╝  ██║   ██║   
	██║  ██║██║  ██║██║  ██║╚█████╔╝██║     ███████╗╚██████╔╝   
	╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚════╝ ╚═╝     ╚══════╝ ╚═════╝    
	                                                            
	███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
	██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
	███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
	╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
	███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
	╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                                                        	""")


def input_in_range(prompt, error_message='Input not in range', min=0, max=0):
	inpt = int(input(prompt))
	while (inpt > max and max > min) or inpt < min:
		print(error_message)
		inpt = int(input('> '))
	return inpt

index = 1

print("Choose module to download images:")

for module in Grabber_base.modules:
	print('[{0}]: {1}'.format(index, module.module_description))
	index += 1

choise = input_in_range('> ', min=1, max=len(Grabber_base.modules))

grabber_module = Grabber_base.modules[choise-1]()

print('Files will be downloaded and tested in blocks to speed up the process')
block_number = input_in_range('Number of blocks to download (0 to download unlimited): ', error_message='Number must be larger or equal to 0')

grabber_options = grabber_module.setup()

i = 0
while i < block_number or block_number == 0:
	print("Downloading block {0}..".format(i+1))
	os.mkdir('block_{0}'.format(i))
	grabber_module.run(grabber_options, 'block_{0}'.format(i))
	os.system('python ./rarjpeg-master/find_rarjpeg.py target/{0} -e'.format(i+1))
	i += 1