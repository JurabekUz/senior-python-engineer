"""
CHALLENGE: Advanced Functional Programming
==========================================

Complete the following tasks using ONLY lambda, map, filter, and reduce.
Try to avoid explicit 'for' loops if possible!

-------------------------------------------------------------------------
TASK 1: The E-commerce Analyst
Data: A list of orders where each order is (id, category, price, status)
Goal:
  1. Filter for 'completed' orders.
  2. For 'electronics', apply a 10% discount if price > 500.
  3. Calculate the total revenue of all electronics after discount.
-------------------------------------------------------------------------
"""
from functools import reduce

orders = [
    (1, "electronics", 800, "completed"),
    (2, "clothing", 50, "completed"),
    (3, "electronics", 400, "completed"),
    (4, "electronics", 1200, "cancelled"),
    (5, "electronics", 600, "completed"),
    (6, "home", 150, "completed"),
]

# Your code for Task 1 here:
# total_electronics_revenue = ...

com_list = filter(lambda x: x[3] == 'completed', orders)
discounted_list = map(lambda x: 0.9*x[2] if x[1] == 'electronics' and x[2] > 50 else x[2], com_list)
total_electronics_revenue = reduce(lambda x,y: x+y, discounted_list)

"""
-------------------------------------------------------------------------
TASK 2: The Sensor Data Cleaner
Data: A list of sensor readings (floats) with some noisy data.
Goal:
  1. Filter out any None values.
  2. Filter out outliers (keep only values between 0 and 100).
  3. Round all remaining values to the nearest integer.
  4. Calculate the average of these cleaned values.
-------------------------------------------------------------------------
"""
readings = [25.5, None, 120.3, 44.1, -5.2, 88.9, None, 15.0, 99.9]

# Your code for Task 2 here:
# average_reading = ...
filtered_list = filter(lambda x: x != None and x in range(1,100), readings)
rounded_list = map(lambda x: round(x), filtered_list)
average_reading = reduce(lambda x, y: (x+y)/2, rounded_list)


"""
-------------------------------------------------------------------------
TASK 3: The Functional Pipeline
Data: A list of raw strings.
Goal:
  1. Filter for strings that contain more than 2 words.
  2. Normalize them: convert to lowercase and strip whitespace.
  3. Join them into a single large paragraph using reduce, with " | " 
     as a separator between sentences.
-------------------------------------------------------------------------
"""
raw_data = [
    "  Python is amazing   ",
    "Short",
    "  LAMBDA FUNCTIONS ARE POWERFUL  ",
    "Functional programming is cool",
    "  map and filter  "
]

# Your code for Task 3 here:
# final_paragraph = ...

filtered_list = filter(lambda st: len(st.split()) > 2, raw_data)
styled_list = map(lambda x: x.lower().strip(), filtered_list)
final_paragraph = reduce(lambda x, y: x.join(" | "), styled_list)

# ─────────────────────────────────────────────
# Testing Area (Print your results here)
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Task 1 Result: {total_electronics_revenue}")
    print(f"Task 2 Result: {average_reading}")
    print(f"Task 3 Result: {final_paragraph}")
