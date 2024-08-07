**Copyright (c) 2023 tristanGIANDO**

*Permission is hereby granted, free of charge, to any person obtaining a copy*
*of this software and associated documentation files (the "Software"), to deal*
*in the Software without restriction, including without limitation the rights*
*to use, copy, modify, merge, publish, distribute, sublicense, and/or sell*
*copies of the Software, and to permit persons to whom the Software is*
*furnished to do so, subject to the following conditions:*

*The above copyright notice and this permission notice shall be included in all*
*copies or substantial portions of the Software.*

*THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR*
*IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,*
*FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE*
*AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER*
*LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,*
*OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE*
*SOFTWARE.*

<h1 align="center">
    EXIF_gallery
</h1>

<h3 align="center">
    A tool designed to give photographers an overview of their photos.
</h3>

[![LinkedIn](https://img.shields.io/badge/LinkedIn_Demo-%230077B5.svg?logo=linkedin&logoColor=white)](https://www.linkedin.com/posts/tristan-giandoriggio_exifabrgallery-pyqt5-mysql-activity-7120075997315485698-LBzX?utm_source=share&utm_medium=member_desktop)

## Introduction

I do some astrophotography, and it's a field where technique is very important.

However, I can never seem to remember all the settings...

So, I created this tool, EXIF_gallery, that allows me to store, analyze, and compare the data from my photos.

Built in PyQt5, I was able to explore SQL and HTML, as well as some more mathematical libraries.

Special thanks to Manon Seve for the logo and to Gabriel Akpo-Allavo, the best of spiritual guides.

It's not shown in the demo, but there are user-specific features such as inputting their own data or adding comments.

The goal in the future is to adapt EXIF_gallery for other types of photography.


**Overview**
![overview](https://raw.githubusercontent.com/tristanGIANDO/EXIF_gallery/main/resources/_overview.png)

**Statistics**
![stats](https://raw.githubusercontent.com/tristanGIANDO/EXIF_gallery/main/resources/_stats.png)

**Portfolio**
![portfolio](https://raw.githubusercontent.com/tristanGIANDO/EXIF_gallery/main/resources/_portfolio.png)

## FEATURES
Each photo can store more data than a conventional image:
* EXIFs
* comments
* processing versions
* location of the shot

### Features for astrophoto
* number of shots + exposure times
* total exposure time calculated automatically
* Bortle level

#### Example
|ID|Image|Subject|Description|Author|Camera|Focal length|Mount|Aperture|ISO|NB lights|Exposure time|Total time|Place|Sky darkness|Moon Illumination|Processed with|Brut|Versions|Date|Comment|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|0|-|M31|some test|me|Canon70D|135mm|SA2i|2.8|1600|50|120|-|here|2|35%|Siril/Photoshop|-|-|24/12/23||

---

## INSTALL

The script is written in **Python 3**.

From a console, run :
```
pip3 install PyQt5 pillow mysql-connector-python scipy cartopy geopy matplotlib
```

## USAGE

Run `EXIF_gallery.exe` or `main.py`.

## API DOCUMENTATION

### INSTRUCTIONS FOR USE
```py
# create database
db = Database()

# add image
data = {
  "id" : 012345678
  "name" : "image_name"
  "path" : "path/file.png"
}
db.add(data)

# update image
db.update("name", 012345678, "new_name_value")

# get images
db.get_rows()

```

<h2 align="center" style="margin:1em;">
    <img src="EXIF_gallery/ui/icons/logo.png"
         alt="EXIF_gallery"></a>
</h2>
