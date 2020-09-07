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


eps = 0.00001

unicornhathd.brightness(0.2)
unicornhathd.rotation(90)

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


    try:
        t = time.time()
        while True:
            unicornhathd.clear()
            #dt = time.time() - t
            #t = time.time()

            #V = glm.rotate(V, 0.05, glm.vec3(0, 0, 1))
            pipeline(verts)
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
    return [P * V * M * v for v in vertices]


def primitive_assembly(vertices):
    return [Primitive(vertices[i:i+3]) for i in range(0, len(vertices), 3)]


def rasterize(primitives):
    out = []
    for primitive in primitives:
        screen_vertices = [clip_to_screen_space(v) for v in primitive.vertices]
        min_x = round(min(screen_vertices, key=lambda v: v.x).x)
        min_y = round(min(screen_vertices, key=lambda v: v.y).y)
        max_x = round(max(screen_vertices, key=lambda v: v.x).x)
        max_y = round(max(screen_vertices, key=lambda v: v.y).y)

        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                centroid = glm.vec3(x + 0.5, y + 0.5, 0)
                v1 = glm.vec3(screen_vertices[0].xy, 0)
                v2 = glm.vec3(screen_vertices[1].xy, 0)
                v3 = glm.vec3(screen_vertices[2].xy, 0)
                a, b, g = barycentric(v1, v2, v3, centroid)
                interp = a + b + g
                if interp >= 1 - eps and interp <= 1 + eps:
                    unicornhathd.set_pixel(x, y, 255 * a, 255 * b, 255 * g)


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
