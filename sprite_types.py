import Circle
import Rect
import Img

# try..except saves from AttributeError during import
# => means import, -> means running line within that file
# why :  sprite_types => Circle => sprite_types -> Circle.Circle
# this raises error, as Circle class not yet defined in Circle
# but when __main__ runs, after all successful imports, Circle.Circle is defined

try:
    Circle = Circle.Circle
except:
    pass

try:
    Rect = Rect.Rect
except:
    pass

try:
    Img = Img.Img
except:
    pass
