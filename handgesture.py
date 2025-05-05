import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize Mediapipe Hands and webcam
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Open webcam
cam = cv2.VideoCapture(0)

def calculate_distance(p1, p2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def are_fingers_folded(landmarks):
    """Check if all fingers except the index finger are folded."""
    finger_tips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    finger_bases = [
        mp_hands.HandLandmark.THUMB_CMC,
        mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
        mp_hands.HandLandmark.RING_FINGER_MCP,
        mp_hands.HandLandmark.PINKY_MCP
    ]

    # If all other fingers (except the index) are folded (i.e., their tips are above their bases)
    for tip, base in zip(finger_tips, finger_bases):
        if landmarks[tip].y < landmarks[base].y:  # If a tip is above its base, finger is not folded
            return False
    return True

while cam.isOpened():
    ret, frame = cam.read()
    if not ret:
        print("Error: Unable to capture video")
        break

    # Flip the frame for a mirror effect
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    # Convert to RGB for Mediapipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw landmarks and connections on the frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get finger landmarks
            landmarks = hand_landmarks.landmark
            index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_base = landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]

            # Map index finger tip to screen coordinates for cursor movement
            screen_x = int(index_tip.x * screen_width)
            screen_y = int(index_tip.y * screen_height)
            pyautogui.moveTo(screen_x, screen_y)

            # Check if all fingers except the index finger are folded (fist detected)
            if are_fingers_folded(landmarks):
                # No scrolling occurs if fingers are folded (fist)
                cv2.putText(frame, "Fist Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            else:
                # Scroll detection when hand is open
                index_y = int(index_tip.y * frame_height)
                middle_y = int(middle_tip.y * frame_height)
                delta_y = middle_y - index_y

                # Scroll thresholds
                SCROLL_UP_THRESHOLD = -30  # Adjust as needed
                SCROLL_DOWN_THRESHOLD = 30  # Adjust as needed
                SCROLL_SENSITIVITY = 20  # Controls scroll speed

                # Scroll up when middle finger is above the index finger
                if delta_y < SCROLL_UP_THRESHOLD:  # Scroll up
                    pyautogui.scroll(SCROLL_SENSITIVITY)
                    cv2.putText(frame, "Scrolling Up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Scroll down when middle finger is below the index finger
                elif delta_y > SCROLL_DOWN_THRESHOLD:  # Scroll down
                    pyautogui.scroll(-SCROLL_SENSITIVITY)
                    cv2.putText(frame, "Scrolling Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Calculate distance between thumb and index finger for click gesture
            thumb_coords = (int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height))
            index_coords = (int(index_tip.x * frame_width), int(index_tip.y * frame_height))
            distance = calculate_distance(thumb_coords, index_coords)

            # Define click threshold (when fingers are close together)
            CLICK_THRESHOLD = 30

            # If the distance between thumb and index finger is less than the threshold, click
            if distance < CLICK_THRESHOLD:
                pyautogui.click()
                cv2.circle(frame, index_coords, 15, (0, 255, 0), -1)  # Visualize click with a green circle

            # Draw circle on index finger tip
            cv2.circle(frame, (int(index_tip.x * frame_width), int(index_tip.y * frame_height)), 10, (255, 0, 0), -1)

    # Show the video feed
    cv2.imshow("Finger Mouse with Scroll and Click", frame)

    # Exit on pressing 'ESC' key
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

# Release resources
cam.release()
cv2.destroyAllWindows()
