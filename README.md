# Intelligent Agent for Playing Flappy Bird using NEAT

Developed by: 
 - Eslam Reda Ragheb
 - Maged Yasser wafa

## 1. General Introduction to the Project

The goal of this project is to build an Intelligent Agent that can learn to play Flappy Bird on its own without being explicitly programmed with the rules. We use an advanced version of the Genetic Algorithm, called **NEAT** (NeuroEvolution of Augmenting Topologies), which helps evolve neural networks by modifying their structure (topology) during the evolution process.

### Summary of the Game Concept

Flappy Bird is a simple game where the player controls a small bird that must pass between pipes without hitting them or the ground.

* Each time the bird successfully passes a pipe, the player gains a point.
* The game ends if the bird collides with a pipe, the ground, or goes off-screen.

### AI Concept in the Project

The AI Agent will repeatedly attempt to play the game.

* In each generation, a population of neural networks evolves through mutations and crossovers, based on the best-performing individuals from the previous generation.
* The goal is for the agent to improve over generations (by passing more pipes) until it reaches an optimal or near-perfect performance.

---

## 2. PEAS Concept

**"PEAS"** stands for four key components that define an AI agent’s design:

1. **Performance Measure**
    * How do we evaluate the agent’s performance?
    * In Flappy Bird, the primary metric is the number of pipes passed before failing.
    * Additional metrics could include the time survived without failing, but the number of pipes passed is usually the most important.

2. **Environment**
    * The environment is the world in which the agent operates.
    * In this case, it’s the Flappy Bird game: the screen, moving pipes, gravity pulling the bird downward, etc.
    * The environment changes over time (pipes move, and gravity affects the bird’s movement).

3. **Actuators (Actions)**
    * These are the actions the agent takes to affect the environment.
    * In Flappy Bird, the primary action is jumping (flap).
    * Another implicit action is not jumping (letting the bird fall).

4. **Sensors (Inputs)**
    * These are the data the agent receives from the environment.
    * In Flappy Bird, the key inputs are:
        * Bird’s position (Y coordinate)
        * Location of the nearest pipe’s opening (top and bottom)
        * Horizontal distance to the upcoming pipe
    * This information is fed into the neural network, which decides whether the bird should jump or not.

---

## 3. Environment Properties (ODESDA)

**"ODESDA"** describes the nature of the environment the intelligent agent interacts with.

1. **O: Observable vs. Partially Observable**
    * Can the agent see everything in the environment?
    * We provide the agent with most of the key information (bird and pipe positions).
    * If all relevant data is available, the environment is almost fully observable.

2. **D: Deterministic vs. Stochastic**
    * Do the same actions always lead to the same outcomes?
    * Flappy Bird is mostly deterministic if all conditions are fixed,
    * but it can be stochastic if pipe placements are randomized.

3. **E: Episodic vs. Sequential**
    * Are decisions independent (Episodic) or do they affect each other over time (Sequential)?
    * The game is episodic at the level of each attempt (start and end separately),
    * but within an episode, decisions are sequential (previous jumps affect the next moves).

4. **S: Static vs. Dynamic**
    * Does the environment change while the agent is deciding?
    * Flappy Bird’s environment is dynamic because pipes move, and the bird falls due to gravity.

5. **D: Discrete vs. Continuous**
    * Are the states and actions fixed or continuous?
    * The actions are discrete (jump or don’t jump).
    * The positions can be treated as continuous values.

6. **A: Single-agent vs. Multi-agent**
    * Are there multiple agents interacting or just one?
    * There is only one agent (the bird), so it is a single-agent environment.

### Summary:

* **Observability:** Almost fully observable.
* **Deterministic/Stochastic:** Mostly deterministic with some randomness in pipe placement.
* **Episodic/Sequential:** Multiple episodes, with sequential decision-making in each.
* **Static/Dynamic:** Dynamic environment.
* **Discrete/Continuous:** Discrete actions (jump/not jump), but states are continuous.
* **Single/Multi-agent:** Single agent.

---

## 4. How NEAT Algorithm Works

**NEAT** (NeuroEvolution of Augmenting Topologies) is a Genetic Algorithm designed to evolve neural networks.
It doesn’t just optimize the connection weights but also evolves the network structure (adding/removing neurons and connections) through mutations.

### Main Stages of NEAT

1. **Initialization**
    * We create a population of neural networks (`pop_size = 50` per generation).
    * Each network starts with a simple structure.
    * The setting `initial_connection = full` means all inputs are initially connected to outputs.

2. **Evaluation**
    * Each network (agent) plays Flappy Bird to measure its fitness.
    * Fitness is calculated based on pipes passed.
    * If an agent reaches a threshold (`fitness_threshold = 100`), it is considered successful.

3. **Selection**
    * The best networks are selected based on fitness to be used in the next generation.
    * Parameters like `elitism = 2` and `survival_threshold = 0.2` determine how many best-performing agents survive.

4. **Crossover (Breeding)**
    * The genetic information of two top-performing networks (parents) is combined to create a new network (offspring).

5. **Mutation**
    * Random modifications occur to:
        * Connection weights (`weight_mutate_rate = 0.8`, `weight_replace_rate = 0.1`).
        * Adding/removing connections (`conn_add_prob = 0.5`, `conn_delete_prob = 0.5`).
        * Adding/removing neurons (`node_add_prob = 0.2`, `node_delete_prob = 0.2`).

6. **Speciation**
    * Networks are grouped into species to preserve diversity and prevent premature convergence.
    * The `compatibility_threshold = 3.0` defines how different networks must be to belong to separate species.

7. **Repeat the Process**
    * The new generation is evaluated, selected, mutated, and bred again.
    * If the performance stagnates for too long (`max_stagnation = 20`), the process stops.

---

## 5. Conclusion

By using the **NEAT** algorithm with Flappy Bird, we can create an intelligent agent that learns through repeated trials, improving its neural network structure naturally.

The **PEAS** framework helps us understand the agent’s performance, environment, actions, and sensors, while **ODESDA** explains the nature of the environment and its impact on learning.

With a well-configured **NEAT** system, we control population size, mutation rates, crossover mechanisms, and species differentiation, making this project a practical example of AI-driven neuroevolution in a simple interactive game.