import ctypes

class Point:

    def __init__(self, params):
        if hasattr(params, "__iter__"):
            if "x" in params and type(params["x"]) is int:
                self.x = ctypes.c_int(params["x"])
            if "y" in params and type(params["y"]) is int:
                self.y = ctypes.c_int(params["y"])
            if "size" in params and type(params["size"]) is int:
                self.size = ctypes.c_int(params["size"])
            if "cie_x" in params and type(params["cie_x"]) is (int, float):
                self.cie_x = ctypes.c_double(float(params["cie_x"]))
            if "cie_y" in params and type(params["cie_y"]) is (int, float):
                self.cie_y = ctypes.c_double(float(params["cie_y"]))
            if "cie_z" in params and type(params["cie_z"]) is (int, float):
                self.cie_z = ctypes.c_double(float(params["cie_z"]))

    def is_valid_point_info(self):
        return hasattr(self, "x") and hasattr(self, "y") and hasattr(self, "size")

    def is_valid_colors(self):
        return hasattr(self, "cie_x") and hasattr(self, "cie_y") and hasattr(self, "cie_z")

    def is_valid(self):
        return self.is_valid_point_info() or self.is_valid_colors()

    def to_point_info_array(self):
        if self.is_valid_point_info():
            IntArray3 = ctypes.c_int * 3 
            arr = [self.x, self.y, self.size]  
            return IntArray3(*arr)
        return ctypes.c_void_p(None)

    def to_colors_array(self):
        if self.is_valid_colors():
            DoubleArray3 = ctypes.c_double * 3 
            arr = [self.cie_x, self.cie_y, self.cie_z]  
            return DoubleArray3(*arr)
        return ctypes.c_void_p(None)

def main():
    p0 = Point({"x":0,"y":0,"size":20})
    p1 = Point({"x":0,"y":0,"size":20})

    print(p0.is_valid())
    arr = p1.to_point_info_array()
    print(arr[2])
    arr = p1.to_colors_array()
    print(arr)

    dict1 = {"a":1, "b":2}
    dict2 = {"c":3, "d":4}
    dict1.update(dict2)
    print(dict1)

    keys = ['a', 'b', 'c']
    values = [ctypes.c_double(0), ctypes.c_double(1), ctypes.c_double(2)]
    dict3 = dict(zip(keys, map(lambda x: x.value, values)))
    print(dict3)

main()