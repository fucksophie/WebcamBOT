import discord, time, json
from discord.colour import Color

config = json.load(open("config.json"))

from mirage import image

COUNTRIES = [
	["Latvia", [
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
	]],
	["Russia", [
		["Moscow", [
			"https://cameras.inetcom.ru/hls/camera12_1.m3u8",
			"https://cameras.inetcom.ru/hls/camera12_2.m3u8",
			"https://cameras.inetcom.ru/hls/camera12_3.m3u8",
			"https://cameras.inetcom.ru/hls/camera12_4.m3u8",
			"https://cameras.inetcom.ru/hls/camera12_5.m3u8",
			"https://cameras.inetcom.ru/hls/camera12_6.m3u8",
			"https://cameras.inetcom.ru/hls/camera12_7.m3u8",
			"https://cameras.inetcom.ru/hls/camera12_8.m3u8"
		]],
		["Petersburg", [
			"https://www.youtube.com/watch?v=9ELF5lw-NX0",
			"https://www.youtube.com/watch?v=JFT2sYtdcuc"
		]]
	]],
]

activity = discord.Activity(type=discord.ActivityType.watching, name=f"webcams :) | {config['prefix']['commands']}viewcams")
client = discord.Client(activity=activity)

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

			if len(args) == 0:
				embed = discord.Embed(colour=Color.blurple())
				
				for country in COUNTRIES:
					embed.add_field(name=country[0], value=f"Use {config['prefix']['commands']}viewcams {country[0]} to view cameras of this country.")
			
				await message.channel.send(embed=embed)
			else:
				country_arg = args[0]
				found = False
				
				for country in COUNTRIES:
					if country_arg.lower().startswith(country[0].lower()):
						found = True
						
						embed = discord.Embed(colour=Color.blurple())
						
						for place in country[1]:
							if type(place[1]) is list:
								embed.add_field(name=place[0], value=f"Use `{config['prefix']['cam']} {country[0].lower()} {place[0].lower()} 0-{len(place[1])-1}` to view this camera!")
							else:
								embed.add_field(name=place[0], value=f"Use `{config['prefix']['cam']} {country[0].lower()} {place[0].lower()}` to view this camera!")
						
						await message.channel.send(embed=embed)
					
				if not found:
					await message.channel.send("Did not find country called " + country_arg + "!")

	if message.content.startswith(config["prefix"]["cam"] + " "):
		args = message.content.split(" ") 
		args.pop(0)
		
		if len(args) == 1:
			await message.channel.send("Add a cam, such as `mz latvia riga 0`!")
			return
			
		count = args.pop(0)
		cam = args.pop(0)

		found_place = False
		found_country = False

		for country in COUNTRIES:
			if count.lower().startswith(country[0].lower()):
				found_country = True
				for place in country[1]:
					if cam.lower().startswith(place[0].lower()):
						found_place = True

						if type(place[1]) is list:
							if len(args) >= 1:
								num = int(args[0])

								if num <= len(place[1])-1:
									await image(place[1][num], country[0] + ", " + place[0], message)
								else:
									await message.channel.send("Provide a number from 0 to " + str(len(place[1])-1))
							else:
								await message.channel.send("Provide a number from 0 to " + str(len(place[1])-1))
						else:
							await image(place[1], country[0] + " " + place[0], message)

	
		if not found_country:
			await message.channel.send("Did not find country called " + count + "!")
			return

		if not found_place:
			await message.channel.send("Did not find place called " + cam + "!")
			return			

client.run(config["token"])