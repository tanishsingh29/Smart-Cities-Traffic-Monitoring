import streamlit as st
import cv2
import pandas as pd
import tempfile
import time
from ultralytics import YOLO
from twilio.rest import Client

st.set_page_config(
    page_title="INTEGRATED COMMAND & CONTROL CENTRE - PATNA",
    layout="wide"
)

st.markdown("""
<style>
body { background-color: #0f172a; }
.main { background-color: #0f172a; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("INTEGRATED COMMAND & CONTROL CENTRE - PATNA")

st.sidebar.title("FOOTAGE PANEL")

uploaded_video = st.sidebar.file_uploader(
    "Upload Footage/ Camera IP",
    type=["mp4", "avi", "mov"]
)

confidence = st.sidebar.slider("Detection Confidence", 0.1, 1.0, 0.4)

st.sidebar.markdown("---")
st.sidebar.subheader("WhatsApp Alert Setup")

account_sid = st.sidebar.text_input("Twilio Account SID", type="password")
auth_token = st.sidebar.text_input("Twilio Auth Token", type="password")

from_whatsapp = st.sidebar.text_input(
    "Twilio WhatsApp Number",
    "+14058709156"
)

to_whatsapp = st.sidebar.text_input(
    "Receiver WhatsApp Number",
    "+916205356146"
)

start_button = st.sidebar.button("Start Detection")


@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")


model = load_model()

vehicle_classes = {
    2: "Car",
    3: "Two Wheeler",
    5: "Bus",
    7: "Truck"
}

def send_whatsapp_alert(message):
    try:
        if not account_sid or not auth_token:
            st.warning("Twilio SID or Auth Token missing.")
            return False

        client = Client(account_sid, auth_token)

        client.messages.create(
            body=message,
            from_=from_whatsapp,
            to=to_whatsapp
        )

        return True

    except Exception as e:
        st.error(f"WhatsApp Alert Failed: {e}")
        return False

def calculate_iou(box1, box2):
    x1, y1, x2, y2 = box1
    a1, b1, a2, b2 = box2

    inter_x1 = max(x1, a1)
    inter_y1 = max(y1, b1)
    inter_x2 = min(x2, a2)
    inter_y2 = min(y2, b2)

    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)

    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (a2 - a1) * (b2 - b1)

    union_area = box1_area + box2_area - inter_area

    if union_area == 0:
        return 0

    return inter_area / union_area


col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Live Traffic Feed")
    video_placeholder = st.empty()

with col2:
    st.subheader("Traffic Analytics")

    car_metric = st.empty()
    bike_metric = st.empty()
    bus_metric = st.empty()
    truck_metric = st.empty()

    st.markdown("---")

    fps_metric = st.empty()
    accident_metric = st.empty()

    st.markdown("---")

    alert_placeholder = st.empty()


st.markdown("---")
st.subheader("Traffic Volume Trend")

chart_placeholder = st.empty()


if uploaded_video is not None and start_button:

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_file.write(uploaded_video.read())
    temp_file.close()

    cap = cv2.VideoCapture(temp_file.name)

    graph_data = []
    frame_counter = 0
    accident_alert_sent = False

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            break

        start_time = time.time()

        results = model(frame, conf=confidence, verbose=False)[0]

        car_count = 0
        bike_count = 0
        bus_count = 0
        truck_count = 0

        vehicle_boxes = []
        accident_detected = False

        for box in results.boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if cls in vehicle_classes:

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = vehicle_classes[cls]

                vehicle_boxes.append((x1, y1, x2, y2))

                if cls == 2:
                    car_count += 1
                elif cls == 3:
                    bike_count += 1
                elif cls == 5:
                    bus_count += 1
                elif cls == 7:
                    truck_count += 1

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

                cv2.putText(
                    frame,
                    f"{label} {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2
                )

        for i in range(len(vehicle_boxes)):
            for j in range(i + 1, len(vehicle_boxes)):

                iou = calculate_iou(vehicle_boxes[i], vehicle_boxes[j])

                if iou > 0.25:
                    accident_detected = True

                    x1, y1, x2, y2 = vehicle_boxes[i]

                    cv2.putText(
                        frame,
                        "ACCIDENT RISK DETECTED",
                        (x1, y1 - 35),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        3
                    )

        total_vehicles = car_count + bike_count + bus_count + truck_count

        end_time = time.time()
        fps = 1 / max(end_time - start_time, 0.001)

        car_metric.metric("Cars", car_count)
        bike_metric.metric("Two Wheelers", bike_count)
        bus_metric.metric("Buses", bus_count)
        truck_metric.metric("Trucks", truck_count)
        fps_metric.metric("System FPS", int(fps))

        if accident_detected:
            accident_metric.error("Accident Risk: YES")
            alert_placeholder.error("Accident Risk Detected")

            if not accident_alert_sent:
                message = (
                    "ALERT: ICCC Detected Accident at Highway. Immediate intervention by Police and Ambulance Services is required to prevent loss of life and ensure public safety. "
                    "INTEGRATED COMMAND & CONTROL CENTRE - PATNA."
                )

                send_whatsapp_alert(message)
                accident_alert_sent = True

        else:
            accident_metric.success("Accident Risk: NO")

            if total_vehicles > 20:
                alert_placeholder.error("High Traffic Congestion Detected")
            else:
                alert_placeholder.success("Traffic Flow Normal")

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        video_placeholder.image(
            frame,
            channels="RGB",
            use_container_width=True
        )

        graph_data.append({
            "Frame": frame_counter,
            "Total Vehicles": total_vehicles,
            "Cars": car_count,
            "Two Wheelers": bike_count,
            "Buses": bus_count,
            "Trucks": truck_count,
            "Accident Risk": accident_detected
        })

        frame_counter += 1

        df = pd.DataFrame(graph_data)

        chart_placeholder.line_chart(
            df.set_index("Frame")[["Total Vehicles"]]
        )

    cap.release()

    st.success("Traffic Analysis Completed Successfully")

else:
    st.info("Please upload a traffic video and click Start Detection.")