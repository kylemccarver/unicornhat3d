import time

import glm
import unicornhathd

class Primitive(object):
    def __init__(self, vertices):
        self.vertices = vertices

w, h = unicornhathd.get_shape()

viewport = {
    "x": 0,
    "y": 0,
    "w": w,
    "h": h,
    "n": 0.1,
    "f": 100
}



M = glm.mat4(1)

V = glm.lookAt(glm.vec3(0, 0, 6), 
               glm.vec3(0, 0, 0), 
               glm.vec3(0, 1, 0))

P = glm.perspective(glm.radians(45), viewport["w"]/viewport["h"], viewport["n"], viewport["f"])

def main():
    global M, V, P, viewport

    verts = [
        glm.vec4(-1, 1, 1, 1),
        glm.vec4(-1, -1, 1, 1),
        glm.vec4(1, -1, 1, 1),

        glm.vec4(1, 1, 1, 1),
        glm.vec4(-1, 1, 1, 1),
        glm.vec4(1, -1, 1, 1)
    ]

    pipeline(verts)

    try:
        while True:
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

    except KeyboardInterrupt:
        unicornhathd.off()


def pipeline(vertices):
    vertex_shader_out = vertex_shader(vertices)
    vertex_post_processing_out = vertex_post_processing(vertex_shader_out)
    primitives = primitive_assembly(vertex_post_processing_out)
    for p in primitives:
        print(p.vertices)


def vertex_shader(vertices):
    out = []
    for v in vertices:
        out.append(P * V * M * v)
    return out


def vertex_post_processing(vertices):
    out = []
    for v in vertices:
        ndc = v.xyz / v.w

        screen = glm.vec3(0)
        screen.x = ((viewport["w"] * 0.5) * ndc.x) + ((viewport["w"] * 0.5) + viewport["x"])
        screen.y = ((viewport["h"] * 0.5) * ndc.y) + ((viewport["h"] * 0.5) + viewport["y"])
        screen.z = (((viewport["f"] - viewport["n"]) * 0.5) * ndc.z) + ((viewport["f"] + viewport["n"]) * 0.5)
        out.append(screen)
    return out


def primitive_assembly(vertices):
    return [Primitive(vertices[i:i+3]) for i in range(0, len(vertices), 3)]


def rasterize():
    pass


def fragment_shader():
    pass


if __name__ == "__main__":
    main()
