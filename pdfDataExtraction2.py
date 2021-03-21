from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io
import time

start_time = time.time()
path = "Annexure 5 Datasheet-Tata Project (1)(1).pdf"
tool = pyocr.get_available_tools()[0]
lang = tool.get_available_languages()[0] # 0 is int(eng)

req_image = []
final_text = []

image_pdf = Image(filename=path, resolution=300)
image_jpeg = image_pdf.convert('jpeg')

for img in image_jpeg.sequence:
    img_page = Image(image=img)
    req_image.append(img_page.make_blob('jpeg'))

for img in req_image:
    txt = tool.image_to_string(
        PI.open(io.BytesIO(img)),
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )
    final_text.append(txt)
print("--- %s seconds ---" % (time.time() - start_time))
for i in final_text:
    print(i)
