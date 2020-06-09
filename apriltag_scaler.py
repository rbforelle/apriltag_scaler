import math
import os


class ApriltagScaler(object):
    def __init__(self, printer_dpi=72):
        self.dpi = printer_dpi  # normal printer default DPI = 72
        self.inch_mm = 25.4  # 1inch = 25.4mm
        self.marker_mm = None
        self.marker_pix = None
        self.png_mm = None
        self.png_pix = None

    def recommended_value(self, dst_marker_mm, round_func= math.floor):
        """
        given a wanted marker size, return the recommended data

        when we want to scale the png marker file, the scaler factor should be an interger,
        otherwise the image after scaling will be fuzzy, this reduces the poisitioning accuracy

        so the result will be rounded to get a recommended value

        for aprital 36h11, marker size = 8x8 pix
        png files downloaded from https://github.com/AprilRobotics/apriltag-imgs has a size of 10x10 pix
        => blank border = 1pix width

        :param dst_marker_mm: destination marker size in mm
        :type dst_marker_mm: float
        :param round_func: function used to round the calculated value, defaults to math.floor
        :type round_func: function, optional
        :return: scaled marker size in mm, scaling factor
        :rtype: float, int
        """
        dst_marker_pix = self._mm_2_pix(dst_marker_mm)
        scale_factor = round_func(dst_marker_pix/8)
        marker_size = self._pix_2_mm(scale_factor*8)
        return marker_size, scale_factor
    
    def _mm_2_pix(self, mm):
        return self.dpi*mm/self.inch_mm

    def _pix_2_mm(self, pix):
        return pix*self.inch_mm/self.dpi

    def scale_factor_2_marker_size(self, scale_factor):
        png_pix = scale_factor/100*10
        marker_pix = png_pix/10*8
        return self._pix_2_mm(marker_pix)
    
    def png_pix_2_marker_size(self, png_pix):
        scale_factor = png_pix/10*100
        return self.scale_factor_2_marker_size(scale_factor)

    def scale_command(self, scale_factor, file_path):
        assert os.path.isfile(file_path)
        base = os.path.splitext(file_path)[0]
        extension = os.path.splitext(file_path)[1]
        new_size = self._pix_2_mm(scale_factor*8)
        new_path = f"{base}_{scale_factor*100}%_{new_size:.2f}mm{extension}"
        command = f"convert {file_path} -scale {scale_factor*100}% {new_path}"
        return command

if __name__ == "__main__":
    scaler = ApriltagScaler()
    # print(scaler.scale_factor_2_marker_size(600))
    # print(scaler.png_pix_2_marker_size(60))
    # print(scaler.recommended_value(30))
    print(scaler.scale_command(10, "D:/tag36_11_00000.png"))