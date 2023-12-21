import cv2
import mediapipe as mp
import utils


class PushupCounter:
    def __init__(self):
        # self.cap = cv2.VideoCapture(0)
        self.pose = mp.solutions.pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.count = 0
        self.prev_state = self.current_state = None
        self.states = ["s1", "s2", "s3"]
        self.ratio, self.vert_wrist_elbow, self.vert_elbow_shoulder, self.shoulder_hip_ankle = utils.pushup_thresholds()
        self.record_exercise = True
        self.show_annotations = True
        self.record = []
        self.flag = False

    def process_frame(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        frame_height, frame_width, _ = frame.shape

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            self.show_annotations and mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

            left_wrist = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST]
            left_elbow = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW]
            left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            left_knee = landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE]
            left_ankle = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE]
            left_hip = landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP]
            head = landmarks[mp.solutions.pose.PoseLandmark.NOSE]
            right_ankle = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE]
            print("print1")
            # Convert landmarks to pixel coordinates
            head.x, head.y = head.x * frame_width, head.y * frame_height
            left_wrist.x, left_wrist.y = left_wrist.x * frame_width, left_wrist.y * frame_height
            left_elbow.x, left_elbow.y = left_elbow.x * frame_width, left_elbow.y * frame_height
            left_shoulder.x, left_shoulder.y = left_shoulder.x * frame_width, left_shoulder.y * frame_height
            left_knee.x, left_knee.y = left_knee.x * frame_width, left_knee.y * frame_height
            left_hip.x, left_hip.y = left_hip.x * frame_width, left_hip.y * frame_height
            left_ankle.x, left_ankle.y = left_ankle.x * frame_width, left_ankle.y * frame_height
            right_ankle.x, right_ankle.y = right_ankle.x * frame_width, right_ankle.y * frame_height

            # Calculating angles
            body_angle = 90 - utils.vert_angle(left_shoulder, left_knee)
            vert_elbow_shoulder_angle = utils.vert_angle(left_elbow, left_shoulder)
            shoulder_hip_ankle_angle = utils.angle(left_hip, left_shoulder, left_ankle)

            shoulder_ankle_distance = utils.distance(left_shoulder, left_ankle)
            body_to_screen_ratio = shoulder_ankle_distance / frame_width

            if 0 < head.x < frame_width and 0 < head.y < frame_height and 0 < left_ankle.x < frame_width and 0 < left_ankle.y < frame_height and 0 < right_ankle.x < frame_width and 0 < right_ankle.y < frame_height:
                feedback = ""
                if body_angle < 60:
                    if body_to_screen_ratio < 0.2:
                        feedback = "Come Closer"
                    elif body_to_screen_ratio > 0.8:
                        feedback = "Too Close!!"
                    else:
                        feedback = "Perfect"
            
                        if (self.vert_elbow_shoulder[0] >= vert_elbow_shoulder_angle >= self.vert_elbow_shoulder[1])  and self.prev_state == "s2" :
                            self.current_state = self.states[0]

                            if self.flag:
                                status = tag
                            else:
                                status = "good"

                        elif self.vert_elbow_shoulder[0] >= vert_elbow_shoulder_angle >= self.self.vert_elbow_shoulder[1] :
                            self.current_state = self.states[0]

                        # elif self.vert_elbow_shoulder[1] > vert_elbow_shoulder_angle > self.vert_elbow_shoulder[2] and self.prev_state == "s1":
                        #     current_state = self.states[2]  #current state = s3

                        elif self.vert_elbow_shoulder[2] > vert_elbow_shoulder_angle >= self.vert_elbow_shoulder[3]  and self.prev_state == "s1" :
                            self.current_state = self.states[1]

                        elif current_state == "s1" and self.prev_state == "s3" :
                            self.show_annotations and cv2.putText(frame, "Go Low!!", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                        else:
                            # current_state = self.states[2]
                            if (shoulder_hip_ankle_angle < self.shoulder_hip_ankle[0]) :
                                cv2.putText(frame, "Keep your hip low!!", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                                self.flag = True
                                tag = "hip high"
                            
                            elif (shoulder_hip_ankle_angle > self.shoulder_hip_ankle[1]) :
                                cv2.putText(frame, "Keep your hip high!!", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                                self.flag = True
                                tag = "hip low"
                        print("print2")
                        if current_state and self.show_annotations:
                            cv2.putText(frame, 'Current state: ' + current_state, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                        self.show_annotations and cv2.putText(frame, f'Vertical elbow shoulder angle: {vert_elbow_shoulder_angle} ', (10, 260), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                        self.show_annotations and cv2.putText(frame, f'Shoulder_hip_ankle angle: {shoulder_hip_ankle_angle} ', (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                        if self.prev_state == "s2" and current_state == "s1":
                            self.count += 1
                            self.prev_state = None 

                            if self.record_exercise:
                                self.record.append(status)

                        self.prev_state = current_state

                        cv2.putText(frame, "Count: " + str(self.count), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

                # cv2.putText(frame, feedback, (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if feedback == "Perfect" else (255, 0, 0), 2)
            else:
                self.show_annotations and cv2.putText(frame, "BODY OUT OF FRAME", (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))


        else:
            self.show_annotations and cv2.putText(frame, "No person detected", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        print("print3")
        return frame
