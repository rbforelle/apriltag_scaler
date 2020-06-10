# Apriltag Scaler

This programm can help to calculate scale factor and convert apriltag to the size we want automatically. It's compatible with all types of apriltags and also can be used for other similar tags.

![](https://raw.githubusercontent.com/rbforelle/apriltag_scaler/master/demo/output_tag36h11.png)

## Calculation for scaling

The original apriltags can be downloaded from <https://github.com/AprilRobotics/apriltag-imgs>

These tags should be scaled for using. What's important is that, in the config file of apriltag we have to define the size of tags in mm. And this size is very important for the positioning accuracy.

But before printing, we only know the size in pixels. For exmaple, a 36h11 tag scaled 1000%, png file size = 100x100 pix. With measurement we find that the marker size is about 28mm, but is it really 28mm?

Actually, it's 28.2222222mm.

Calculation:

- 36h11 tag
  - png size = 10x10 pix
  - marker size = 8x8 pix
- scaled 1000%
  - png size = 100x100 pix
  - marker size = 80x80 pix
- printer DPI = 72
  - length[mm] = pixel * 1Inch[25.4mm] / dpi

**=> length = 28.22222222 mm**

Otherweise, what's more common in usage is that, we need a `50mm` tag, how should I scale and print it? Attention that the scale factor should be an integer. A `scale factor of 17` should be used to generate tags with `size of 47.98mm`.

All these can be done automatically with this programm.

## Install

In order to use the convert function, ImageMagick should be installed

```bash
sudo apt install imagemagick
```

## Usage

For apriltag 36h11, original tag size: 8x8 pixels, png size: 10x10 pixels  
For apriltag 16h9, original tag size: 6x6 pixels, png size: 8x8 pixels

```python
# apriltag 36h11
scaler_36h11 = ApriltagScaler(printer_dpi=72, origin_tag_size_pix=8, origin_img_size_pix=10)

# apriltag 16h5
scaler_16h5 = ApriltagScaler(printer_dpi=72, origin_tag_size_pix=6, origin_img_size_pix=8)
```

### scale factor => maker size[mm]

10 = 1000%

```python
scaler_36h11.scale_factor_2_marker_size(10)
=> 28.222222222222222

scaler_16h5.scale_factor_2_marker_size(10)
=> 21.166666666666668
```

### png size[pix] => marker size[mm]

convert size of the scaled png file in pixel to size of the marker in mm

```python
scaler_36h11.png_pix_2_marker_size(60)
=> 16.93333333333333

scaler_16h5.png_pix_2_marker_size(60)
=> 15.875
```

### Get recommended scale factor

input is size of the marker that we want(not always can be achieved), here 30mm

```python
marker_size, scale_factor = scaler_36h11.recommended_value(30, round_func = math.floor)
=> marker_size: 28.22222222
=> scale_factor: 10

marker_size, scale_factor = scaler_16h5.recommended_value(30, round_func = math.floor)
=> marker_size: 29.633333333333333
=> scale_factor: 14
```

### Scale and print all tags in directory

`convert`, `montage` in ImageMagick can be used to scale tag images and put them together for printing.

I have combined these tools with my programm together

#### Scale 36h9 tags

```python
scaler_36h9.convert("demo/tag36h9/origin/", dst_dir = "demo/tag36h9/scaled/", tag_size = 40)
```

### Put them together manuelly

```bash
montage demo/tag36h11/scaled/* -geometry +12+12 demo/output_tag36h11.png
```

Print it with 72 DPI, set 39.51mm in the config file, that's all!
