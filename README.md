# Live Video Attendance System with Face Recognition, Gesture Verification, and Liveness Detection

## 🔍 Abstract
This real-time attendance system combines facial recognition, liveness detection, and gesture-based verification to ensure secure and accurate user authentication. Using DeepFace for face recognition, the system processes real-time video to identify individuals. Anti-spoofing is ensured through liveness detection (micro-movements) and an additional gesture-matching step. Attendance is logged only after both verifications succeed, ensuring robustness and eliminating proxy entries.

---

## 🧠 Features
- Real-time facial recognition using DeepFace.
- Anti-spoofing with liveness detection (detects real faces vs. images/videos).
- Random gesture-based verification using a custom-trained model and MediaPipe.
- Excel sheet auto-generation with daily logs.
- Duplicate prevention for re-login attempts.
- Fully automated using OpenCV and webcam feed.

---

## ⚙️ Tech Stack
- **Language:** Python  
- **Libraries/Frameworks:** DeepFace, OpenCV, MediaPipe, NumPy, Pandas, Tkinter  
- **Tools:** Excel Writer, Virtualenv

---

## 🧪 Methodology Summary
1. **Setup:** Webcam initiated; Excel workbook created for the current day.
2. **Face Recognition:** DeepFace finds match from saved database.
3. **Liveness Detection:** Spoof detection using DeepFace's anti-spoofing module.
4. **Gesture Verification:** User performs randomly prompted gesture; verified using MediaPipe.
5. **Logging:** Attendance stored in Excel only after dual verification.
6. **Continuous Monitoring:** Runs until 'q' is pressed.

---

## 📈 Results
- Detected faces in real-time with >95% accuracy.
- Successfully rejected spoofing attempts using images and videos.
- Achieved over 90% success in gesture-based verification with minimal false negatives.

---

## 📝 Future Improvements
- Integration with cloud-based databases (e.g., Firebase or AWS).
- Adding multi-face detection support.
- Real-time admin dashboard for live tracking.

---

- YouTube Demo Link [Click here](https://www.youtube.com/watch?v=1zEXZ8xSUvg)


