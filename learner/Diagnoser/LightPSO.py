from random import random
iterations = 3
particles = range(10)

class LightPSO:

    def __init__(self, dim, tf):
        self.dim = dim
        self.tf = tf
        self.position_matrix = {}
        self.velocity_matrix = {}
        self.pbest = {}
        self.gbest = []
        self.pbest_val = {}
        self.gbest_val = 0.0

    def initialize(self):
        self.position_matrix.update(map(lambda x: (x, map(lambda x: random(), range(self.dim))), particles))
        self.velocity_matrix.update(map(lambda x: (x, map(lambda x: random(), range(self.dim))), particles))
        self.pbest.update(map(lambda particle: (particle,list(self.position_matrix[particle])), particles))
        self.pbest_val.update(map(lambda particle: (particle, self.tf.probabilty_TF(self.pbest[particle])), particles))
        self.find_gbest()

    def find_gbest(self):
        def prob(particle):
            return self.position_matrix[particle], self.tf.probabilty_TF(self.position_matrix[particle])
        self.gbest ,self.gbest_val = min(map(prob, particles),key=lambda x: x[1])

    def move_particles(self):
        map(lambda x: self.move_particles, particles)

    def move_particle(self, particle):
        random_factor = random()
        def update_position(d):
            return min(max(self.position_matrix[particle][d] + self.velocity_matrix[particle][d], 0), 1)
        def update_velocity(d):
            v = self.position_matrix[particle][d]
            return 0 if (v == 1 or v == 0) else v
        self.position_matrix[particle].update(map(lambda d: (d, update_position(d)), range(self.dim)))
        self.velocity_matrix[particle].update(map(lambda d: (d, update_velocity(d)), range(self.dim)))
        temp_val = self.tf.probabilty_TF(self.position_matrix[particle])
        if temp_val < self.pbest_val[particle]:
            self.pbest[particle] = list(self.position_matrix[particle])
            self.pbest_val[particle] = temp_val
        if temp_val < self.gbest_val:
            self.gbest_val = temp_val
            self.gbest = list(self.position_matrix[particle])
        self.update_velocity(particle, random_factor)

    def update_velocity(self, particle, random_factor):
        pb_vector = {}
        gb_vector = {}
        for d in range(self.dim):
            pb_vector[d] = self.pbest[particle][d] - self.position_matrix[particle][d]
            gb_vector[d] = self.gbest[d] - self.position_matrix[particle][d]
            self.velocity_matrix[particle][d] = (0.2 * self.velocity_matrix[particle][d] +
                                                 1 * gb_vector[d] * random_factor +
                                     0.3 * pb_vector[d])
    def run(self):
        self.initialize()
        for i in range(iterations):
            self.move_particles()
        return self.gbest_val
