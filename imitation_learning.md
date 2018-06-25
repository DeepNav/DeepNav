# Imitation Learning

We will use imitation learning to train a policy that controls the
boat. Imitation learning is the study of algorithms that improve
performance in making decisions by observing demonstrations from a
teacher[1].


Our algorithm will be very similar to DAGGER [2]. The core idea of
DAGGER is to train the first policy from the teacher's demonstration,
and then let the policy explore the environment, the teacher only
corrects the policy after the exploration in hindsight. Allowing the
trained policy to explore the environment makes the training data
distribution closer to the inference distribution, rather than the
teacher demonstration's data distribution. Significantly improve the
reliability of the trained policy.

## DAGGER Pseudo Algorithm

```

The teacher demonstrates the task, collect the states, and the
teacher's actions.

Initialize the dataset as the list of collected pairs of state and
action.

Train the policy on the dataset.

for i = 1 to N do

  Use the trained policy, collect some states.
  
  In hindsight, ask the teacher the action for the collected state.
  
  Append the newly collected pairs of state and action to the dataset.
  
  Train the policy on the dataset.

```

## Our Pseudo Algorithm

In the boat navigation case, the teacher is a person. The problem with
applying DAGGER directly to driving a boat is that it's hard to give
the sensor data to the teacher and ask him what action to take - the
teacher has to be on the boat in the exact moment to know what action
to take. So we modify the DAGGER algorithm to:

```

The teacher demonstrates driving the boat, collect the states, and the
teacher's actions.

Initialize the dataset as the list of collected pairs of state and
action.

Train the policy on the dataset.

for i = 1 to N do

  Let the boat self-drive with the trained policy.
  
  The teacher can take over the boat's control at any time and drive
  with the teacher's policy, collect the pairs of state and action as
  D0.
  
  Append D0 to the dataset.
  
  When the teacher is driving, train the new policy with the new
  dataset in real-time.
```

We think that training the new policy in real-time is essential as it
dramatically increases the iteration speed.


[1] [An Invitation to Imitation](https://www.ri.cmu.edu/publications/an-invitation-to-imitation/)

[2] [A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning](https://www.cs.cmu.edu/~sross1/publications/Ross-AIStats11-NoRegret.pdf)
