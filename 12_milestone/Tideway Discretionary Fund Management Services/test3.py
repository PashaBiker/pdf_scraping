







from PIL import Image
im = Image.open("12_milestone\Tideway Discretionary Fund Management Services\circle.png")
im = im.convert("RGB")
Dated_Fixed_Income  = 0
Equity_Income = 0
Alternatives = 0
Fixed_Income = 0
Equity_Growth = 0


for pixel in im.getdata():
    if pixel == (193,230,231):
        Dated_Fixed_Income += 1
    if pixel == (0,174,239):
        Equity_Income += 1
    if pixel == (247,148,30):
        Alternatives += 1
    if pixel == (88,194,173):
        Fixed_Income += 1
    if pixel == (156,203,59):
        Equity_Growth += 1

print("Dated_Fixed_Income = ", Dated_Fixed_Income , "Equity_Income = " , Equity_Income , 
      "Alternatives = " , Alternatives , "Fixed_Income = " , Fixed_Income,"Equity_Growth =" , Equity_Growth)

