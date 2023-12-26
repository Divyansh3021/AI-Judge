from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
from aiortc.contrib.media import MediaRecorder
import streamlit as st
from pushupModule import PushupCounter
from PullupModule import PullupCounter
from AztecPushupModule import AztecPushupCounter
import av

st.title("Sports AI Judge")

exercises = ["Pushup", "Pullup", "Aztec Pushup"]
selected_exercise = st.selectbox("Select Exercise", exercises)

if selected_exercise == "Pushup":
    live_frame_process = PushupCounter()
elif selected_exercise == "Pullup":
    live_frame_process = PullupCounter()
elif selected_exercise == "Aztec Pushup":
    live_frame_process = AztecPushupCounter()

def video_frame_callback(frame: av.VideoFrame):
    frame = frame.to_ndarray(format="rgb24")
    frame = live_frame_process.process_frame(frame)
    return av.VideoFrame.from_ndarray(frame, format = "rgb24")

output_video_file = f"output_live.flv"

def out_recorder_factory() -> MediaRecorder:


        return MediaRecorder(output_video_file)
ctx = webrtc_streamer(
                        key="Squats-pose-analysis",
                        video_frame_callback=video_frame_callback,
                        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},  # Add this config
                        media_stream_constraints={"video": {"width":1080, "height":720}, "audio": False},
                        video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False, width="100%", height = "100%"),
                        out_recorder_factory=out_recorder_factory
                    )