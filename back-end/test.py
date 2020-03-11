pth = "addasd.sadasd.jpg"

arr = pth.split('.')
new_filename = '{}.{}'.format(uuid.uuid4, pth.split('.')[-1])
print(new_filename)
ext = arr[-1]
print(ext)