from __future__ import print_function
from PIL import Image
import sys
import os
import os.path
import errno
from signal import SIGINT, SIGTERM
from pysigset import suspended_signals


def resize(path, outpath):
  with suspended_signals(SIGINT, SIGTERM):
    try:
      fh = os.open(outpath, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0666)
    except OSError as e:
      if e.errno == errno.EEXIST:
        return
      else:
        raise

    try:
      with os.fdopen(fh, 'w') as out:
        img = Image.open(path)
        box = (299, 299)

        #calculate the cropping box and get the cropped part
        x1 = y1 = 0
        x2, y2 = img.size
        wRatio = 1.0 * x2/box[0]
        hRatio = 1.0 * y2/box[1]
        if hRatio > wRatio:
          y1 = int(y2/2-box[1]*wRatio/2)
          y2 = int(y2/2+box[1]*wRatio/2)
        else:
          x1 = int(x2/2-box[0]*hRatio/2)
          x2 = int(x2/2+box[0]*hRatio/2)
        img = img.crop((x1,y1,x2,y2))

        img.thumbnail(box, Image.LANCZOS)

        # This is necessary when saving to PNG, as it doesn't support CMYK
        if img.mode == "CMYK":
          img = img.convert("RGB")
        
        img.save(out, "PNG", optimize=True)
        # TensorFlow doesn't support webp yet, so we'll go with the larger png
        #img.save(out, "WebP", lossless=True)

    except Exception as e:
      sys.stdout.write('failed:' + path + ',' + str(e).replace('\n', '\\n') + '\n')
      try:
        os.remove(outpath)
      except OSError:
        pass


def main(paths, outdir):
  for path in paths:
    resize(path, outdir + '/' + path.split('/')[-1][:-4] + '.png')


if __name__ == '__main__':
  if sys.argv[1] == '--outdir':
    outdir = sys.argv[2]
    sys.exit(main(sys.argv[3:], outdir))
  else:
    sys.exit(main(sys.argv[1:], '.'))
