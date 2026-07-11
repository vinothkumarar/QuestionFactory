# Queue Builder

The Queue Builder converts one Production Request into one or more
Production Orders.

Example:

Production Request

- Total Questions = 250
- Batch Size = 100

Output:

Batch 6

- Q501–Q600

Batch 7

- Q601–Q700

Batch 8

- Q701–Q750

The Queue Builder automatically determines the number of batches
and the question ranges using the current Factory State.
