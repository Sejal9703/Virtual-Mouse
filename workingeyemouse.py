import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize webcam and face mesh
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

# Constants
BLINK_THRESHOLD = 0.004
SMOOTHING = 15
SCROLL_MULTIPLIER = 600  # For nose tip scrolling
DEADZONE_SCROLL = 3

# State variables
prev_x, prev_y = 0, 0
left_blink_flag = False
right_blink_flag = False
initial_nose_y = None

# Metrics for system robustness
metrics = {
    'good': {'clicks': 0, 'correct': 0, 'false_clicks': 0, 'latencies': []},
    'bad': {'clicks': 0, 'correct': 0, 'false_clicks': 0, 'latencies': []}
}
lighting_condition = 'good'

while True:
    ret, frame = cam.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    cv2.putText(frame, f"Lighting: {lighting_condition.upper()} (Press G/B)", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    if landmark_points:
        landmarks = landmark_points[0].landmark

        # Cursor movement using landmark 475 (index 1 of 474-478)
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            if id == 1:
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y
                curr_x = prev_x + (screen_x - prev_x) / SMOOTHING
                curr_y = prev_y + (screen_y - prev_y) / SMOOTHING
                pyautogui.moveTo(curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y

        # Eye landmarks for blink detection
        left_eye = [landmarks[145], landmarks[159]]
        right_eye = [landmarks[374], landmarks[386]]

        left_diff = abs(left_eye[0].y - left_eye[1].y)
        right_diff = abs(right_eye[0].y - right_eye[1].y)

        # Left eye blink = left click
        if left_diff < BLINK_THRESHOLD:
            if not left_blink_flag:
                t1 = time.time()
                pyautogui.click(button='left')
                t2 = time.time()
                latency = t2 - t1
                metrics[lighting_condition]['clicks'] += 1
                metrics[lighting_condition]['correct'] += 1
                metrics[lighting_condition]['latencies'].append(latency)
                left_blink_flag = True
        else:
            left_blink_flag = False

        # Right eye blink = right click
        if right_diff < BLINK_THRESHOLD:
            if not right_blink_flag:
                t1 = time.time()
                pyautogui.click(button='right')
                t2 = time.time()
                latency = t2 - t1
                metrics[lighting_condition]['clicks'] += 1
                metrics[lighting_condition]['correct'] += 1
                metrics[lighting_condition]['latencies'].append(latency)
                right_blink_flag = True
        else:
            right_blink_flag = False

        # Nose tip scrolling (landmark 1)
        nose_y = landmarks[1].y
        if initial_nose_y is None:
            initial_nose_y = nose_y
        scroll_delta = int((initial_nose_y - nose_y) * SCROLL_MULTIPLIER)
        if abs(scroll_delta) > DEADZONE_SCROLL:
            pyautogui.scroll(scroll_delta)

        # Draw eye dots
        for eye_landmarks, color in zip([left_eye, right_eye], [(0, 255, 255), (255, 0, 255)]):
            for landmark in eye_landmarks:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, color, -1)

    # Key press to toggle lighting condition
    key = cv2.waitKey(10) & 0xFF
    if key == ord('g'):
        lighting_condition = 'good'
    elif key == ord('b'):
        lighting_condition = 'bad'
    elif key == 27:
        break

    cv2.imshow("Eye-Controlled Mouse", frame)

cam.release()
cv2.destroyAllWindows()

# === Print Final Performance Metrics ===
def print_metrics(label):
    data = metrics[label]
    print(f"\n[{label.upper()} LIGHT]")
    if data['clicks'] == 0:
        print("No clicks detected.")
        return
    accuracy = (data['correct'] / data['clicks']) * 100
    avg_latency = np.mean(data['latencies']) * 1000 if data['latencies'] else 0
    print(f"Total Clicks: {data['clicks']}")
    print(f"Correct Clicks: {data['correct']}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Average Click Latency: {avg_latency:.2f} ms")
    print(f"False Clicks (if applicable): {data['false_clicks']}")

print("\n=== SYSTEM PERFORMANCE REPORT ===")
print_metrics('good')
print_metrics('bad')
print("=================================")
