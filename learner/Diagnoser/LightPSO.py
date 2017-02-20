from random import random
iterations = 3
particles = 10

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
        for particle in range(particles):
            self.position_matrix[particle] = []
            self.velocity_matrix[particle] = []
            for d in range(self.dim):
                self.velocity_matrix[particle].append(random())
                self.position_matrix[particle].append(random())
            self.pbest[particle] = list(self.position_matrix[particle])
            self.pbest_val[particle] = self.tf.probabilty_TF(self.position_matrix[particle])
        self.find_gbest()

    def find_gbest(self):
        self.gbest = self.position_matrix[0]
        self.gbest_val = self.tf.probabilty_TF(self.gbest)
        for particle in range(particles)[1:]:
            current_val = self.tf.probabilty_TF(self.position_matrix[particle])
            if (current_val < self.gbest_val):
                gbest = self.position_matrix[particle]
                self.gbest_val = current_val

    def move_particles(self):
        for particle in range(particles):
            self.move_particle(particle)

    def move_particle(self, particle):
        random_factor = random()
        for d in range(self.dim):
            self.position_matrix[particle][d] += self.velocity_matrix[particle][d]
            self.position_matrix[particle][d] = min(max(self.position_matrix[particle][d], 0), 1)
            if self.position_matrix[particle][d] == 1 or self.position_matrix[particle][d] == 0:
                self.velocity_matrix[particle][d] = 0
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
