import qrcode

for i in range(1, 56):
    img = qrcode.make(i)
    img.save("qrcodes/qr" + str(i) + ".png")