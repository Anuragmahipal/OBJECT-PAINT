import cv2
import numpy as np


cap = cv2.VideoCapture(0)


sampling = True
roi_top, roi_bottom, roi_right, roi_left = 100, 150, 200, 150
hsv_lower = None
hsv_upper = None


canvas = None
prev_x, prev_y = None, None
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0)]  
color_index = 0
draw_color = colors[color_index]


thickness=5


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_copy = frame.copy()

    if canvas is None:
        canvas = np.ones_like(frame) * 255 

    if sampling:
        cv2.rectangle(frame_copy, (roi_left, roi_top), (roi_right, roi_bottom), (0, 255, 0), 2)
        cv2.putText(frame_copy, "Place object in box & press 's' to sample", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    else:

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, hsv_lower, hsv_upper)

        mask = cv2.GaussianBlur(mask, (7, 7), 0)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)


        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.imshow("Mask", mask)

        if contours:


            max_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(max_contour) > 1000:
                M = cv2.moments(max_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    if prev_x is not None and prev_y is not None:
                        if abs(cx - prev_x) < 50 and abs(cy - prev_y) < 50:
                            cv2.line(canvas, (prev_x, prev_y), (cx, cy), draw_color, thickness)


                    prev_x, prev_y = cx, cy

                    cv2.circle(frame_copy, (cx, cy), 8, (255, 0, 0), -1)
                else:
                    prev_x, prev_y = None, None
            else:
                prev_x, prev_y = None, None
        else:
            prev_x, prev_y = None, None

    
    combined = cv2.addWeighted(frame_copy, 0.5, canvas, 0.5, 0)  #if wanted a combination of frame and canvas
    cv2.imshow("object_here",frame_copy)
    # cv2.imshow("combine",combined)

    cv2.imshow("paint",canvas)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('s') and sampling:

        print("Frame shape:", frame.shape)
        print("ROI:", roi_top, roi_bottom, roi_left, roi_right)
  
        roi = frame[roi_top:roi_bottom, roi_left:roi_right]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        h = hsv_roi[:, :, 0].flatten()
        s = hsv_roi[:, :, 1].flatten()
        v = hsv_roi[:, :, 2].flatten()

        h_median = int(np.median(h))
        s_median = int(np.median(s))
        v_median = int(np.median(v))

        
        hsv_lower = np.array([max(h_median - 10, 0), max(s_median - 40, 0), max(v_median - 40, 0)])
        hsv_upper = np.array([min(h_median + 10, 179), min(s_median + 40, 255), min(v_median + 40, 255)])

        sampling = False
        print(f"HSV range: {hsv_lower} - {hsv_upper}")


    elif key == ord('c'):
        canvas = np.ones_like(frame) * 255  # Clear canvas
        print("Canvas cleared!")

    elif key== ord('x'):
        color_index+=1
        color_index%=len(colors)              # change color
        draw_color = colors[color_index]
    
    elif key== ord('d'):
        thickness+=1                          # increase thickness
    elif key == ord('a'):
        thickness=max(2,thickness-1)          # decrease thickness


cap.release()
cv2.destroyAllWindows()
