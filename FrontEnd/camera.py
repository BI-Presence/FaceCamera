import subprocess
import cv2
import numpy as np
import time
from keras_facenet import FaceNet
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
from mtcnn import MTCNN
from flask import Flask, render_template, Response
import webbrowser

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Muat model dan encoder
model = load_model('../AppBack/backend/media/mtcnn_facenet_ann_model.h5')
with open('../AppBack/backend/media/face_labels.txt', 'r') as file:
    LABELS = [line.strip() for line in file.readlines()]

encoder = LabelEncoder()
encoder.fit(LABELS)

# Inisialisasi FaceNet dan detektor MTCNN
embedder = FaceNet()
img_detector = MTCNN()

# Load Haar Cascade untuk deteksi senyum dan mata
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Variabel untuk melacak posisi sebelumnya dari wajah (head movement)
prev_bbox = None
movement_threshold = 10  # Threshold untuk menganggap pergerakan kepala signifikan

# Variabel untuk melacak label dan waktu kemunculan
last_label = None
label_start_time = None
required_label_duration = 3  # Label harus muncul selama 3 detik

def get_embedding(face_img):
    face_img = np.asarray(face_img, dtype=np.float32)
    face_img = np.expand_dims(face_img, axis=0)
    return embedder.embeddings(face_img)[0]

def predict_class(embedding, model, encoder, threshold=0.9):
    """Memprediksi label dari embedding dan menentukan confidence score."""
    test_embedding = np.expand_dims(embedding, axis=0)
    predict_proba = model.predict(test_embedding)[0]
    predicted_class = np.argmax(predict_proba)
    confidence_score = predict_proba[predicted_class]

    if confidence_score < threshold:
        predicted_label = "unknown"
        confidence_percentage = 0.0  # Set confidence to 0% for unknown faces
    else:
        predicted_label = encoder.inverse_transform([predicted_class])[0]
        confidence_percentage = confidence_score * 100  # Confidence in percentage

    return predicted_label, confidence_percentage

def open_url_in_browser(url):
    """Fungsi untuk membuka URL di browser menggunakan webbrowser."""
    print(f"Membuka URL: {url}")
    try:
        webbrowser.open(url)
        print("Berhasil membuka browser!")
    except Exception as e:
        print(f"Gagal membuka browser: {e}")

def load_and_preprocess_image_from_frame(frame):
    """Convert frame to RGB, resize, dan return resized image and bbox"""
    t_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    height, width, _ = t_img.shape
    scale = min(480 / width, 480 / height)
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_img = cv2.resize(t_img, (new_width, new_height))
    detections = img_detector.detect_faces(resized_img)
    if detections:
        x, y, w, h = detections[0]['box']
        return resized_img, (x, y, w, h)
    return resized_img, None

def crop_and_get_embedding(image, bbox, target_size=(160, 160)):
    x, y, w, h = bbox
    face_img = image[y:y+h, x:x+w]
    face_img = cv2.resize(face_img, target_size)
    return get_embedding(face_img)

def detect_smile_and_eyes(face_img):
    """Detect smile and eyes in the face image using Haar Cascade"""
    gray_face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    
    # Deteksi senyum
    smiles = smile_cascade.detectMultiScale(gray_face_img, scaleFactor=1.8, minNeighbors=20, minSize=(25, 25))
    smile_detected = len(smiles) > 0

    # Deteksi mata
    eyes = eye_cascade.detectMultiScale(gray_face_img, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20))
    eye_detected = len(eyes) >= 2  # Menganggap dua mata harus terdeteksi

    return smile_detected, eye_detected

def is_head_moving(current_bbox, prev_bbox, threshold):
    """Check if the head has moved significantly"""
    if prev_bbox is None:
        return False  # No previous position to compare with
    x1, y1, w1, h1 = current_bbox
    x2, y2, w2, h2 = prev_bbox
    movement = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return movement > threshold

def generate_frames():
    global prev_bbox, last_label, label_start_time

    cap = cv2.VideoCapture(0)  # 0 adalah kamera default
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Proses frame
        resized_img, bbox = load_and_preprocess_image_from_frame(frame)
        if bbox:
            x, y, w, h = bbox
            face_img = resized_img[y:y+h, x:x+w]

            # Tambahkan kotak di sekitar wajah
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Cek pergerakan kepala
            head_moved = is_head_moving(bbox, prev_bbox, movement_threshold)
            prev_bbox = bbox  # Simpan posisi wajah saat ini sebagai posisi sebelumnya

            # Deteksi senyum dan mata
            smile_detected, eyes_detected = detect_smile_and_eyes(face_img)

            # Jika kepala bergerak, senyum dan mata terdeteksi, anggap wajah sebagai manusia asli
            if smile_detected and eyes_detected and head_moved:
                test_img = crop_and_get_embedding(resized_img, bbox)
                predicted_label, confidence_percentage = predict_class(test_img, model, encoder)
                cv2.putText(frame, f"Label: {predicted_label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, f"Confidence: {confidence_percentage:.2f}%", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

                current_time = time.time()

                if predicted_label == last_label:
                    # Jika label sama seperti sebelumnya, cek apakah sudah muncul selama 3 detik
                    if current_time - label_start_time >= required_label_duration:
                        print(f"Label yang terdeteksi: {predicted_label}")
                        # Buka halaman berdasarkan label
                        if "supervisor" in predicted_label:
                            print("Membuka halaman Supervisor")
                            open_url_in_browser("https://www.bi.go.id/id/default.aspx")
                        elif "employee" in predicted_label:
                            print("Membuka halaman Employee")
                            open_url_in_browser("https://www.bi.go.id/id/karier/internship-program.aspx")
                else:
                    # Reset jika label berubah
                    print(f"Label berubah dari {last_label} ke {predicted_label}")
                    last_label = predicted_label
                    label_start_time = current_time
            else:
                cv2.putText(frame, "Liveness detection failed", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Encode frame ke dalam format yang bisa ditampilkan di web
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Kirimkan frame dalam bentuk stream ke browser
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
