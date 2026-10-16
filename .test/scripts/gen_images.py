from pathlib import Path
from PIL import Image
import random


QUANTITY = 20


out = Path("images")
out.mkdir(exist_ok=True)

for i in range(QUANTITY):
    w, h = random.randint(1200, 1800), random.randint(1200, 1800)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    img = Image.new("RGB", (w, h), color)
    img.save(out / f"img_{i:02d}.jpg", quality=85)

print(f"Generated {QUANTITY} images")