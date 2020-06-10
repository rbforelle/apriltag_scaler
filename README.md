# Apriltag Scaler

This programm can help to calculate scale factor and convert apriltag to the size we want automatically.

![](https://raw.githubusercontent.com/rbforelle/apriltag_scaler/master/demo/output/output.png)

## Calculation for scaling

The original apriltags can be downloaded from <https://github.com/AprilRobotics/apriltag-imgs>

These tags should be scaled for using. What's important is that, in the config file of apriltag we have to define the size of tags in mm. And this size is very important for the positioning accuracy. 

But before printing, we only know the size in pixels. For exmaple, a 36h11 tag scaled 1000%, png file size = 100x100 pix. With measurement we find that the marker size is about 28mm, but is it really 28mm? 

Actually, it's 28.2222222mm.

Calculation:

- 36h11 tag, 
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

```python
scaler = ApritagScaler()
```

### scale factor => maker size[mm]

10 = 1000%

```python
print(scaler.scale_factor_2_marker_size(10))
```

### png size[pix] => marker size[mm]

convert size of the scaled png file in pixel to size of the marker in mm

```python
print(scaler.png_pix_2_marker_size(60)
```

### Get recommended scale factor

input is size of the marker that we want. (not always can be achieved)

```python
marker_size, scale_factor = scaler.recommended_value(30, round_func = math.floor)

=> marker_size: 28.22222222
=> scale_factor: 10
```

### Scale and print all tags in directory

`convert`, `montage` in ImageMagick can be used to scale tag images and put them together for printing.

I have combined these tools with my programm together

#### Scale tags

```python
scaler.convert("~/tags_to_convert/", scale_factor = 10)
scaler.convert("~/tags_to_convert/", dst_dir = "~/tags_converted/", marker_size = 30)
```

### Put them together manuelly

```bash
cd ~/tags/converted/
montage * -geometry +12+12 output.png
```

Print it with 72 DPI, set 28.22mm in the config file, that's all!
