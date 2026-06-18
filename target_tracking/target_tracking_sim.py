import cv2
import numpy as np

width, height = 640, 480
fps = 30
output_file = 'car_tracking_sim.avi'

car_img = cv2.imread('car.png', cv2.IMREAD_UNCHANGED)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

target_w, target_h = 200, 100
target_x, target_y = 50, 50
shrink_rate = 0.99

if car_img.shape[2] == 4:
    b, g, r, a = cv2.split(car_img)
    mask = a 
    car_rgb = cv2.merge((b, g, r))
else:
    mask = None 
    car_rgb = car_img

# 4. DÖNGÜ
for i in range(300):
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    current_w = max(1, int(target_w))
    current_h = max(1, int(target_h))
   
    resized_car = cv2.resize(car_rgb, (current_w, current_h), interpolation=cv2.INTER_AREA)
    
    if mask is not None:
        resized_mask = cv2.resize(mask, (current_w, current_h), interpolation=cv2.INTER_AREA)
        
        region = frame[int(target_y):int(target_y+current_h), int(target_x):int(target_x+current_w)]
        region[resized_mask > 0] = resized_car[resized_mask > 0]
    else:
        frame[int(target_y):int(target_y+current_h), int(target_x):int(target_x+current_w)] = resized_car

    video.write(frame)
   
    target_w *= shrink_rate
    target_h *= shrink_rate
    target_x += ((width / 2) - (target_w / 2) - target_x) * 0.02
    target_y += ((height / 2) - (target_h / 2) - target_y) * 0.02

video.release()
print("Araba simülasyonu başarıyla oluşturuldu!")