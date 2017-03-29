import os

print __file__
path_ = os.path.abspath(__file__)
# path_ = os.path.relpath(__file__)
print path_
print os.path.dirname(path_)
