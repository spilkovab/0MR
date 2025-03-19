import numpy as np
import pylab as plt


def motion_mdl(state,distance = 0.5):
    x,y,f = state
    f = np.random.normal(f, 0.1)
    d = np.random.normal(distance,0.01)
    x += d * np.cos(f)
    y += d * np.sin(f)
    return x, y, f    

def preditcion(particles, samples = 30):
    return [motion_mdl(state) for _ in range(samples) for state in particles]

def estimate(particles):
    p = np.array(particles)
    return np.mean(p, axis = 0)

def update_robot(real_state):
    x, y, f = real_state
    return x + 0.5, y, f

def weight(measurement, particle):
    x, y, f = particle
    d = np.sqrt((x-2)**2 + (y-0)**2) # prekazka na pozici [2, 0]
    e = d - measurement
    return 1/np.abs(e) + 1/f

def resampling(state_space, state_weights, __samples = 10):
    size, count = 0, 0
    result_space, result_weights = [],[]
    while (size < __samples):
        count = np.random.randint(len(state_weights))
        if (np.random.random() < state_weights[count]):
            result_space.append(state_space[count])
            result_weights.append(1. / __samples)
            del state_space[count]
            del state_weights[count]
            size+=1
    return result_space, result_weights

if __name__ == "__main__":
    iter = 100
    init_state = 0, 0, 0
    print(motion_mdl((0,0,0)))
    x, y, _ = init_state
    plt.plot(x,y,'bo')

    real_state = init_state

    p = [init_state]


    for i in range(iter):
        p = preditcion(p,30)

        real_state = update_robot(real_state)
        
        # measurement

        measurement = 2.0 - real_state[0]

        w = [weight(measurement, particle) for particle in p]
        w = [wght/sum(w) for wght in w]

        p, _ = resampling(p, w)

        for state in p:
            x,y,f = state
            plt.plot([x, x + 0.02*np.cos(f)],[y, y + 0.02*np.sin(f)],'y-')

        x, y, f = estimate(p)
        plt.plot([x, x + 0.02*np.cos(f)],[y, y + 0.02*np.sin(f)],'r-')
        x, y, f = real_state
        plt.plot([x, x + 0.02*np.cos(f)],[y, y + 0.02*np.sin(f)],'k-')


# plt.axis('square')
plt.show()