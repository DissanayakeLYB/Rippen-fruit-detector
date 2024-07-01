import cv2
import numpy as np

def count_fingers(roi, drawing):
    # Convert to grayscale
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (35, 35), 0)
    
    # Threshold to get binary image
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        return 0
    
    # Get the largest contour
    contour = max(contours, key=lambda x: cv2.contourArea(x))
    
    # Create bounding rectangle around the contour
    x, y, w, h = cv2.boundingRect(contour)
    
    # Create a convex hull around the largest contour
    hull = cv2.convexHull(contour)
    
    # Draw contours
    cv2.drawContours(drawing, [contour], -1, (0, 255, 0), 2)
    cv2.drawContours(drawing, [hull], -1, (0, 0, 255), 2)
    
    # Find convexity defects
    hull = cv2.convexHull(contour, returnPoints=False)
    defects = cv2.convexityDefects(contour, hull)
    
    if defects is None:
        return 0
    
    # Count defects
    finger_count = 0
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])
        far = tuple(contour[f][0])
        
        # Calculate the length of sides of the triangle
        a = np.linalg.norm(np.array(start) - np.array(end))
        b = np.linalg.norm(np.array(start) - np.array(far))
        c = np.linalg.norm(np.array(end) - np.array(far))
        
        # Apply cosine rule here
        angle = np.arccos((b**2 + c**2 - a**2) / (2*b*c))
        
        # If angle is less than 90 degrees, count it as a finger
        if angle <= np.pi / 2:
            finger_count += 1
            cv2.circle(drawing, far, 4, (0, 0, 255), -1)
    
    return finger_count

# Initialize video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame to avoid mirrored image
    frame = cv2.flip(frame, 1)
    
    # Define region of interest (ROI)
    roi = frame[100:400, 100:400]
    cv2.rectangle(frame, (100, 100), (400, 400), (0, 255, 0), 2)
    
    # Process the ROI and count fingers
    drawing = np.zeros(roi.shape, np.uint8)
    finger_count = count_fingers(roi, drawing)
    
    # Display the number of fingers
    cv2.putText(frame, f'Fingers: {finger_count}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Show the frames
    cv2.imshow('Frame', frame)
    cv2.imshow('ROI', drawing)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
