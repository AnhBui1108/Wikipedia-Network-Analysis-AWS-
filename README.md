##LargeScaleDA-P2
## Submission Details

## Includes:
1. **Entry Point for EMR Step:** `entrypoint.py`  
2. **Dependencies for EMR Step:** A `main.zip` file containing:  
   - The driver class: `main.py`  
   - The method class: `method.py`  
3. **Automated Test Suite:** `Test.py`  
4. **Synthetic Dataset**  
5. **README File**

---
## How to Run the Automated Test Suite:
The `test.py` file is designed to run on your local machine. Follow these steps to execute it:  

1. Download the synthetic dataset to your local machine.  
2. Open `test.py` and update the file path:  
   Replace `./TestData/` in this line with the path where you store the downloaded synthetic dataset
   ```python
   path = f"./TestData/{path}"
3. Run test.py as a regular Python script.

## Synthetic Dataset Details:
The dataset includes four (04) '.jsonl' files:
1. page.jsonl: Simulates the "page" dataset from Wikipedia.
2. linktarget.jsonl: Simulates the "linktarget" dataset from Wikipedia.
3. pagelinks.jsonl: Simulates the "pagelinks" dataset from Wikipedia.
4. redirect.jsonl: Simulates the "redirect" dataset from Wikipedia.
   
#### Dataset Scenarios
The dataset covers two scenarios for mutual link pairs:

- Case 1: A → B (Page A links to Page B) and B → A (Page B links back to Page A).
- Case 2: A → D → C → A (Page A links to Page D, Page D redirects to Page C, and Page C links back to Page A).
For connected components, the dataset includes a basic scenario: Example: A → B → C (Page A connects to Page B, and Page B connects to Page C).
Note: There are no cycles in the connected components.

## Reflection
#### Project 1:
This project was interesting. The most challenging part wasn’t the coding but understanding the Wikipedia dataset and figuring out how to run Spark on both interactive and non-interactive EMR clusters.

The most enjoyable part was improving performance. My first attempt took about 60 minutes, meeting the requirement, but I aimed to reduce it to 20 minutes or less. I tried several strategies: broadcast joins, repartitioning, and writing code to fully utilize Spark's parallelism to optimize two major tasks—joining with pagelinks and computing unique mutual link pairs.
I too focused on improving the perfomance and overlooked checking whether my code met all project requirements, which cost me some points. However, this process taught me a lot about Lazy evolution, paralle, bottelnech I/O, how spark method working, Spark UI and how to read the dash. These literally helps handle the midterm effectively. Overall, it was worth the effort.

#####Key Learnings:
For Spark:
- Broadcast joins and repartitioning didn’t significantly help for this project.
- Cache intermedate - that needs to be resused mutiple times significantly improves performance. A HUG BIG NOTE ###Persist() is not an action—it doesn’t trigger computation.
- Spark is lazily evaluated; for example, .show(n=20) computes only the first 20 rows.
For projects in general:
- Ensure the code meets requirements before focusing on optimization.
- To improve performance, explore new logic, not just different methods
