import sys
import time

import glm
import unicornhathd


class Primitive(object):
    def __init__(self, vertices):
        self.vertices = vertices


class Fragment(object):
    def __init__(self):
        self.screen = glm.vec3(0)
        self.depth = sys.maxsize


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
                mvp = P * V * M * v

                screen = clip_to_screen_space(mvp)
               
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
    fragments = rasterize(primitives)


def vertex_shader(vertices):
    return vertices


def vertex_post_processing(vertices):
    out = []
    for v in vertices:
        out.append(P * V * M * v)
    return out


def primitive_assembly(vertices):
    return [Primitive(vertices[i:i+3]) for i in range(0, len(vertices), 3)]


def rasterize(primitives):
    for primitive in primitives:
        screen_vertices = [clip_to_screen_space(v) for v in primitive.vertices]
        min_x = min(screen_vertices, key=lambda v: v.x).x
        min_y = min(screen_vertices, key=lambda v: v.y).y
        max_x = max(screen_vertices, key=lambda v: v.x).x
        max_y = max(screen_vertices, key=lambda v: v.y).y

        for x in min_x:
            for y in min_y:
                pass


def fragment_shader():
    pass


def clip_to_screen_space(vertex):
    ndc = vertex.xyz / vertex.w
    screen = glm.vec3(0)
    screen.x = ((viewport["w"] * 0.5) * ndc.x) + ((viewport["w"] * 0.5) + viewport["x"])
    screen.y = ((viewport["h"] * 0.5) * ndc.y) + ((viewport["h"] * 0.5) + viewport["y"])
    screen.z = (((viewport["f"] - viewport["n"]) * 0.5) * ndc.z) + ((viewport["f"] + viewport["n"]) * 0.5)
    return screen


def barycentric(v1, v2, v3, p):
    A_t = glm.length(glm.cross((v2 - v1), (v3 - v1))) * 0.5
    A_1 = glm.length(glm.cross((v2 - p), (v3 - p))) * 0.5
    A_2 = glm.length(glm.cross((p - v1), (v3 - v1))) * 0.5
    A_3 = glm.length(glm.cross((v2 - v1), (p - v1))) * 0.5

    a = A_1 / A_t
    b = A_2 / A_t
    g = A_3 / A_t

    return a, b, g


if __name__ == "__main__":
    main()
