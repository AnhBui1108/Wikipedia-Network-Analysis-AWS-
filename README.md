
**Submission Details**

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

### Reflection
#### Project 1
This project was interesting. The most challenging part wasn’t the coding but understanding the Wikipedia dataset and figuring out how to run Spark on both interactive and non-interactive EMR clusters.

The most enjoyable part was improving performance. My first attempt took about 60 minutes, meeting the requirement, but I aimed to reduce it to 20 minutes or less. I tried several strategies: broadcast joins, repartitioning, and writing code to fully utilize Spark's parallelism to optimize two major tasks—joining with pagelinks and computing unique mutual link pairs.
I too focused on improving the perfomance and overlooked checking whether my code met all project requirements, which cost me some points. However, this process taught me a lot about Lazy evolution, paralle, bottelnech I/O, how spark method working, Spark UI and how to read the dash. These literally helps handle the midterm effectively. Overall, it was worth the effort.

#### Key Learnings:
**For Spark**
- Broadcast joins and repartitioning didn’t significantly help for this project.
- Cache intermedate - that needs to be resused mutiple times significantly improves performance. A HUG BIG NOTE ### `Persist()` is not an action—it doesn’t trigger computation.
- Spark is lazily evaluated; for example, `.show(n=20)` computes only the first 20 rows.
**For projects in general**
- Ensure the code meets requirements before focusing on optimization.
- To improve performance, explore new logic, not just different methods

#### Project 2:
Learning from Project 1, I carefully considered two logical approaches for finding connected components in this project:

- **Approach 1**: Create a bidirectional edge table (bidi edge) and join the output of each iteration to this bidi edge. This approach is simple and easy to implement, but it requires joining a table with ~400 million rows in every iteration.
- **Approach 2**: Create an adjacency list for each node. For each node in the list, find its component ID and assign it a new component ID based on the smallest value between the node itself and its neighbors. This approach involves joining two smaller tables.
I initially thought Approach 2 would be faster due to the smaller table size, but I was wrong. Approach 1 took ~34 seconds per iteration, while Approach 2 took ~90 seconds per iteration. After reviewing the logs and dashboard, I realized why. In Approach 1, although it joins a 400-million-row table, it allows us to directly perform the join, fully leveraging Spark's parallelism. In contrast, Approach 2 requires multiple steps before joining, which limits parallelism and makes it slower.

**Most challenging**: 
The most headache I 've got are both from Project 1, specifically when computing mutual links:

- **Incorrect assumption**: I initially assumed that all page_namespace = 0. This led to a mutual link table with ~900 million rows, which cost me an entire day to realize and fix.
- **Computing mutual links for all page**: I computed mutual links for all pages, including article pages, user pages, and others. This resulted in **~192 million mutual link rows** with **~11 million unique vertices**, taking over **`150 iterations`**, which couldn’t finish within 90 minutes. I used the same logic as yours, with similar iteration times (~32 seconds), but the difference was the number of unique vertices. I then updated my code to compute mutual links only for article pages (page_namespace == 0). After this change, the code worked perfectly.
  
**Question:**
If Page A and Page B have mutual links, but neither is an article page (page_namespace != 0), are they still included in the mutual link table?

**Most time consuming part:**
Adjusting the script file felt like playing an endless game of "Whack-a-Bug".  I lost count of how many times the cluster encountered step failures due to minor mistakes—like a typo or updating the main class but forgetting to update the corresponding methods, and vice versa. I wish I had used VS Code instead of Jupyter Notebook

Overall, I spent about 80% of my time fixing bugs, but it was all worth it. I learned so much from this. 
### Ovarall
I think both projects were excellent. They truly helped me learn a lot about Spark, it methods and some tips for debugging. And it also taught me how frustrating it is to wait 40 minutes for a program to stop due to a tiny silly mistake that you made, only to have to run it again and again.
