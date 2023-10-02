from flask import Flask, render_template, Response, jsonify,request
import cv2
import json
import time
import numpy as np
from keras.models import load_model

app = Flask(__name__)

# Load the HDF5 model
hdf5_model_path = "D:/STARTUP1/Mentor/model_25img_t1_34v_colab.hdf5"
engagement_detector = load_model(hdf5_model_path)

model_running = False

# Data structure to store analysis results
analysis_results = {
    'timestamps': [],
    'engagement_scores': []
}

def detect_engagement(frame):
    # Preprocess the frame as needed (e.g., resize, normalize)
    resized_frame = cv2.resize(frame, (40, 40))  # Replace with your desired dimensions
    normalized_frame = resized_frame / 255.0  # Normalize pixel values if necessary
    
    # Make predictions using your loaded HDF5 model
    engagement_prediction = engagement_detector.predict(np.expand_dims(normalized_frame, axis=0))
    
    # You can perform further processing on the prediction if necessary
    engagement_result = engagement_prediction[0][0]  # Extract the prediction result

    # Get the current timestamp
    timestamp = time.time()
     # Append the results to the data structure
    analysis_results['timestamps'].append(timestamp)
    analysis_results['engagement_scores'].append(engagement_result)

    return engagement_result  # Return the engagement prediction as a number
def generate_frames():
    camera = cv2.VideoCapture(0)  # Open the default camera (0)

    while True:
        success, frame = camera.read()  # Read a frame from the camera

        if not success:
            break

        if model_running:
            # Perform engagement detection on the frame
            engagement_result = detect_engagement(frame)
            # Draw the engagement result on the frame as a string
            cv2.putText(frame, f'Engagement: {engagement_result:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Convert the frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

    camera.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    global model_running
    if request.args.get('action')=='start':
        model_running = True
    elif request.args.get('action')=='stop':
        model_running = False
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_engagement')
def get_engagement():
    # You should implement a method in your Engagement_Detection class to get the current engagement level.
    # This method should return the engagement level as a number.
    global model_running
    return jsonify({'model_running': model_running})
    #engagement_result = 0  # Replace with your method to get the engagement result
    #return jsonify({'engagement': engagement_result})
@app.route('/save_results')
def save_results():
    # Save analysis_results to a JSON file
    with open('analysis_results.json', 'w') as json_file:
        json.dump(analysis_results, json_file)
    return jsonify({'message': 'Analysis results saved to JSON file'})

if __name__ == '__main__':
    app.run(debug=True)
