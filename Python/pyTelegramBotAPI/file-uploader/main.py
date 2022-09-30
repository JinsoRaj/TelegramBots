import sys
import os
import tqdm
import requests
import argparse
import configparser
import requests_toolbelt

config = configparser.ConfigParser()
config.read('config.ini')
chat_id = config['Telegram']['chat_id']
bot_token = config['Telegram']['bot_token']

class ProgressBar(tqdm.tqdm):
	def update_to(self, n: int) -> None:
		self.update(n - self.n)

def url(bot_token:str):
	url = f'https://api.telegram.org/bot{bot_token}/getMe'
	return url

def upload_url(bot_token:str):
	url = f'https://api.telegram.org/bot{bot_token}/sendDocument'
	return url

def upload_file(bot_token:str, chat_id:str, file_name:str, caption:str=None):

	file_size = os.path.getsize(file_name)

	if file_size > 51200000:
		sys.exit("Bot can upload only 50 MB file.")
	data_to_send = []
	session = requests.session()

	with open(file_name, "rb") as fp:
		data_to_send.append(
			("document", (file_name, fp))
		)
		data_to_send.append(('chat_id', (chat_id)))
		data_to_send.append(('caption', (caption)))
		encoder = requests_toolbelt.MultipartEncoder(data_to_send)
		with ProgressBar(
			total=encoder.len,
			unit="B",
			unit_scale=True,
			unit_divisor=1024,
			miniters=1,
			file=sys.stdout,
		) as bar:
			monitor = requests_toolbelt.MultipartEncoderMonitor(
				encoder, lambda monitor: bar.update_to(monitor.bytes_read)
			)

			r = session.post(
				upload_url(bot_token),
				data=monitor,
				allow_redirects=False,
				headers={"Content-Type": monitor.content_type},
			)

	resp = r.json()
	
	if resp['ok'] == True:
		print(f'{file_name} uploaded sucessfully on {resp["result"]["sender_chat"]["title"]}')
	else:
		print(resp)

def test_token(bot_token:str):
	r = requests.get(url(bot_token))
	verify_data = r.json()

	if verify_data['ok'] == True:
		print(f'Bot Token is correct and Bot username is {verify_data["result"]["username"]}.')
	elif verify_data['ok'] == False:
		print(f'Bot Token is wrong.')

def main(argv = None):
	parser = argparse.ArgumentParser(description="upload your files to your group or channel", formatter_class=argparse.RawDescriptionHelpFormatter)
	subparsers = parser.add_subparsers(dest="command")

	test_parser = subparsers.add_parser("test", help="test telegram bot token")

	upload_parser = subparsers.add_parser("up", help="upload file to your group or channel")
	upload_parser.add_argument("filename", type=str, help="one or more files to upload")
	upload_parser.add_argument('-c', '--caption', type=str, default=None, help="Send caption for your file")

	args = parser.parse_args(argv)

	if args.command == "test":
		return test_token(bot_token)
	elif args.command == "up":
		return upload_file(bot_token, chat_id, args.filename, args.caption)
	else:
		parser.print_help()

if __name__ == '__main__':
	raise SystemExit(main())