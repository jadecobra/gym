import io
import wsgiref.util

filelike = io.StringIO('This is an exmaple file-like object'*10)
wrapper = wsgiref.util.FileWrapper(filelike, blksize=5)

for chunk in wrapper:
    print(chunk)