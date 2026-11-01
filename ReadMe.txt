 Smart City Traffic Monitoring Dashboard

About the Project

This is a Python-based traffic monitoring dashboard that I worked on during my internship at Patna Smart City Limited.

The main idea behind this project was to explore how AI and computer vision can be used to monitor traffic, detect vehicles, identify possible accidents and display useful information on a single dashboard.

I wanted to understand how these technologies can be used in real-life traffic monitoring systems.

Project Features :-

The project includes different features related to traffic monitoring:

Vehicle Detection: Used YOLOv8 to detect vehicles from traffic footage.

Traffic Congestion Monitoring: Displays traffic conditions and helps identify areas with heavy traffic.

Accident Detection: Explores how AI can identify possible accidents that can be checked by an operator.

Number Plate Recognition: Used EasyOCR to experiment with reading vehicle number plates.

Camera Monitoring: A dashboard interface to view camera feeds and traffic information.

Alert System: Explored sending notifications when a possible incident is detected.

 Technologies Used

Python: Main programming language used in the project.

Streamlit: Used to build the dashboard interface.

YOLOv8: Used for vehicle detection.

OpenCV: Used for image and video processing.

EasyOCR: Used for number plate recognition.

Plotly: Used for displaying graphs and visual information.

 How to Run the Project

1. Install Python on your computer.
2. Download or clone this repository.
3. Open the project folder in VS Code or a terminal.
4. Install the required libraries using `pip install -r requirements.txt`.
5. Run the application using `streamlit run app.py`.

The setup may need some changes depending on the model files and configuration used.

Screenshots

Screenshots of the dashboard and detection results can be added here to show how the project works.

What I Learned

Working on this project helped me understand how machine learning models can be used in practical applications.

I gained experience in Python programming, computer vision, working with different libraries and bringing multiple features together into one dashboard.

It also helped me understand that AI models are not always accurate. For example, a vehicle detection or accident detection system may sometimes give incorrect results. This is why human verification is important, especially when such systems are used for public safety.

Limitations

This project is a prototype developed for learning and demonstration purposes. It is not a fully tested traffic management or emergency response system.

The accuracy of detection can change depending on video quality, lighting, traffic conditions and other factors. Any possible accident detected by the system should be verified by a human operator.

Note

This repository is intended to contain only my own code and material that is safe to share publicly. No confidential Smart City data, private CCTV footage or sensitive information should be included.