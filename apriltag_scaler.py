import math
import os


class ApriltagScaler(object):
    def __init__(self, printer_dpi=72, origin_tag_size_pix = 8, origin_img_size_pix = 10):
        self.dpi = printer_dpi  # normal printer default DPI = 72
        self.origin_tag_size_pix = origin_tag_size_pix
        self.origin_img_size_pix = origin_img_size_pix
        self.inch_mm = 25.4  # 1inch = 25.4mm

    def recommended_value(self, dst_tag_mm, round_func = math.floor):
        """
        given a wanted tag size, return the recommended data

        when we try to scale the png tag file, the scale factor should be an interger,
        otherwise the image gets blurry after scaling, this reduces the poisitioning accuracy

        so the calculated scale factor will be rounded to get a recommended value

        :param dst_tag_mm: destination tag size in mm
        :type dst_tag_mm: float
        :param round_func: function used to round the calculated value, defaults to math.floor
        :type round_func: function, optional
        :return: scaled tag size in mm, scale factor
        :rtype: float, int
        """
        dst_tag_pix = self.mm_2_pix(dst_tag_mm)
        scale_factor = round_func(dst_tag_pix/self.origin_tag_size_pix)
        tag_size = self.pix_2_mm(scale_factor*self.origin_tag_size_pix)
        return tag_size, scale_factor
    
    def mm_2_pix(self, mm):
        return self.dpi*mm/self.inch_mm

    def pix_2_mm(self, pix):
        return pix*self.inch_mm/self.dpi

    def scale_factor_2_tag_size(self, scale_factor):
        png_pix = scale_factor*self.origin_img_size_pix
        tag_pix = png_pix/self.origin_img_size_pix*self.origin_tag_size_pix
        return self.pix_2_mm(tag_pix)
    
    def png_pix_2_tag_size(self, png_pix):
        scale_factor = png_pix/self.origin_img_size_pix
        return self.scale_factor_2_tag_size(scale_factor)

    def scale_command(self, scale_factor, file_path, dst_dir=None, with_label=False, border_width_pix=4):
        """
        return command to scale the png file using convert from imagemagick
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
        :param border_width: add border outside of the tag, default to 4 pixels => 1mm
        :type border_width: int, optional
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
        new_size = self.pix_2_mm(scale_factor*self.origin_tag_size_pix)
        new_path = f"{os.path.join(dst_dir, file_name)}_{scale_factor*100}%_{new_size:.2f}mm{extension}"

        scaled_img_size = scale_factor*self.origin_img_size_pix + border_width_pix*2

        command = f"convert -scale {scale_factor*100}% -border {border_width_pix} {file_path} {new_path}"
        # add label, this will be printed when all images combined with montage
        command2 = f"convert -label \'{file_name}\\nscaled_img_size: {scaled_img_size} pix\\ntag_size: {new_size:.2f} mm\' {new_path} {new_path}"
        return [command, command2]
    
    def convert(self, src_dir, dst_dir=None, scale_factor = None, tag_size = None):
        """
        scale all files in the src_dir, output to dst_dir
        :param src_dir: dst directory with tag png files
        :type src_dir: string
        :param dst_dir: dst directory, defaults to None
        :type dst_dir: string, optional
        :param scale_factor: factor for scaling, defaults to None
        :type scale_factor: int, optional
        :param tag_size: tag size you want, defaults to None
        :type tag_size: float, optional
        :raises ValueError:
        """
        # check input data
        assert os.path.isdir(src_dir), src_dir
        if dst_dir is not None:
            assert os.path.isdir(dst_dir)
        if not (scale_factor or tag_size):
            raise ValueError

        # calculate recommended scaling factor if no scale_factor defined
        if scale_factor is None and tag_size is not None:
            real_tag_size, scale_factor = self.recommended_value(tag_size)

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
        

if __name__ == "__main__":
    scaler_36h11 = ApriltagScaler(printer_dpi=72, origin_tag_size_pix=8, origin_img_size_pix=10)
    print(scaler_36h11.scale_factor_2_tag_size(10))
    print(scaler_36h11.png_pix_2_tag_size(60))
    print(scaler_36h11.recommended_value(30))
    print(scaler_36h11.scale_command(10, "demo/tag36h11/origin/tag36_11_00000.png"))
    scaler_36h11.convert("demo/tag36h11/origin/", dst_dir = "demo/tag36h11/scaled/", tag_size = 40)

    os.system('montage demo/tag36h11/scaled/* -geometry +12+12 demo/output_tag36h11.png')
    
    '''
    scaler_16h5 = ApriltagScaler(printer_dpi=72, origin_tag_size_pix=6, origin_img_size_pix=8)
    print(scaler_16h5.scale_factor_2_tag_size(10))
    print(scaler_16h5.png_pix_2_tag_size(60))
    print(scaler_16h5.recommended_value(30))
    print(scaler_16h5.scale_command(10, "demo/tag16h5/origin/tag16_05_00000.png"))
    scaler_16h5.convert("demo/tag16h5/origin/", dst_dir = "demo/tag16h5/scaled/", tag_size = 40)

    os.system('montage demo/tag16h5/scaled/* -geometry +12+12 demo/output_tag16h5.png')
    '''