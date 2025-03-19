from utils01 import Point

# empty class
class point3d(Point):
    z = 0

    def __str__(self):
        return '{} {} {}'.format(self.x, self.y, self.z)

ppoint = point3d()

print(ppoint)