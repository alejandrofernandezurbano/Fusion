import numpy as np
import open3d as o3d
import cv2
import os
import random
import glob
import YoloDetector as yd
import Lidar2Camera as l2c
import LidarUtils as lu
import Utils as ut
import FusionUtils as fu
import YoloUtils as yu
import time					
import struct
from sort.sort import Sort


def load_data(data_dir):
        image_files = sorted(glob.glob(data_dir+"images/*.png"))
        point_files = sorted(glob.glob(data_dir+"points/*.pcd"))
        label_files = sorted(glob.glob(data_dir+"labels/*.txt"))
        calib_files = sorted(glob.glob(data_dir+"calibs/*.txt"))

        return image_files, point_files, label_files, calib_files
#index =6
sort_tracker = Sort()          
data_dir = "/home/alejandro-fernandez/ros2_ws/src/Visual-Sensor-Fusion/Code/Data/"
        
imgs, pts, labels, calibs = load_data(data_dir)
weights = data_dir + "model//yolov4//yolov4.weights"
config = data_dir + "model//yolov4//yolov4.cfg"
names = data_dir + "model//yolov4//coco.names"
out_dir = os.path.join(data_dir, "output//images")
detector = yd.Detector(0.4)
detector.load_model(weights, config, names)
        
#cv2.namedWindow("fused_result", cv2.WINDOW_KEEPRATIO)
        
# load the image
image = cv2.imread(imgs[12]) # original 11
        
# create LiDAR2Camera object
lidar2cam = l2c.LiDAR2Camera(calibs[7]) # original 4
        
# 1 - Run 2D object detection on image
detections, yolo_detections = detector.detect(image, draw_bboxes=True, display_labels=True)
        
# load lidar points and project them inside 2d detection
point_cloud = np.asarray(o3d.io.read_point_cloud(pts[12]).points) # original 11
pts_3D, pts_2D = lu.get_lidar_on_image(lidar2cam, point_cloud, (image.shape[1], image.shape[0]))
lidar_pts_img, _ = fu.lidar_camera_fusion(pts_3D, pts_2D, detections, image)
        
# Build a 2D Object
list_of_2d_objects = ut.fill_2D_obstacles(detections)

# Build a 3D Object (from labels)
list_of_3d_objects = ut.read_label(labels[6]) # original 5


# Get the LiDAR Boxes in the Image in 2D and 3D
lidar_2d, lidar_3d = lu.get_image_with_bboxes(lidar2cam, lidar_pts_img, list_of_3d_objects)

# Associate the LiDAR boxes and the Camera Boxes
lidar_boxes = [obs.bbox2d for obs in list_of_3d_objects]  # Simply get the boxes
pred_bboxes = [detection[1] for detection in detections]
camera_boxes = [np.array([box[0], box[1], box[0] + box[2], box[1]+box[3]]) for box in pred_bboxes]
#print("lidar_boxes: ", lidar_boxes)
#print("camera_boxes: ", camera_boxes)
# camera_boxes = [obs.bbox for obs in list_of_2d_objects]
matches, unmatched_lidar_boxes, unmatched_camera_boxes = fu.associate(lidar_boxes, camera_boxes)               #ERRRRORRRRR
print("matches: ",matches);print("unmatched_lidar_boxes: ",unmatched_lidar_boxes);print("unmatched_camera_boxes: ",unmatched_camera_boxes)
# Build a Fused Object
final_image, _ = fu.build_fused_object(list_of_2d_objects, list_of_3d_objects, matches, lidar_2d)

# draw yolo detections on top to fused results
final_image = yu.draw_yolo_detections(final_image, detections,classes_to_draw=("person", "car"))

for match in matches: 
  print("lidar_boxes: ", lidar_boxes[match[0]]);print("camera_boxes: ", camera_boxes[match[1]])  
  optimal_box = fu.find_optimal_box([lidar_boxes[match[0]]],  [camera_boxes[match[1]]]); print("Caja óptima: ", optimal_box)
  #cv2.rectangle(final_image, (int(optimal_box[0]), int(optimal_box[1])), (int(optimal_box[2]), int(optimal_box[3])), (0,0,255), 2)
  
 
pcd = o3d.io.read_point_cloud(pts[11])

#o3d.visualization.draw_geometries([pcd])               
cv2.imshow("lidar_3d", lidar_3d)
cv2.imshow("lidar_2d", lidar_2d)
cv2.imshow("yolo_detections", yolo_detections)
cv2.imshow("lidar_pts_img", lidar_pts_img)
cv2.imshow("final_image", final_image)
cv2.imwrite(os.path.join(out_dir,"lidar_3d1.png"), lidar_3d)
cv2.imwrite(os.path.join(out_dir,"fused_result1.png"), final_image)

cv2.waitKey(0)
