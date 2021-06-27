import discord, requests, io, cv2, m3u8
from discord import message
from discord.colour import Color

from PIL import Image, ImageFont, ImageDraw
from datetime import datetime

def getM3u8(url: str):
    playlist = m3u8.load(url)
    ts = playlist.segments[len(playlist.segments)-1]

    buf = getFrame("/".join(url.split("/")[:-1]) + "/" + ts.uri)
    
    return buf

def getFrame(url: str):
    cap = cv2.VideoCapture(url)
    success, image = cap.read()

    if success:
        is_success, im_buf_arr = cv2.imencode(".jpg", image)

        if is_success:
            io_buf = io.BytesIO(im_buf_arr)
            return io_buf

async def image(url: str, location: str, message: message):
	if ".mjpg" in url or ".webm" in url:
		buf = getFrame(url)

		if not buf:
			await message.channel.send(embed=discord.Embed(title="Error!", description=f"Experienced networking error!", color=Color.red()))
			return

		image = Image.open(buf)
	elif ".m3u8" in url:
		buf = getM3u8(url)
		
		if not buf:
			await message.channel.send(embed=discord.Embed(title="Error!", description=f"Experienced networking error!", color=Color.red()))
			return
			
		image = Image.open(buf)
	else:
		r = requests.get(url, stream=True, headers={
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_5 rv:2.0; en-US) AppleWebKit/534.1.1 (KHTML, like Gecko) Version/5.0.1 Safari/534.1.1"
		})

		r.raw.decode_content = True
		
		if r.status_code > 400:
			await message.channel.send(embed=discord.Embed(title="Error!", description=f"Experienced {r.status_code} error!", color=Color.red()))
			return

		image = Image.open(r.raw)

	draw = ImageDraw.Draw(image)
	
	font_title = ImageFont.truetype("Alice-Regular.ttf", 48)
	font_time = ImageFont.truetype("Alice-Regular.ttf", 24)

	draw.text((11, image.size[1] - 60), location, 0, font_title)
	draw.text((font_title.getsize(location)[0] + 15, image.size[1] - 38), datetime.now().strftime('%H:%M'), 0, font_time)

	b = io.BytesIO()
	image.save(b, "JPEG")
	b.seek(0)

	original = await message.channel.send(embed=discord.Embed(title="Loading...", description="Rendering Image.", color=Color.orange()))

	await message.channel.send(file=discord.File(b, 'img.jpg'))

	await original.edit(embed=discord.Embed(title="Yay!", description="Rendered!", color=Color.green()))