import math

def pushup_thresholds():
    body_to_screen_ratio = [0.2,0.8]
    vert_wrist_elbow = [0,15,30]
    vert_elbow_shoulder = [180, 130, 90, 30]
    shoulder_hip_ankle = [170, 185]

    return body_to_screen_ratio,vert_wrist_elbow, vert_elbow_shoulder, shoulder_hip_ankle

def pullup_thresholds():
    body_to_screen_ratio = [0.2,0.8]
    elbow_shoulder_hip = [170, 105, 20]
    shoulder_hip_ankle = [170, 185]
    return body_to_screen_ratio,elbow_shoulder_hip, shoulder_hip_ankle

def aztec_pushup_thresholds():
    body_to_screen_ratio = [0.2,0.8]
    vert_wrist_elbow = [0,15,30]
    vert_elbow_shoulder = [0, 60, 120]
    shoulder_hip_ankle = [170, 185]
    ankle_wrist_distance = [60]
    shoulder_hip_ankle = [180, 130, 90, 20]

    return body_to_screen_ratio,ankle_wrist_distance, shoulder_hip_ankle, vert_wrist_elbow, vert_elbow_shoulder, shoulder_hip_ankle

# def vert_angle(point1, point2):

#     # Calculate the slope of the line (rise over run)
#     delta_y = point2.y - point1.y
#     delta_x = point2.x - point1.x

#     # Ensure there's no division by zero
#     if delta_x == 0 and delta_y == 0:
#         raise Exception("Same points")

#     elif delta_x == 0:
#         return "same x"
    
#     elif delta_y == 0:
#         return "same y"

#     # Calculate the angle with the vertical using arctangent
#     angle_rad = math.atan(delta_x / delta_y)

#     # Convert the angle from radians to degrees
#     angle_deg = math.degrees(angle_rad)

#     # Return the angle with the vertical
#     return int(math.fabs(angle_deg))

def vert_angle(point1, point2):
    # Calculate the slope of the line (rise over run)
    delta_y = point2.y - point1.y
    delta_x = point2.x - point1.x

    # Ensure there's no division by zero
    if delta_x == 0 and delta_y == 0:
        raise Exception("Same points")

    # Calculate the angle with the vertical using arctangent
    angle_rad = math.atan2(delta_x, delta_y)  # Swap delta_x and delta_y

    # Convert the angle from radians to degrees
    angle_deg = math.degrees(angle_rad)

    # Ensure the angle is positive
    if angle_deg < 0:
        angle_deg += 180  # Adjust for the angle with the vertical

    return angle_deg


def old_vert_angle(point1, point2):

    # Calculate the slope of the line (rise over run)
    delta_y = point2.y - point1.y
    delta_x = point2.x - point1.x

    # Ensure there's no division by zero
    if delta_x == 0 and delta_y == 0:
        raise Exception("Same points")

    elif delta_x == 0:
        return "same x"
    
    elif delta_y == 0:
        return "same y"

    # Calculate the angle with the vertical using arctangent
    angle_rad = math.atan(delta_x / delta_y)

    # Convert the angle from radians to degrees
    angle_deg = math.degrees(angle_rad)

    # Return the angle with the vertical
    return int(math.fabs(angle_deg))

# def angle(point1, point2, point3):
#     """ Calculate angle between two lines """
#     point1 = (point1.x, point1.y)
#     point2 = (point2.x, point2.y)
#     point3 = (point3.x, point3.y)

#     if(point1==(0,0) or point2==(0,0) or point3==(0,0)):
#         return 0
#     numerator = point2[1] * (point1[0] - point3[0]) + point1[1] * \
#                 (point3[0] - point2[0]) + point3[1] * (point2[0] - point1[0])
#     denominator = (point2[0] - point1[0]) * (point1[0] - point3[0]) + \
#                 (point2[1] - point1[1]) * (point1[1] - point3[1])
#     try:
#         ang = math.atan(numerator/denominator)
#         ang = ang * 180 / math.pi
#         if ang < 0:
#             ang = 180 + ang
#         return ang
#     except:
#         return 90.0

def angle(point2, point1, point3):
    x1, y1, x2, y2, x_common, y_common = point1.x, point1.y, point3.x, point3.y, point2.x, point2.y
    # Calculate the vectors formed by the common point and the two points on the lines
    vector1 = (x1 - x_common, y1 - y_common)
    vector2 = (x2 - x_common, y2 - y_common)

    # Calculate the dot product of the two vectors
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

    # Calculate the magnitudes of the vectors
    magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
    magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

    # Calculate the cosine of the angle using the dot product and magnitudes
    cosine_angle = dot_product / (magnitude1 * magnitude2)

    # Calculate the angle in radians using the arccosine function
    angle_rad = math.acos(cosine_angle)

    # Convert the angle from radians to degrees
    angle_deg = math.degrees(angle_rad)

    # Return the angle between the two lines
    return int(math.fabs(angle_deg))


# def angle_of_singleline(point1, point2):

#     point1 = (point1.x, point1.y)
#     point2 = (point2.x, point2.y)

#     """ Calculate angle of a single line """
#     x_diff = point2[0] - point1[0]
#     y_diff = point2[1] - point1[1]
#     return math.degrees(math.atan2(y_diff, x_diff))

def distance(point1, point2):
    # Calculate the horizontal and vertical differences
    delta_x = point2.x - point1.x
    delta_y = point2.y - point1.y

    # Use the Pythagorean theorem to calculate the distance
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

    return int(math.fabs(distance))

def body_angle(shoulder_avg, ankle_avg):
    # Calculate the slope of the line (rise over run)
    delta_y = ankle_avg[1] - shoulder_avg[1]
    delta_x = ankle_avg[0] - shoulder_avg[0]

    # Ensure there's no division by zero
    if delta_x == 0 and delta_y == 0:
        raise Exception("Same points")

    elif delta_x == 0:
        return "same x"
    
    elif delta_y == 0:
        return "same y"

    # Calculate the angle with the vertical using arctangent
    angle_rad = math.atan(delta_x / delta_y)

    # Convert the angle from radians to degrees
    angle_deg = math.degrees(angle_rad)

    # Return the angle with the vertical
    return int(math.fabs(angle_deg))