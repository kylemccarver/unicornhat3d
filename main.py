import math
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


class VertexArrayObject(object):
    def __init__(self):
        self.attributes = {}


    def enable_vertex_attrib_array(self, index):
        self.attributes[index] = []


    def bind_vertex_attrib_data(self, index, data, size):
        self.attributes[index] = VertexAttribPointer(data, size)


class VertexAttribPointer(object):
    def __init__(self, data, size):
        self.data = data
        self.size = size


class Vertex(object):
    def __init__(self, attributes):
        self.attributes = attributes
        self.position = None


class Primitive(object):
    def __init__(self, vertices):
        self.vertices = vertices


class Fragment(object):
    def __init__(self, screen, attributes):
        self.screen = screen
        self.attributes = attributes
        self.color = None


unicornhathd.brightness(0.2)
unicornhathd.rotation(90)

def main():
    global M, V, P, view, depth_buffer, frame_buffer

    verts = [
        # face 1 (front)
        glm.vec4(-1, 1, 1, 1),
        glm.vec4(-1, -1, 1, 1),
        glm.vec4(1, -1, 1, 1),

        glm.vec4(1, 1, 1, 1),
        glm.vec4(-1, 1, 1, 1),
        glm.vec4(1, -1, 1, 1),
      
        # face 2 (right)
        glm.vec4(1, 1, 1, 1),
        glm.vec4(1, -1, 1, 1),
        glm.vec4(1, -1, -1, 1),

        glm.vec4(1, 1, -1, 1),
        glm.vec4(1, 1, 1, 1),
        glm.vec4(1, -1, -1, 1),

        # face 3 (back)
        glm.vec4(1, 1, -1, 1),
        glm.vec4(1, -1, -1, 1),
        glm.vec4(-1, -1, -1, 1),
        
        glm.vec4(-1, 1, -1, 1),
        glm.vec4(1, 1, -1, 1),
        glm.vec4(-1, -1, -1, 1),

        # face 4 (left)
        glm.vec4(-1, 1, -1, 1),
        glm.vec4(-1, -1, -1, 1),
        glm.vec4(-1, -1, 1, 1),

        glm.vec4(-1, 1, 1, 1),
        glm.vec4(-1, 1, -1, 1),
        glm.vec4(-1, -1, 1, 1),

        # face 5 (top)
        glm.vec4(-1, 1, -1, 1),
        glm.vec4(-1, 1, 1, 1),
        glm.vec4(1, 1, 1, 1),

        glm.vec4(1, 1, -1, 1),
        glm.vec4(-1, 1, -1, 1),
        glm.vec4(1, 1, 1, 1),

        # face 6 (bottom)
        glm.vec4(-1, -1, 1, 1),
        glm.vec4(-1, -1, -1, 1),
        glm.vec4(1, -1, -1, 1),

        glm.vec4(1, -1, 1, 1),
        glm.vec4(-1, -1, 1, 1),
        glm.vec4(1, -1, -1, 1)
    ]

    colors = [
        # face 1 (front)
        glm.vec4(1, 0, 0, 1),
        glm.vec4(1, 0, 0, 1),
        glm.vec4(1, 0, 0, 1),

        glm.vec4(1, 0, 0, 1),
        glm.vec4(1, 0, 0, 1),
        glm.vec4(1, 0, 0, 1),

        # face 2 (right)
        glm.vec4(0, 1, 0, 1),
        glm.vec4(0, 1, 0, 1),
        glm.vec4(0, 1, 0, 1),

        glm.vec4(0, 1, 0, 1),
        glm.vec4(0, 1, 0, 1),
        glm.vec4(0, 1, 0, 1),

        # face 3 (back)
        glm.vec4(0, 0, 1, 1),
        glm.vec4(0, 0, 1, 1),
        glm.vec4(0, 0, 1, 1),

        glm.vec4(0, 0, 1, 1),
        glm.vec4(0, 0, 1, 1),
        glm.vec4(0, 0, 1, 1),

        # face 4 (left)
        glm.vec4(1, 1, 0, 1),
        glm.vec4(1, 1, 0, 1),
        glm.vec4(1, 1, 0, 1),

        glm.vec4(1, 1, 0, 1),
        glm.vec4(1, 1, 0, 1),
        glm.vec4(1, 1, 0, 1),

        # face 5 (top)
        glm.vec4(0, 1, 1, 1),
        glm.vec4(0, 1, 1, 1),
        glm.vec4(0, 1, 1, 1),

        glm.vec4(0, 1, 1, 1),
        glm.vec4(0, 1, 1, 1),
        glm.vec4(0, 1, 1, 1),

        # face 6 (bottom)
        glm.vec4(1, 0, 1, 1),
        glm.vec4(1, 0, 1, 1),
        glm.vec4(1, 0, 1, 1),

        glm.vec4(1, 0, 1, 1),
        glm.vec4(1, 0, 1, 1),
        glm.vec4(1, 0, 1, 1)
    ]

    w, h = unicornhathd.get_shape()
    view = Viewport(0, 0, w, h, 0.1, 100)

    depth_buffer = [view.f] * view.w * view.h
    frame_buffer = [glm.vec4(0, 0, 0, 1)] * view.w * view.h

    vao = VertexArrayObject()

    vao.enable_vertex_attrib_array(0)
    vao.bind_vertex_attrib_data(0, verts, 3)

    vao.enable_vertex_attrib_array(1)
    vao.bind_vertex_attrib_data(1, colors, 3)

    M = glm.mat4(1)

    V = glm.lookAt(glm.vec3(0, 0, 5), 
                   glm.vec3(0, 0, 0), 
                   glm.vec3(0, 1, 0))

    P = glm.perspective(glm.radians(45), view.w / view.h, view.n, view.f)

    try:
        while True:
            t = time.process_time()
            clear_screen()

            V = glm.rotate(V, 0.05, glm.vec3(math.sin(t), math.cos(t), math.sin(t)))

            pipeline(vao)
            draw()

    except KeyboardInterrupt:
        unicornhathd.off()


def pipeline(vao):
    vertices = vertex_specification(vao.attributes)

    for vertex in vertices:
        vertex.position, vertex.attributes = vertex_shader(vertex.attributes, {})
        vertex_post_processing(vertex)

    primitives = primitive_assembly(vertices)
    fragments = rasterize(primitives)

    for fragment in fragments:
        fragment.color = fragment_shader(fragment.attributes)
        per_sample(fragment)


def vertex_specification(attributes):
    return [Vertex({k: attributes[k].data[i] for k in attributes.keys()}) for i in range(0, len(attributes[0].data))]


def vertex_shader(v_attr, out):
    # in
    v_position = v_attr[0]
    color = v_attr[1]
    # out
    position = v_position
    out["color"] = color

    return position, out


def vertex_post_processing(vertex):
    vertex.position = P * V * M * vertex.position


def primitive_assembly(vertices):
    return [Primitive(vertices[i:i+3]) for i in range(0, len(vertices), 3)]


def rasterize(primitives):
    out = []
    for primitive in primitives:
        screen_vertices = [clip_to_screen_space(v.position) for v in primitive.vertices]
        min_x = math.floor(min(screen_vertices, key=lambda v: v.x).x)
        min_y = math.floor(min(screen_vertices, key=lambda v: v.y).y)
        max_x = math.ceil(max(screen_vertices, key=lambda v: v.x).x)
        max_y = math.ceil(max(screen_vertices, key=lambda v: v.y).y)

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

                inside = True
                inside &= top_left_test(v1, v2) if w0 == 0 else w0 > 0
                inside &= top_left_test(v2, v0) if w1 == 0 else w1 > 0
                inside &= top_left_test(v0, v1) if w2 == 0 else w2 > 0

                if inside:
                    a = w0 / area / primitive.vertices[0].position.w
                    b = w1 / area / primitive.vertices[1].position.w
                    g = w2 / area / primitive.vertices[2].position.w

                    z, attr_interp = interpolate_primitive(a, b, g, primitive)
                    out.append(Fragment(glm.vec3(x, y, z), attr_interp))

    return out


def fragment_shader(f_attr):
    # in
    color = f_attr["color"]
    # out
    return color


def per_sample(fragment):
    x, y, z = int(fragment.screen.x), int(fragment.screen.y), fragment.screen.z

    if x < view.x or x >= view.w or y < 0 or y >= view.h:
        return

    if z < depth_buffer[x * view.w + y]:
        depth_buffer[x * view.w + y] = z
        frame_buffer[x * view.w + y] = fragment.color


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


def interpolate_primitive(a, b, g, primitive):
    attr = {}
    depth = interpolate(a, b, g, 
                        primitive.vertices[0].position.z, 
                        primitive.vertices[1].position.z, 
                        primitive.vertices[2].position.z)

    for key in primitive.vertices[0].attributes.keys():
        attr[key] = interpolate(a, b, g, 
                                primitive.vertices[0].attributes[key], 
                                primitive.vertices[1].attributes[key], 
                                primitive.vertices[2].attributes[key])
    return depth, attr


def interpolate(a, b, g, f1, f2, f3):
    return (a * f1 + b * f2 + g * f3) / (a + b + g)


def clear_screen():
    global depth_buffer, frame_buffer
    depth_buffer = [view.f] * view.w * view.h
    frame_buffer = [glm.vec4(0, 0, 0, 1)] * view.w * view.h
    unicornhathd.clear()


def draw():
    for x in range(0, view.w):
        for y in range(0, view.h):
            color = frame_buffer[x * view.w + y]
            unicornhathd.set_pixel(x, y, color.x * 255, color.y * 255, color.z * 255)
    unicornhathd.show()


if __name__ == "__main__":
    main()
