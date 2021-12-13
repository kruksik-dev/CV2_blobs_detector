import subprocess
import sys
import glob 
import os
import csv


#static flag 
first_time_flag = True

#install package if not found 
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    

#remove gray background from image 
def remove_background_gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _ , threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

    _cnts = cv2.findContours(threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts = sorted(_cnts, key=cv2.contourArea)
    for cnt in cnts:
        if cv2.contourArea(cnt) > 100:
            break

    mask = np.zeros(img.shape[:2],np.uint8)
    cv2.drawContours(mask, [cnt],-1, 255, -1)
    dst = cv2.bitwise_and(img, img, mask=mask)
    return dst

def find_blobs(image):
    filename = os.path.basename(image).split('.')[0]
    img = cv2.imread(image)
    img = remove_background_gray(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)




    blurred = cv2.medianBlur(gray, 7)
    _filter = cv2.bilateralFilter(blurred, 5, 50, 50)
    adap_thresh = cv2.adaptiveThreshold(_filter,
                                        225,
                                        cv2.CALIB_CB_ADAPTIVE_THRESH,
                                        cv2.THRESH_BINARY,
                                        21, 0)


    element = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)) 
    dilated = cv2.dilate(adap_thresh, element, iterations=1)

    # blob detection parameters, can be change 
    params = cv2.SimpleBlobDetector_Params()
    params.filterByColor = False
    params.minThreshold = 15
    params.maxThreshold = 1000
    params.blobColor = 25
    params.minArea = 15
    params.maxArea = 5000000
    params.filterByCircularity = False
    params.filterByConvexity = False
    params.minCircularity = 0.1
    params.maxCircularity = 1

    det = cv2.SimpleBlobDetector_create(params)
    keypts = det.detect(dilated)

    res = cv2.drawKeypoints(img,
                            keypts,
                            np.array([]),
                            (0, 0, 255 ),
                            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    for kp in keypts:
        cv2.rectangle(res,(int(kp.pt[0]),int(kp.pt[1])),(int(kp.pt[0])+1,int(kp.pt[1])+1),(0,255,0),2)

    #text about how many blobs found 
    image_text = f'Found blobs: {len(keypts)}' # can be change {len(keypts)} is blobs number
    res = cv2.putText(res, image_text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0,0,255), 2, cv2.LINE_AA)

    if not os.path.exists('results'):
        os.makedirs('results')
    cv2.imwrite(f'results/{filename}_detected.jpg', res)
    print(f'Picture {filename} has been detected ')
    return len(keypts), filename

def write_results_to_csv(filename,keypts):
    with open("blobs_detection_output.csv",'a',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        global first_time_flag
        if first_time_flag:
            writer.writerow(('Picture','Amount of blobs'))
            first_time_flag = False
        writer.writerow((filename,keypts))




if __name__ == '__main__':
    try:
        import cv2
        import numpy as np 
    except:
        install('opencv-python')
        import cv2
        import numpy as np



    for img in glob.glob('target_pictures/*.jpg'):
        blobs, file = find_blobs(img)
        write_results_to_csv(file,blobs)