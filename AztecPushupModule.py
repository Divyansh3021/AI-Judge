import cv2
import mediapipe as mp
import utils


class AztecPushupCounter:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.count = 0
        self.prev_state = self.current_state = None
        self.states = ["s1", "s2", "s3"]
        self.height = 0
        self.body_to_screen_ratio, self.ankle_wrist_distance_thresh, self.shoulder_hip_ankle, self.vert_wrist_elbow, self.vert_elbow_shoulder, self.shoulder_hip_ankle = utils.aztec_pushup_thresholds()
        self.prev_ankle_y, self.prev_wrist_y = 0, 0
        self.record = []
        self.flag = False
        self.record_exercise = True
        self.show_annotations = True
        self.feedback = None
        # self.mp_drawing = mp.solutions.drawing_utils
        # self.mp_pose = mp.solutions.pose

    def process_frame(self, frame):

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        frame_width, frame_height, _ = frame.shape
        print("Print0")
        if results:
            landmarks = results.pose_landmarks.landmark
            # self.show_annotations and mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
            print("Print1")

            left_wrist = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST]
            left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]
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
            head = landmarks[mp.solutions.pose.PoseLandmark.NOSE]
            
            # Convert landmarks to pixel coordinates
            head.x, head.y = head.x*frame_width, head.y*frame_height
            left_wrist.x, left_wrist.y  = left_wrist.x * frame_width, left_wrist.y * frame_height
            left_elbow.x, left_elbow.y  = left_elbow.x * frame_width, left_elbow.y * frame_height
            left_shoulder.x, left_shoulder.y = left_shoulder.x*frame_width, left_shoulder.y*frame_height
            left_hip.x, left_hip.y = left_hip.x*frame_width, left_hip.y*frame_height
            left_ankle.x, left_ankle.y = left_ankle.x*frame_width, left_ankle.y*frame_height
            left_knee.x, left_knee.y = left_knee.x*frame_width, left_knee.y*frame_height
            right_knee.x, right_knee.y = right_knee.x*frame_width, right_knee.y*frame_height

            # Calculating angles
            body_angle =90 - utils.old_vert_angle(head, left_ankle)
            vert_wrist_elbow_angle = utils.old_vert_angle(left_wrist, left_elbow)
            vert_elbow_shoulder_angle = utils.old_vert_angle(left_elbow, left_shoulder)
            shoulder_hip_ankle_angle = utils.angle(left_hip, left_shoulder, left_ankle)
            shoulder_hip_knee_angle = utils.angle(left_hip, left_shoulder, left_knee)

            ankle_wrist_distance = utils.distance(left_ankle, left_wrist)
            shoulder_ankle_distance = utils.distance(left_shoulder, left_ankle)
            self.height = max(self.height, utils.distance(left_wrist, left_ankle))

            body_to_screen_ratio = shoulder_ankle_distance / frame_width

            # if left_ankle.z < left_wrist.z :

            # cv2.putText(frame, f"Ankle wrist distance: 0", (10,260), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            print("Print5")
            
            # elif left_ankle.z > left_wrist.z :
            #     cv2.putText(frame, "Ankle in front ", (10,260), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 2)

            if 0<head.x<frame_width and 0< head.y < frame_height and 0 < left_ankle.x <frame_width and 0 < left_ankle.y <frame_height and 0 < right_ankle.x < frame_width and 0 < right_ankle.y < frame_height:

                if body_angle < 60:
                    if body_to_screen_ratio < 0.2:
                        self.feedback = "Come Closer"
                    elif body_to_screen_ratio > 0.8:
                        self.feedback = "Too Close!!"
                    else:
                        self.feedback = "Perfect"
                        print("Print2")

                        if body_to_screen_ratio < 0.2:
                            self.show_annotations and cv2.putText(frame, "Come Closer", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                        elif body_to_screen_ratio > 0.8:
                            self.show_annotations and cv2.putText(frame, "Too Close!!", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                        else:
                            self.show_annotations and cv2.putText(frame, "Perfect", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


                            if (self.shoulder_hip_ankle[2] >= shoulder_hip_knee_angle) and (self.prev_state == "s2") and (left_wrist.y < self.prev_wrist_y and left_ankle.y < self.prev_ankle_y):
                                self.current_state = self.states[2]     #current state = s3

                                if self.flag:
                                    status = "not good"
                                else:
                                    status = "good"

                            elif (self.shoulder_hip_ankle[0] >= shoulder_hip_knee_angle >= self.shoulder_hip_ankle[1])  and (self.vert_elbow_shoulder[0]<= vert_elbow_shoulder_angle<= self.vert_elbow_shoulder[1]):
                                self.current_state = self.states[0]   #Current state = s1
                                self.prev_wrist_y, self.prev_ankle_y = left_wrist.y , left_ankle.y

                            elif (self.shoulder_hip_ankle[1] > shoulder_hip_knee_angle >= self.shoulder_hip_ankle[2])  and (self.prev_state == "s1"):
                                self.current_state = self.states[1]   #current state = s2
                            
                            # else:
                            #     if ankle_wrist_distance> ankle_wrist_distance_thresh[0] and prev_state == "s2":
                            #         cv2.putText(frame, "touch ankle properly!!", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                            #         flag = True
                    

                            if self.current_state and self.show_annotations: cv2.putText(frame, "Current state: "+current_state, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 45, 255), 2)

                            if (self.prev_state == "s3" and self.current_state == "s1"):
                                self.count+=1
                                self.prev_state = None 
                                self.prev_wrist_y, self.prev_ankle_y = 0, 0
                                self.record.append(status)
                            
                            self.prev_state = self.current_state

                        # cv2.putText(frame, "Current Height: "+str(utils.distance(left_wrist, left_ankle)), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                else:
                    self.show_annotations and cv2.putText(frame, "Align properly", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            else:
                print("Print6")
                cv2.putText(frame, "Body out of frame", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        else:
            self.show_annotations and cv2.putText(frame, "No person detected", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        self.show_annotations and cv2.putText(frame, "Count: " + str(self.count), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
        self.show_annotations and cv2.putText(frame, "Body Angle: " + str(body_angle), (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
        # cv2.putText(frame, "Ankle: " + str(left_ankle.y), (10, 220), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 2)
        # cv2.putText(frame, "Wrist: " + str(left_wrist.y), (10,260), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 2)

        self.feedback and self.show_annotations and cv2.putText(frame, self.feedback, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if feedback == "Perfect" else (255, 0, 0), 2)
        print("print4")
        return frame