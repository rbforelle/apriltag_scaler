import math


class ApriltagScaler(object):
    def __init__(self, printer_dpi=72):
        self.dpi = printer_dpi
        self.inch_mm = 25.4
        self.marker_mm = None
        self.marker_pix = None
        self.png_mm = None
        self.png_pix = None

    def recommended_value(self, dst_marker_mm, round_func= math.floor):
        dst_marker_pix = self._mm_2_pix(dst_marker_mm)
        dst_png_pix = dst_marker_pix/8*10
        # png_pix should be an integer multiple of 10
        # to prevent problem by scale
        png_pix = round_func(dst_png_pix/10)*10  
        return f"marker_size: {self._pix_2_mm(png_pix/10*8)}mm\npng_size: {png_pix}pix, scale_factor: {png_pix/10*100}%"
    
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

if __name__ == "__main__":
    scaler = ApriltagScaler()
    # print(scaler.scale_factor_2_marker_size(600))
    # print(scaler.png_pix_2_marker_size(60))
    print(scaler.recommended_value(30))