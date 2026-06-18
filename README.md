Autonomous Target Tracking and Lock Continuity System
This project is a simulation of autonomous target detection and tracking mechanisms commonly used in security and defense systems. The system utilizes the YOLO deep learning model for real-time object detection while integrating a Kalman Filter to smooth out sensor noise and maintain continuous target tracking during temporary lock losses.

🚀 Key Features
Deep Learning-Based Detection: High-accuracy vehicle/target detection powered by YOLO.

Predictive Tracking (Kalman Filter): Employs a physical motion model (Constant Velocity) to continue tracking even when the target temporarily leaves the frame or experiences visual noise.

Validation Check (Lock Loss Mechanism): Monitors bounding box dimensions and triggers a visual alert when the target drops below the minimum trackable threshold.

Telemetry and Video Export: Automatically saves the processed video stream with real-time tracking annotations into an .mp4 file.
