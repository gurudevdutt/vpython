from vpython import *
from PIL import ImageGrab
import os
import glob

scene.caption = """To rotate "camera", drag with right button or Ctrl-drag.
To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
  On a two-button mouse, middle is left + right.
To pan left/right and up/down, Shift-drag.
Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
# size of box and thickness of box walls
side = 4.0
thk = 0.3
s2 = 2*side - thk
s3 = 2*side + thk

wallR = box (pos=vector( side, 0, 0), size=vector(thk, s2, s3),  color = color.red)
wallL = box (pos=vector(-side, 0, 0), size=vector(thk, s2, s3),  color = color.red)
wallB = box (pos=vector(0, -side, 0), size=vector(s3, thk, s3),  color = color.blue)
wallT = box (pos=vector(0,  side, 0), size=vector(s3, thk, s3),  color = color.blue)
wallBK = box(pos=vector(0, 0, -side), size=vector(s2, s2, thk), color = color.gray(0.7))
wallFrtpos = vector(0,0,side)
#wallFrt = box(pos=vector(0,0,6),size=vector(12,12,0.2))
ball = sphere(pos = vector(-1,0,0),color = color.green, radius = 0.4, make_trail=True, retain=200)
ball.mass = 1.0
ball.p = vector(-1, -2, +3)

side = side - thk*0.5 - ball.radius

dt = 0.01
#deltat = 0.05
t = 0
vscale=0.1
varr = arrow(pos=ball.pos, axis=vscale * (ball.p/ball.mass), color=color.yellow)
scene.autoscale=False

fnum=10
sceneleft = 50
scenetop = 230
os.chdir('./frames/')
files = glob.glob('*')
print('Removing all image files...')
for f in files:
    os.remove(f)
# trying to get the bounding box from the window rather than hard coding  but doesn't quite work yet.
def coords(scene):  # return canvas bounding box, excluding frames
    bar, d = 30, 8  # title bar and frame thickness for Windows
    #print ("Scene coords:",(int(scene.center.x -scene.range + d), int(scene.center.y - scene.range + bar),
    #        int(scene.center.x + 2*scene.width - d), int(scene.center.y + 2*scene.height - d)))
    left = scene.center.x - scene.range + d
    top = scene.center.y - scene.range + bar
    right = left + scene.width - d
    bottom = top + scene.height - d
    return (int(left), int(top), int(right), int(bottom))

print("Scene coords", coords(scene))
# while True:
#     rate(200)
#     ball.pos = ball.pos + (ball.p/ball.mass)*dt
#     if not (side > ball.pos.x > -side):
#         ball.p.x = -ball.p.x
#     if not (side > ball.pos.y > -side):
#         ball.p.y = -ball.p.y
#     if not (side > ball.pos.z > -side):
#         ball.p.z = -ball.p.z
while t < 3:
    rate(200)
    ball.pos = ball.pos + (ball.p/ball.mass) * dt
    if ball.pos.x  > (wallR.pos.x - ball.radius) or ball.pos.x < (wallL.pos.x + ball.radius):
        ball.p.x = -ball.p.x
    if ball.pos.y > (wallT.pos.y - ball.radius) or ball.pos.y < (wallB.pos.y + ball.radius):
        ball.p.y = - ball.p.y
    if ball.pos.z > (wallFrtpos.z - ball.radius) or ball.pos.z < (wallBK.pos.z + ball.radius):
        ball.p.z = - ball.p.z
    varr.pos = ball.pos
    varr.axis = vscale*(ball.p/ball.mass)
    t = t + dt
    # Grab every 10 frames
    saveimg = False
    if fnum >= 200:
        break
    elif not saveimg:
        break
    elif (fnum % 20 == 0):
        im = ImageGrab.grab((sceneleft, scenetop, sceneleft + 1200, scenetop + 780))  # screen box from (0,0)-(500,500)
        #im = ImageGrab.grab(coords(scene))
        num = '00' + repr(fnum)
        imgstr = 'img-{0:d}.png'.format(fnum)
        print(imgstr+'\n')
        im.save(imgstr)  # save image to disk, xxx=img number, e.g. 000-200
    fnum += 1
# if the program cannot find "ffmpeg", check its path. can also replace it with "movie.bat"
#call("ffmpeg -r 20 -i img-%3d.png -vcodec libx264 -vf format=yuv420p,scale=412:412 -y movie.mp4")
#print("\n Movie made: movie.mp4")