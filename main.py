import discord, time, json
from discord.colour import Color

config = json.load(open("config.json"))

from mirage import image

"""
add blur to the image if possible or fix font sizes
"""

PLACES = [
	["Valka", "http://www.valka.lv/webcam/img.php"],
	["Kolka", "http://84.15.209.153:8080/?action=snapshot"],
	["Ventspils", "http://85.158.74.22/mjpg/video.mjpg"],
	["Sigulda", "https://camstream.alteco.lv:8443/live/camera12_720p2628kbs/index.m3u8"],
	["Liepaja", "http://arhivs.liepaja.lv/webcam2/current.jpg"],
	["Madona", "http://www.madona.lv/lat/webcam/gj.php?id=1?v=" + str(time.time())],
	["Kuldiga", "http://edge-telia1.tiesraides.lv/live/kuldiga.lv.12_1/chunklist.m3u8"],
	["Saulkrasti", "http://s29.ipcamlive.com/streams/1dpjeuoznbp0goljd/stream.m3u8"],
	["Aluksne", [
		"https://skats.aluksne.lv:8125/muzejs.webm",
		"https://skats.aluksne.lv:8125/cam.webm",
	]], 
	["Cesis", [
		"https://camstream.alteco.lv:8443/live/camera3_720p2628kbs/index.m3u8",
		"https://camstream.alteco.lv:8443/live/camera1_720p2628kbs/index.m3u8"
	]],
	["Kakis", [
		"http://www.kakiskalns.lv/images/cam.php?id=1&v=" + str(time.time()),
		"http://www.kakiskalns.lv/images/cam.php?id=2&v=" + str(time.time()),
		"http://www.kakiskalns.lv/images/cam.php?id=3&v=" + str(time.time()),
	]],
	["Riga", [
		"https://rop.lv/hls/cam1.m3u8",
		"https://rop.lv/hls/cam2.m3u8",
		"https://rop.lv/hls/cam3.m3u8"
	]],
]


client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	
@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith(config["prefix"]["commands"]):
		args = message.content.split(" ")
		command = args.pop(0)[len(config["prefix"]["commands"]):]

		if command == "viewcams":
			embed = discord.Embed(colour=Color.blurple())

			for place in PLACES:
				if type(place[1]) is list:
					embed.add_field(name=place[0], value=f"Use `{config['prefix']['cam']} {place[0].lower()} 0-{len(place[1])-1}` to view this camera!")
				else:
					embed.add_field(name=place[0], value=f"Use `{config['prefix']['cam']} {place[0].lower()}` to view this camera!")

			await message.channel.send(embed=embed)

	if message.content.startswith(config["prefix"]["cam"] + " "):
		args = message.content.split(" ") 
		args.pop(0)
		cam = args.pop(0)
		found = False

		for place in PLACES:
			if cam.lower().startswith(place[0].lower()):
				found = True

				if type(place[1]) is list:
					if len(args) >= 1:
						num = int(args[0])

						if num <= len(place[1])-1:
							await image(place[1][num], place[0], message)
						else:
							await message.channel.send("Provide a number from 0 to " + str(len(place[1])-1))
					else:
						await message.channel.send("Provide a number from 0 to " + str(len(place[1])-1))
				else:
					await image(place[1], place[0], message)


		if not found:
			await message.channel.send("Did not find place called " + cam + "!")

client.run(config["token"])