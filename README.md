AI-Powered Cricket Cover Drive Analysis 🏏
This project uses computer vision to analyze the biomechanics of a cricket cover drive from a video. It leverages OpenCV and MediaPipe to perform real-time pose estimation, calculate key performance metrics, and provide a final evaluation score.

Features
Pose Estimation: Detects 33 key body landmarks in each frame of the video.

Biomechanical Metrics: Calculates crucial metrics for a cover drive, including:

Front Elbow Angle

Spine Lean

Head-over-Knee Alignment

Front Foot Direction

Real-time Visual Feedback: Overlays the pose skeleton, angles, and performance feedback directly onto the video.

Performance Scoring: Generates a final evaluation report (evaluation.json) with scores (1-10) and comments for each metric.

Annotated Video Output: Saves the processed video with all visual overlays for review.

Demo
Here's a quick look at the system in action, analyzing a cover drive and generating real-time feedback.

(Placeholder for a GIF or short video of the project running)

Installation
To get this project up and running on your local machine, follow these steps.

Clone the repository:

Bash

git clone https://github.com/TanishqMisal/Cover-Drive-Analysis.git
cd Cover-Drive-Analysis
Create a virtual environment (recommended):

Bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the required dependencies:
The project's dependencies are listed in requirements.txt. Install them with pip:

Bash

pip install -r requirements.txt
Usage
Place your input video file (e.g., input_video.mp4) in the root directory of the project.

Open the main.py file and update the video_path variable to point to your video file:

Python

video_path = 'your_video_name.mp4'
Run the script from your terminal:

Bash

python main.py
The script will process the video, display the real-time analysis in a window, and save the output files in the /output directory.

Output Files
After the script finishes, you will find two files in the /output directory:

annotated_video.mp4: The original video with the pose skeleton, metrics, and feedback drawn on each frame.

evaluation.json: A JSON file containing the final scores and comments for each biomechanical metric.

Example evaluation.json:
JSON

{
  "elbow_angle": {
    "score": 8,
    "average_value": 165.4,
    "comment": "Good arm extension."
  },
  "spine_lean": {
    "score": 7,
    "average_value": 12.1,
    "comment": "Solid balance and posture."
  },
  "summary": "A strong performance. Focus on keeping the head still for better balance."
}
Technologies Used
Python

OpenCV: For video I/O and drawing overlays.

MediaPipe: For robust, real-time pose estimation.

NumPy: For mathematical calculations (angles, distances).
