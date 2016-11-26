from PIL import Image
import sys
import subprocess
import magic

def main(paths):
  m=magic.open(magic.MAGIC_MIME)
  m.load()

  for path in paths:
    mime_type = m.file(path)
    if mime_type.startswith('image/jpeg'):
      sys.stdout.write('magic,succeeded,' + path + ',' + mime_type + '\n')
    else:
      sys.stdout.write('magic,failed,' + path + ',' + mime_type + '\n')

    try:
      im = Image.open(path)
      im.verify()
      im = Image.open(path)
      im.load()
      sys.stdout.write('PIL,succeeded,' + path + ',\n')
    except Exception as e:
      sys.stdout.write('PIL,failed,' + path + str(e).replace('\n', '\\n') + '\n')

    try:
      out = subprocess.check_output('jpeginfo -c "' + path + '"', stderr=subprocess.STDOUT, shell=True)
      sys.stdout.write('jpeginfo,succeeded,' + path + ',' + out.replace('\n', '\\n') + '\n')
    except subprocess.CalledProcessError as e:
      sys.stdout.write('jpeginfo,failed,' + path + ',' + e.output.replace('\n', '\\n') + '\n')

    try:
      out = subprocess.check_output('identify -verbose "' + path + '"', stderr=subprocess.STDOUT, shell=True)
      sys.stdout.write('identify,succeeded,' + path + ',' + out.replace('\n', '\\n') + '\n')
    except subprocess.CalledProcessError as e:
      sys.stdout.write('identify,failed,' + path + ',', + e.output.replace('\n', '\\n') + '\n')




if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
