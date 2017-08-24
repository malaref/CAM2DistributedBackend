import cv2

from analyzer.analyzer import Analyzer

class MyAnalyzer(Analyzer):
    
    def __int__(self, id):
        Analyzer.__int__(self, id)

    def initialize(self):
        self.bgsub = cv2.BackgroundSubtractorMOG()
        self.frames_num = 0
        self.total_motion = 0

    def on_new_frame(self):
        frame_metadata = self.get_frame_metadata()
        file_name = '{}_{}'.format(
            frame_metadata.camera_metadata.camera_id,
            frame_metadata.datetime.strftime('%Y-%m-%d_%H-%M-%S-%f'))

        frame = self.get_frame()
        self.save(file_name + '_input.png', frame)

        frame = self.bgsub.apply(frame)
        self.save(file_name + '_mask.png', frame)

        motion = cv2.countNonZero(frame) / float(frame.size)
        self.save(file_name + '_motion.txt', motion)

        self.frames_num += 1
        self.total_motion += motion

    def finalize(self):
        self.save('average_motion.txt', self.total_motion / self.frames_num)
