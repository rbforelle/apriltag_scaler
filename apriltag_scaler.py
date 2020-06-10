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

    def recommended_value(self, dst_marker_mm, round_func = math.floor):
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
        png_pix = scale_factor*10
        marker_pix = png_pix/10*8
        return self._pix_2_mm(marker_pix)
    
    def png_pix_2_marker_size(self, png_pix):
        scale_factor = png_pix/10
        return self.scale_factor_2_marker_size(scale_factor)

    def scale_command(self, scale_factor, file_path, dst_dir=None, with_label=False):
        """
        return command to scale the png file
        :param scale_factor:
        :type scale_factor: int
        :param file_path: path of the file to scale
        :type file_path: string
        :param dst_dir: output dir, defaults to None
        :type dst_dir: string, optional
        :param with_label: if true, set label for the image, optional
        :type with_label: bool
        :return: scale commands
        :rtype: list[string]
        """
        # check file
        assert os.path.isfile(file_path), file_path
        basedir = os.path.dirname(file_path)
        if dst_dir == None:  # if dst_dir not defined, use the same dir as output
            dst_dir = basedir
        else:
            assert os.path.isdir(dst_dir), dst_dir
        # split file name    
        basename = os.path.basename(file_path)
        file_name = os.path.splitext(basename)[0]
        extension = os.path.splitext(basename)[1]
        # calculate new file size based on scale factor
        new_size = self._pix_2_mm(scale_factor*8)
        new_path = f"{os.path.join(dst_dir, file_name)}_{scale_factor*100}%_{new_size:.2f}mm{extension}"
        # to use this command, make sure that ImageMagick has already been installed
        # scale and add 1mm border
        command = f"convert -scale {scale_factor*100}% -border 4 {file_path} {new_path}"
        # add label, this will be printed when all images combined with montage
        command2 = f"convert -label \'{file_name}\\n{scale_factor*8} pix\\n{new_size:.2f} mm\' {new_path} {new_path}"
        return [command, command2]
    
    def convert(self, src_dir, dst_dir=None, scale_factor = None, marker_size = None):
        # check input data
        assert os.path.isdir(src_dir), src_dir
        if dst_dir is not None:
            assert os.path.isdir(dst_dir)
        if not (scale_factor or marker_size):
            raise ValueError

        # calculate recommended scaling factor if no scale_factor defined
        if scale_factor is None and marker_size is not None:
            real_marker_size, scale_factor = self.recommended_value(marker_size)

        # convert all files in the directory
        for file_name in os.listdir(src_dir):
            basedir = os.path.dirname(src_dir)
            file_path = os.path.join(basedir, file_name)
            if not os.path.isfile(file_path):
                continue
            commands = self.scale_command(scale_factor, file_path, dst_dir, with_label=True)
            for command in commands:
                print(command)
                os.system(command)
        
        # montage * -geometry +12+12 output.png


if __name__ == "__main__":
    scaler = ApriltagScaler()
    print(scaler.scale_factor_2_marker_size(10))
    print(scaler.png_pix_2_marker_size(60))
    print(scaler.recommended_value(30))
    print(scaler.scale_command(10, "/mnt/d/test_dir/tag36_11_00000.png"))
    scaler.convert("/mnt/d/test_dir/", dst_dir = "/mnt/d/test_dir/converted/", marker_size = 40)