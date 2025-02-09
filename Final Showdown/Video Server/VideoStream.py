import cv2

class VideoStream:
    def __init__(self, filename):
        self.filename = filename
        self.cap = cv2.VideoCapture(filename)  # Open video file using OpenCV
        if not self.cap.isOpened():
            raise IOError(f"Cannot open video file {filename}")
        self.frameNum = 0

    def nextFrame(self, resize_to=(640, 360), quality=50):
    #def nextFrame(self, resize_to=(1280, 720), quality=50):
        """Get the next frame, resized and encoded with adjustable quality."""
        ret, frame = self.cap.read()
        if not ret:
            return None  # End of video

        # Resize the frame to reduce memory usage
        frame = cv2.resize(frame, resize_to)

        # Encode frame with adjustable JPEG quality
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        ret, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
        if not ret:
            raise ValueError("Error encoding frame")
        frame_data = encoded_frame.tobytes()

        self.frameNum += 1
        return frame_data

    def nextFrameBatch(self, batch_size=10, resize_to=(640, 360), quality=50):
    #def nextFrameBatch(self, batch_size=10, resize_to=(1280, 720), quality=50):
        """Get a batch of frames, resized and encoded."""
        frames = []
        for _ in range(batch_size):
            ret, frame = self.cap.read()
            if not ret:
                return None  # End of video

            # Resize the frame
            frame = cv2.resize(frame, resize_to)

            # Encode the frame
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            ret, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
            if not ret:
                raise ValueError("Error encoding frame")
            frame_data = encoded_frame.tobytes()

            frames.append(frame_data)

        return frames

    def frameNbr(self):
        """Get the current frame number."""
        return self.frameNum

    def release(self):
        """Release the video capture object and free memory."""
        self.cap.release()
        cv2.destroyAllWindows()