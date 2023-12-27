# from pushupModule import PushupCounter
# from PullupModule import PullupCounter
# from AztecPushupModule import AztecPushupCounter
# import cv2

# # counter = PushupCounter()
# # counter = PullupCounter()
# counter = AztecPushupCounter()

# # Open the webcam
# cap = cv2.VideoCapture("perfect_aztec_pushup.mp4")

# while cap.isOpened():
#     # Read a frame from the webcam
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Process the frame using PushupCounter
#     processed_frame = counter.process_frame(frame)

#     # Display the processed frame
#     cv2.imshow('Pushup Counter', processed_frame)

#     # Break the loop if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the webcam and close all OpenCV windows
# cap.release()
# cv2.destroyAllWindows()