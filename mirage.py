import discord, requests, io, cv2, m3u8, pafy
from discord import message
from discord.colour import Color

from PIL import Image, ImageFont, ImageDraw, ImageFilter
from datetime import datetime

def getM3u8(url: str):
    playlist = m3u8.load(url)
    ts = playlist.segments[len(playlist.segments)-1]

    buf = getFrame("/".join(url.split("/")[:-1]) + "/" + ts.uri)
    
    return buf

def getYoutube(url: str):
	video = pafy.new(url)
	best = video.getbest(preftype="mp4")
	
	cap = cv2.VideoCapture(best.url)
	
	success, image = cap.read()

	if success:
		is_success, im_buf_arr = cv2.imencode(".jpg", image)

		if is_success:
			io_buf = io.BytesIO(im_buf_arr)
			return io_buf

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
	elif "youtube.com" in url:
		buf = getYoutube(url)

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
	w_1, h_1 = font_title.getsize(location)
	w_2, h_2 = font_time.getsize(datetime.now().strftime('%H:%M'))
	
	mask = Image.new('L', image.size, 0)
	mask_draw = ImageDraw.Draw(mask)
	mask_draw.rectangle([(10, image.size[1]-10), (w_1+w_2+18, image.size[1] - 55)], fill=255)
	
	image.paste(image.filter(ImageFilter.GaussianBlur(27)), mask=mask)

	draw.text((11, image.size[1] - 60), location, 0, font_title)
	draw.text((w_1 + 15, image.size[1] - 38), datetime.now().strftime('%H:%M'), 0, font_time)

	b = io.BytesIO()
	image.save(b, "JPEG")
	b.seek(0)

	original = await message.channel.send(embed=discord.Embed(title="Loading...", description="Rendering Image.", color=Color.orange()))

	file = discord.File(b, filename="image.png")

	embed = discord.Embed(title="Yay!", description="Rendered!", color=Color.green())
	embed.set_image(url="attachment://image.png")
	
	await message.channel.send(file=file, embed=embed)
	await original.delete()