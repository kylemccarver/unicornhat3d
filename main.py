import time

import glm
import unicornhathd

w, h = unicornhathd.get_shape()

viewport = {
    "x": 0,
    "y": 0,
    "w": w,
    "h": h,
    "n": 0.1,
    "f": 100
}

verts = [
    glm.vec4(-1, 1, 0, 1),
    glm.vec4(-1, -1, 0, 1),
    glm.vec4(1, -1, 0, 1)
]

M = glm.mat4(1)

V = glm.lookAt(glm.vec3(0, 0, 6), 
               glm.vec3(0, 0, 0), 
               glm.vec3(0, 1, 0))

P = glm.perspective(glm.radians(45), viewport["w"]/viewport["h"], viewport["n"], viewport["f"])

for v in verts:
    mvc = P * V * M * v
    ndc = mvc.xyz / mvc.w

    screen = glm.vec3(0)
    screen.x = ((viewport["w"] * 0.5) * ndc.x) + ((viewport["w"] * 0.5) + viewport["x"])
    screen.y = ((viewport["h"] * 0.5) * ndc.y) + ((viewport["h"] * 0.5) + viewport["y"])
    screen.z = (((viewport["f"] - viewport["n"]) * 0.5) * ndc.z) + ((viewport["f"] + viewport["n"]) * 0.5)
    
    unicornhathd.set_pixel(screen.x, screen.y, 255, 0, 0)

unicornhathd.brightness(0.2)
unicornhathd.rotation(90)
unicornhathd.show()
time.sleep(2)
unicornhathd.off()
