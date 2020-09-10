import sys
import time

import glm
import unicornhathd


class Viewport(object):
    def __init__(self, x, y, w, h, n, f):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.n = n
        self.f = f


class Primitive(object):
    def __init__(self, vertices):
        self.vertices = vertices


class Fragment(object):
    def __init__(self):
        self.screen = glm.vec3(0)
        self.depth = sys.maxsize


unicornhathd.brightness(0.2)
unicornhathd.rotation(90)

def main():
    global M, V, P, view

    verts = [
        glm.vec4(-1, 1, 1, 1),
        glm.vec4(-1, -1, 1, 1),
        glm.vec4(1, -1, 1, 1),

        glm.vec4(1, 1, 1, 1),
        glm.vec4(-1, 1, 1, 1),
        glm.vec4(1, -1, 1, 1)
    ]

    w, h = unicornhathd.get_shape()

    view = Viewport(0, 0, w, h, 0.1, 100)

    M = glm.mat4(1)

    V = glm.lookAt(glm.vec3(0, 0, 6), 
                   glm.vec3(0, 0, 0), 
                   glm.vec3(0, 1, 0))

    P = glm.perspective(glm.radians(45), view.w / view.h, view.n, view.f)

    try:
        t = time.time()
        #while True:
            #unicornhathd.clear()
            #dt = time.time() - t
            #t = time.time()

            #V = glm.rotate(V, 0.05, glm.vec3(0, 0, 1))
        pipeline(verts)
            #unicornhathd.show()

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

        v0 = screen_vertices[0]
        v1 = screen_vertices[1]
        v2 = screen_vertices[2]
        area = edge_function(v0, v1, v2)

        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                centroid = glm.vec3(x + 0.5, y + 0.5, 0)

                w0 = edge_function(v1, v2, centroid)
                w1 = edge_function(v2, v0, centroid)
                w2 = edge_function(v0, v1, centroid)

                bias0 = 0 if top_left_test(v1, v2) else -1
                bias1 = 0 if top_left_test(v2, v0) else -1
                bias2 = 0 if top_left_test(v0, v1) else -1

                if w0 + bias0 >= 0 and w1 + bias1 >= 0 and w2 + bias2 >= 0:
                    # TODO: perspective-correct interpolation
                    a, b, g = w0 / area, w1 / area, w2 / area
                    #unicornhathd.set_pixel(x, y, 255 * a, 255 * b, 255 * g)


def fragment_shader():
    pass


def clip_to_screen_space(vertex):
    ndc = vertex.xyz / vertex.w
    screen = glm.vec3(0)
    screen.x = ((view.w * 0.5) * ndc.x) + ((view.w * 0.5) + view.x)
    screen.y = ((view.h * 0.5) * ndc.y) + ((view.h * 0.5) + view.y)
    screen.z = (((view.f - view.n) * 0.5) * ndc.z) + ((view.f + view.n) * 0.5)
    return screen


def edge_function(a, b, p):
    return (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x);


def top_left_test(p, q):
    e = q - p
    return True if e.x < 0 and e.y == 0 or e.y < 0 else False


if __name__ == "__main__":
    main()
