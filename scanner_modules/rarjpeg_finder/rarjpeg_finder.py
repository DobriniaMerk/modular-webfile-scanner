import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)))) # adds current directory to PATH for importing; ugly
from rarjpeg import Rarjpeg

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # ugly but needed
import scanner_modules

class Scanner(scanner_modules.Scanner_base):
	module_description = "RarjpegScanner\nScans images for hidden archives"

	def run(self, args, workdir):
		found = 0
		extracted = 0
		passworded = 0
		if os.path.isdir(workdir):
			for file in os.listdir(dirpath):
				rarjpeg = Rarjpeg(rarjpeg_path)
				valid = rarjpeg.is_valid

				if not args[0]:   # only test
					if valid:
						if args[1] > 0:
							print(f"{file} is valid")
						found += 1
					elif args[1] > 1:
						print(f"{file} is invalid")
				else:             # extract
					extracted, msg = rarjpeg.extract()
					if(extracted):
						if args[1] > 0:
							print(f"{file} extracted successfully")
						extracted += 1
						found += 1
					elif "password" in msg:
						print(f"{file} contains archive, but requires password to extract")
						passworded += 1
						found += 1
					elif args[1] > 1:
						print(f"{file} contains no archive")

			if args[1] > 0:
				print("Scan finished")
				print(f"Scanned {len(os.listdir(dirpath))} files")
				print(f"Found {found} archives")
				print(f"Extracted {extracted} ", end='')
				if args[0]:
					print(f'with {passworded} of them locked by a password')
					path = os.path.join(os.getcwd(), "extracted_rarjpegs")
					print(f"Extracted files can be found in {path}")
				print()

	def setup(self):
		extract = lower(input("Should files be extracted if arcive is found or only messaged [y/(n)]: ")) == 'y'
		loglevel = min(max(0, int(input("Logging level (0 - no logging at all; 1 - log only successfull; 2 - log all): "))), 2)
		return (extract, loglevel)