# Virtual-Mouse

# Virtual Mouse - Cursor Movement Using Eye, Hand, and Voice

This project presents a **Virtual Mouse system** that integrates **eye tracking**, **hand gesture recognition**,
and **voice commands** to enable multimodal, hands-free human-computer interaction. Designed to enhance accessibility,
the system allows users to control a
computer without traditional input devices like a physical mouse or keyboard.

## 🔍 Abstract

The Virtual Mouse leverages computer vision and voice recognition to provide an intuitive interface especially beneficial
for users with physical limitations. By using eye movement for cursor positioning, hand gestures for interactions,
and voice for executing commands, the system offers a flexible and accessible alternative to conventional input methods.

## 🎯 Objectives

- Provide an assistive solution for individuals with physical disabilities.
- Empower users with motor impairments to operate computers independently.
- Offer multiple input options—eye, hand, and voice—to suit different user needs.
- Ensure ease of use with minimal setup and calibration.

## 🛠️ Implementation Overview

### 👁️ Eye Tracking
- Implemented using **Visible Light Limbus Tracking**.
- Real-time cursor control with ~90% accuracy.
- Supports click actions via **dwell time** or **blinks**.
- Latency: Under 50ms.

### ✋ Hand Gesture Recognition
- Detects gestures like swipes, taps, and pinches.
- Over 90% recognition accuracy.
- Clicking and hovering enabled via custom gestures.
- Calibrated for various hand sizes.

### 🗣️ Voice Control
- Built using Python libraries:
  - `speech_recognition`
  - `pyttsx3`
  - `pyautogui`
- Recognizes commands like “open Google” or “send email.”
- Latency: Under 300ms.
- Includes noise filtering using `pyaudio`.

### 🔄 Integration
- All three modules are combined into a **single multimodal system**.
- Designed for **real-time responsiveness**, **robustness**, and **ease of use**.

## 💡 Applications

- Accessibility**: Assist users with mobility impairments.
- Healthcare**: Enable touch-free controls in sterile zones.
- VR/AR: Enhance interaction in immersive environments.
- Smart Homes: Control IoT devices via voice/gestures.
- Public Interfaces: Reduce touch for better hygiene.
- Gaming: Hands-free gameplay experience.
- Education: Assist differently-abled students.
- Industrial Use: Enable remote/hands-free machine operation.

## 📌 Future Work

- Enhance responsiveness and adaptability.
- Expand into AR/VR and robotic control applications.
- Improve calibration and user feedback mechanisms.


## 📁 Requirements

- Python 3.x
- OpenCV
- NumPy
- pyautogui
- speech_recognition
- pyttsx3
- pyaudio

