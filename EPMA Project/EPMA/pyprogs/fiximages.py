import cv2
import numpy as np

def remove_white_boundaries(image_path,uid):
    ## (1) Convert to gray, and threshold
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    ## (2) Morph-op to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

    ## (3) Find the max-area contour
    cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnt = sorted(cnts, key=cv2.contourArea)[-1]

    ## (4) Crop and save it
    x,y,w,h = cv2.boundingRect(cnt)
    dst = img[y:y+h, x:x+w]
    cv2.imwrite("./PNG/"+uid+".png", dst)
        
    #cv2.imshow('Result', result)
    # cv2.imwrite('result.png', result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # return result

# # Replace 'your_image_path.png' with the path to your image
# result_image = remove_white_boundaries('your_image_path.png')

# # Display the result
# cv2.imshow('Result', result_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
