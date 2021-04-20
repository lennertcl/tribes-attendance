import sys
from pathlib import Path
import qrcode

def generate_codes(amount):
    for i in range(1, amount + 1):
        img = qrcode.make(i)
        img.save("qrcodes/qr" + str(i) + ".png")

if __name__ == "__main__":
    amount = int(sys.argv[1])
    Path("qrcodes").mkdir(exist_ok=True)
    generate_codes(amount)
