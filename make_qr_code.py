import qrcode
import os

try:
	os.chdir(os.getcwd()+'\\qrcodes')
except:
	os.mkdir(os.getcwd()+'\\qrcodes')
	os.chdir(os.getcwd()+'\\qrcodes')

def create_qr_code(item, quanity, to='hoganpy3@gmail.com'):
	img = qrcode.make(f'MATMSG:TO:{to};SUB:{item};BODY:{quanity};;')
	img.save(f'{item.lower()}.png')

	os.chdir('..')
print('\nHello.\n') 
print('Welcome to the QR scanner. This program will generate a QR code based off of the inputs you give it.')
print('This program will also store the qr codes in a folder for your future use.\n\n')

description = input('What is the name of the item you\'d like to create a QR code for?\n')
quanity = input('And how many of this item do you wish to log?\n')


#change email address in this function to change email address associated with QR code.
create_qr_code(description, quanity, 'hoganpy3@gmail.com')




