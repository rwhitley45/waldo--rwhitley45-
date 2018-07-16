# waldo--rwhitley45-
Repository for Waldo coding exercise

This repository contains the python3 program ```iscropped.py``` for the waldo coding exercise. The program uses the external
image processing library OpenCV which can be installed via pip with the following command:

```bash
pip3 install opencv-python
```

Example usage:
```bash
python3 iscropped.py ./images/image1.ext ./images/image2.ext 
```

### Assumptions:
- The cropped image is a direct crop from the larger image.
- Cropped image is not repeated throughout the original image. If so, only the first occurance is
returned.
- I tested the program on three image formats (Tiff, JPEG, and PNG). If more lossy image formats are
required, I will need to include their extension within the program.
 
### Lossy Image Format:
JPEG's lossy format provided some challenge to this assignment, as I noticed pixel values do not remain consistent
on the resulting cropped image. To account for this, I used a standard deviation for pixels to try and account 
for the loss in quality. However, I don't belive this solution is 100% foolproof. 
