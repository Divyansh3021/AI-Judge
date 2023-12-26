import cv2, mediapipe as mp
import math
import utils

class PullupCounter:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.7)
        self.count = 0
        self.prev_state = self.current_state = None
        self.states = ["s1", "s2", "s3"]
        self.record_exercise = True
        self.show_annotations = True
        self.record = []
        self.flag = False
        self.body_to_screen_ratio,self.elbow_shoulder_hip, self.shoulder_hip_ankle = utils.pullup_thresholds()
        self.ankle_y = [0,0]
        self.height = 0

    def process_frame(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        # print(results.pose_landmarks.landmark)
        frame_height, frame_width, _ = frame.shape
        # print(frame_height, frame_width)
        print("Print0")

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            self.show_annotations and mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

            left_wrist = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST]
            left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]
            head = landmarks[mp.solutions.pose.PoseLandmark.NOSE]
            left_hip = landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP]
            left_ankle = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE]
            right_ankle = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE]
            left_elbow = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW]
            right_elbow = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW]
            left_wrist = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST]
            left_knee = landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE]
            right_knee = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE]

            print("Print1")

            # print("left wrist: ", left_wrist.x * frame_width, left_wrist.y * frame_height)
            # print("left shoulder: ", left_shoulder.x * frame_width, left_shoulder.y * frame_height)
            # print("left ankle: ", left_ankle)


            left_wrist.x, left_wrist.y  = left_wrist.x * frame_width, left_wrist.y * frame_height
            left_elbow.x, left_elbow.y  = left_elbow.x * frame_width, left_elbow.y * frame_height
            left_shoulder.x, left_shoulder.y = left_shoulder.x*frame_width, left_shoulder.y*frame_height
            left_hip.x, left_hip.y = left_hip.x*frame_width, left_hip.y*frame_height
            left_ankle.x, left_ankle.y = left_ankle.x*frame_width, left_ankle.y*frame_height
            left_knee.x, left_knee.y = left_knee.x*frame_width, left_knee.y*frame_height

            right_wrist.x, right_wrist.y  = right_wrist.x * frame_width, right_wrist.y * frame_height
            right_elbow.x, right_elbow.y  = right_elbow.x * frame_width, right_elbow.y * frame_height
            right_shoulder.x, right_shoulder.y = right_shoulder.x*frame_width, right_shoulder.y*frame_height
            right_hip.x, right_hip.y = right_hip.x*frame_width, right_hip.y*frame_height
            right_ankle.x, right_ankle.y = right_ankle.x*frame_width, right_ankle.y*frame_height
            right_knee.x, right_knee.y = right_knee.x*frame_width, right_knee.y*frame_height

            shoulder_avg = [(left_shoulder.x + right_shoulder.x)/2, (left_shoulder.y + right_shoulder.y)/2]
            ankle_avg = [(left_ankle.x + right_ankle.x)/2, (left_ankle.y + right_ankle.y)/2]
            knee_avg = [(left_knee.x + right_knee.x)/2, (left_knee.y + right_knee.y)/2]

            # print("Left wrist: ", left_wrist)

            #Calculating angles
            body_angle =  max(utils.vert_angle(left_shoulder, left_knee), utils.vert_angle(right_shoulder, right_knee))
            left_elbow_shoulder_hip_angle = utils.angle(left_shoulder, left_elbow, left_hip)
            right_elbow_shoulder_hip_angle = utils.angle(right_shoulder, right_elbow, right_hip)

            # Other angle calculations

            shoulder_ankle_distance = utils.distance(left_shoulder, left_ankle)
            body_to_screen_ratio = shoulder_ankle_distance / frame_height

            # cv2.putText(frame, "Left: "+str(int(left_ankle.y))+" Right: "+str(int(right_ankle.y)), (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if 0 < head.x * frame_width < frame_width and 0 < head.y * frame_height < frame_height and 0 < left_ankle.x < frame_width and 0 < left_ankle.y < frame_height and 0 < right_ankle.x < frame_width and 0 < right_ankle.y < frame_height:
                if  body_angle > 70:
                    feedback = ""
                    print("Print2")

                    if body_to_screen_ratio < 0.2:
                        feedback = "Come Closer!!"
                    elif body_to_screen_ratio > 0.8:
                        feedback = "Too Close!!"
                    else:
                        feedback = "Perfect!"
                        
                        print("Print3")
                        if ((self.elbow_shoulder_hip[0] >= left_elbow_shoulder_hip_angle >= self.elbow_shoulder_hip[1]) and
                            (self.elbow_shoulder_hip[0] >= right_elbow_shoulder_hip_angle >= self.elbow_shoulder_hip[1])) and (self.prev_state == "s2"):
                            self.current_state = self.states[0]
                            self.ankle_y = [left_ankle.y, right_ankle.y]

                            if self.flag:
                                status = self.tag
                            else:
                                status = "good"

                        elif ((self.elbow_shoulder_hip[0]>= left_elbow_shoulder_hip_angle>= self.elbow_shoulder_hip[1]) and (self.elbow_shoulder_hip[0]>= right_elbow_shoulder_hip_angle>= self.elbow_shoulder_hip[1])):
                            # current_state = states[0]   #Current state = s1
                            self.current_state = self.states[0]
                            self.ankle_y = [left_ankle.y, right_ankle.y]
                            self.height = utils.distance(left_shoulder, left_knee)

                        elif ((self.elbow_shoulder_hip[1] > left_elbow_shoulder_hip_angle >= self.elbow_shoulder_hip[2]) and
                            (self.elbow_shoulder_hip[1] > right_elbow_shoulder_hip_angle >= self.elbow_shoulder_hip[2])) and (self.prev_state == "s1") and (left_ankle.y < self.ankle_y[0] and right_ankle.y < self.ankle_y[1]) and (abs(self.height - (math.sqrt((left_shoulder.x - left_knee.x)**2 + (left_shoulder.y - left_knee.y)**2))) < self.height/10):
                            self.current_state = self.states[1]  # current state = s2

                        else:
                            if (left_elbow_shoulder_hip_angle > self.elbow_shoulder_hip[0]) and (right_elbow_shoulder_hip_angle > self.elbow_shoulder_hip[0]):

                                if self.show_annotations:
                                    cv2.putText(frame, "Open Arms wider!", (700, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                                self.flag = True
                                tag = "Arms too close"
                        
                        if self.current_state and self.show_annotations:
                            cv2.putText(frame, 'Current state: '+ self.current_state, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                        if (self.prev_state == "s2" and self.current_state == "s1"):
                            self.count+=1
                            self.prev_state = None 

                            if self.record_exercise:
                                self.record.append(status)
                        
                        self.prev_state = self.current_state

                        cv2.putText(frame, "Count: "+str(self.count), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            else:
                cv2.putText(frame, "Body out of frame", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        else:
            self.show_annotations and cv2.putText(frame, "No person detected", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        print("Print4")
        return frame