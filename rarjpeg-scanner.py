import os

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


modules_dir = "./modules"

modules = []

index = 1

print("Choose module to download images:")

for module_name in os.listdir(modules_dir):
	module = os.path.join(modules_dir, module_name)
	if os.path.isfile(module):
		modules.append(module)
		print('[{0}]: '.format(index), end='')
		lines = os.popen('python ' + module).readlines()
		for line in lines:
			print(line, end='')
		index += 1

choise = input_in_range('> ', min=1, max=len(modules))

print('Images will be downloaded and tested in blocks to speed up the process')

block_size = input_in_range('Size of one block: ', error_message='Size must be larger than 0', min=1)
block_number = input_in_range('Number of blocks to download (0 to download unlimited): ', error_message='Number must be larger or equal to 0')


i = 0
while i < block_number or block_number == 0:
	print("Downloading block {0}..".format(i+1))
	os.system('python {0} --num {1} --dir ./target/{2}'.format(modules[choise-1], block_size, i+1))
	os.system('python ./rarjpeg-master/find_rarjpeg.py target/{0} -e'.format(i+1))
	i += 1