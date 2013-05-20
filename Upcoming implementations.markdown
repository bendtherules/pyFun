Upcoming in pyFun
-----------------
***

1. Circle class ( __Doing__ ) and Angled rect class (subclassed from rect)
2. Image module (similar to GM sprites)
    + Make a custom image object which should support
        + Sprites and shapes, with good query hooks
        + Easy shape drawing functions, may look at codes in turtle module and other similar ones.
        + Animation (no. of frame, speed of frame, start(), pause(),resume(),stop())
        + Origin
        + Strips
        + Masking
        + Collision query
        + Cursor sprites
    + Support backgrounds somehow and provide easy-to-use update-only-required-part-of-screen functions
3. Instance query module
    + Support query about other classes and instances easily.
    + Let use coding for other instances from another instance. Similar to with(other){do_it;}
    + Provide interaction methods based on image module like
         + Collision detection (between one object and another object|point|image)
         + Outside room
         + Is mouse click on this object?
4. Timer (alarm) module
    * Support arbitrary number of timers and also tracking them with id.
5. Add other keyboard and mouse module extras like GM
6. Add events mentioned in GM "Other" event dropdown.
7. Surfaces
8. Particles
9. Sound module
10. Path module
11. Timeline module
12. Highscore api
