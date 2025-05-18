import cv2
import numpy as np

def decode_base64_to_image(base64_string: str) -> np.ndarray:
    """
    Convert base64 image string to OpenCV format
    """
    import base64
    img_data = base64.b64decode(base64_string)
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def detect_faces(image: np.ndarray) -> list:
    """
    Detect faces using OpenCV's DNN face detector
    Returns list of face ROI coordinates (x,y,w,h)
    """
    net = cv2.dnn.readNetFromCaffe(
        "deploy.prototxt",  # Download from OpenCV repo
        "res10_300x300_ssd_iter_140000.caffemodel"  # Download model
    )
    
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, 
                               (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    
    faces = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:  # Confidence threshold
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")
            faces.append((x1, y1, x2-x1, y2-y1))
    
    return faces

def align_face(image: np.ndarray, face_box: tuple) -> np.ndarray:
    """
    Crop and align face using facial landmarks
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (x, y, w, h) = face_box
    
    # Simple center crop (replace with landmark-based alignment for better accuracy)
    face_roi = image[y:y+h, x:x+w]
    return cv2.resize(face_roi, (160, 160))  # Standard size for FaceNet
