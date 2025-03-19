import numpy as np
import pylab as plt

''' PARTICLE FILTERS '''

def motion_mdl(state, distance=0.5):
    '''
    Motion model for a particle filter
    state: [x, y, f] - x, y: position, f: angle
    distance: distance moved
    '''
    x, y, f = state
    f = f + np.random.normal(f, 0.1)
    d = np.random.normal(distance, 0.01)
    x += d*np.cos(f)
    y += d*np.sin(f)

    return x, y, f

def prediction(particles, samples=30):
    '''
    Predict the next state of the particles
    '''
    return [motion_mdl(state) for _ in range(samples) for state in particles]

def estimate(particles):
    '''
    Estimate the position of the particles
    '''
    p = np.array(particles)
    return np.mean(p, axis=0)

# def weight(measurement, state):
#     '''
#     Weight of the particles
#     '''
#     x, y, f = state

def update_robot(real_state):
    '''
    Update the real state of the robot
    '''
    x, y, f = real_state
    return x + 0.5, y, f

def weight(measurement, particle):
    '''
    Weight of the particles
    '''
    x, y, f = particle
    d = np.sqrt((x-2)**2 + (y-0)**2) # Distance from the tree on position [2,0] -- TODO: add tree list
    return 1/np.abs(d - measurement)

def resampling(particles, weights, samples=10):
    '''
    Resampling the particles
    '''
    size, count = 0, 0
    result_space, result_weights = [], []

    while(size<samples):
        count = np.random.randint(len(weights))
        if (np.random.random() < weights[count]):
            result_space.append(particles[count])
            result_weights.append(1. / samples)
            del particles[count]
            del weights[count]
            size += 1
    return result_space, result_weights

if __name__ == '__main__':
    iter = 100
    initial_state = 0, 0, 0
    print(motion_mdl((0, 0, 0)))

    x, y, _ = initial_state
    plt.plot(x, y, 'bo')

    p = [initial_state]
    real_state = initial_state

    for i in range(iter):
        p = prediction(p)

        real_state = update_robot(real_state)
        measurement = 2.0 - real_state[0]

        w = [weight(measurement, particle) for particle in p]
        w = [wght/sum(w) for wght in w]

        p, _ = resampling(p, w)

        for state in p:
            x, y, f = state
            plt.plot([x, x +0.02*np.cos(f)], [y, y+0.02*np.sin(f)], 'r-')

        x, y, f = estimate(p)
        plt. plot([x, x +0.02*np.cos(f)], [y, y+0.02*np.sin(f)], 'b-')
        x, y, f = real_state
        plt.plot(x, y, 'g*')

    plt.axis('square')
    plt.show()