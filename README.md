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

