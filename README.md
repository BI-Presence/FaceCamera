# FaceCameraApp
## Introduction
FaceCameraApp is a facial recognition system designed to facilitate real-time identity verification for logging into a webpage based on employee status. Using a combination of Cascade Classifier for face detection, FaceNet for feature extraction, and Artificial Neural Network (ANN) for classification, the system provides accurate and efficient face recognition capabilities. As well as detecting using smiles and head movements. The language used is python with django admin database.
## Meet The Team
| NIM      | Name                         | University                             | Scope of Task                                                                                                                                                                                                                              |
| ---------| --------------------------   | ---------------------------------------| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 17210809 | Roslina Puspita              | Universitas Bina Sarana Informatika    | Model Research, Dataset Collection, Data Processing, Deep Learning Model Development, Model Training, Testing & Optimization, Model Deployment, Real-Time Face Recognition, Model Training, ML-Frontend Integration, ML Backend, Frontend & Backend initial view, Documentation |
| 17210640 | Lailatul Qodariyah           | Universitas Bina Sarana Informatika    | Model Research, Dataset Collection, Refine the initial look of the Backend, ML Backend, Backend creation of enhancements that have been made |
| 19210759 | Syifa Rahma Leily            | Universitas Bina Sarana Informatika    | Part of the Backend, Create a login on the backend that only supervisors can enter | |
| 19210782 | Fransisca Kusuma             | Universitas Bina Sarana Informatika    | Creating Frontend Views using Frames and BI Logos |
| 15210380 | Raihan Juniargho             | Universitas Bina Sarana Informatika    | Creating Frontend Views using Frames and BI Logos |

## Flow Diagram for Face Detection and Recognition
The following diagram illustrates the step-by-step process for face detection and recognition using MTCNN to detect faces, FaceNet to extract facial features, and ANN to classify faces as well as detection using smiles and head movements :


## Requirements
To run this project, you need the following Python packages with their specified versions :
- blinker==1.8.2
- CacheControl==0.14.0
- cachetools==5.5.0
- certifi==2024.8.30
- cffi==1.17.1
- charset-normalizer==3.3.2
- click==8.1.7
- cmake==3.30.3
- colorama==0.4.6
- cryptography==43.0.1
- cvzone==1.6.1
- dlib==19.24.6
- face-recognition==1.3.0
- face-recognition-models==0.3.0
- firebase-admin==6.5.0
- Flask==3.0.3
- google-api-core==2.20.0
- google-api-python-client==2.147.0
- google-auth==2.35.0
-  google-auth-httplib2==0.2.0
- google-cloud-core==2.4.1
- google-cloud-firestore==2.19.0
- google-cloud-storage==2.18.2
- google-crc32c==1.6.0
- google-resumable-media==2.7.2
- googleapis-common-protos==1.65.0
- grpcio==1.66.1
- grpcio-status==1.66.1
- httplib2==0.22.0
- idna==3.10
- itsdangerous==2.2.0
- Jinja2==3.1.4
- MarkupSafe==2.1.5
- msgpack==1.1.0
- numpy==2.1.1
- opencv-python==4.10.0.84
- pillow==10.4.0
- proto-plus==1.24.0
- protobuf==5.28.2
- pyasn1==0.6.1
- pyasn1_modules==0.4.1
- pycparser==2.22
- PyJWT==2.9.0
- pyparsing==3.1.4
- requests==2.32.3
- rsa==4.9
- uritemplate==4.1.1
- urllib3==2.2.3
- Werkzeug==3.0.4

## This Project Allow :
- Python 3.10.5

Check the following installation if there is no please install this :
- flask 
- cv2
- face_recognition
- numpy
- cvzone
- firebase_admin

## Installation
To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/BI-Presence/FaceCameraApp.git
   cd PROJECTAPP
    ```
   
2. Create a virtual environment:
   ```bash
   python -m venv my_env
   ```

3. Activate the virtual environment:
   ```bash
   my_env\Scripts\activate
    ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Install other package in description :
    - flask
   - cv2
   - face_recognition
   - numpy
   - cvzone
   - firebase_admin

6. Run Example Camera:
   python app.py

7. Access the application:
   Open your web browser and go to http://127.0.0.1:8000


Folder:
- The Try folder contains ML Code on the Front End and also the Frontend Camera
- AppBack folder is a folder that contains the Backend in the project created both ML and also the Backend View
