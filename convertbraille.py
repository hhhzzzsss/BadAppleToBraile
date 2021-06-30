import cv2
import numpy as np

outfile = open('badapple.txt', 'w', encoding="utf-8")

def convert_braille(image):
    image = cv2.resize(image, (160, 120))
    image = image[:,:,0];
    image = np.reshape(image, (20, 6, 80, 2));
    image = np.swapaxes(image, 1, 2);
    for line in image:
        for cbox in line:
            code = 0x2800
            threshold = 50;
            if cbox[2][0] > threshold: code += 1
            if cbox[3][0] > threshold: code += 2
            if cbox[4][0] > threshold: code += 4
            if cbox[2][1] > threshold: code += 8
            if cbox[3][1] > threshold: code += 16
            if cbox[4][1] > threshold: code += 32
            if cbox[5][0] > threshold: code += 64
            if cbox[5][1] > threshold: code += 128
            outfile.write(chr(code))
        outfile.write('\n')
    outfile.write('--\n')
            

vidcap = cv2.VideoCapture('badapple.mp4')
start_frame = 45
end_frame = 6516
frame = 0
success, image = vidcap.read()
while success:
    if (frame%3 == 0 and frame>=start_frame and frame <= end_frame):
        convert_braille(image)
        print("converted frame %d" % (frame/3))
    success, image = vidcap.read()
    frame += 1;

outfile.close()
