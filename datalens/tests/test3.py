import os

path = r"hggf\2.ext"

result = os.path.splitext(os.path.basename(path))[0]

print(result)