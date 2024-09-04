import cv2
from gaze_tracking import GazeTracking


class GazeTrackingExtended(GazeTracking):
    def is_looking_at_screen(self):
        """Returns true if the user is looking at the screen"""
        if self.pupils_located:
            horizontal = self.horizontal_ratio()
            vertical = self.vertical_ratio()
            return 0.35 < horizontal < 0.65 and 0.35 < vertical < 0.65
        return False


gaze = GazeTrackingExtended()
webcam = cv2.VideoCapture(0)

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "goz kirpma"
    elif gaze.is_right():
        text = "Solo bakmak"
    elif gaze.is_left():
        text = "Saga bakmak"
    # elif gaze.is_center():
    #     text = "Merkeze bakmak"

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    if left_pupil is not None and right_pupil is not None:
        if gaze.is_looking_at_screen():
            text += " - Ekrana Bakiyor"
        else:
            text += " - Ekrana Bakmiyor"
        # os.system('xrandr --output eDP-1 --brightness 1')
        # os.system('xrandr --output HDMI-1-1 --brightness 0.1')
    else:
        text += " - Goz Bebekleri Bulunamiyor"
        # os.system('xrandr --output eDP-1 --brightness 0.1')
        # os.system('xrandr --output HDMI-1-1 --brightness 1')

    # cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
    cv2.putText(frame, "Sol goz bebegi:  " + str(left_pupil), (0, 30), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Sag goz bebegi: " + str(right_pupil), (0, 65), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break

webcam.release()
cv2.destroyAllWindows()
