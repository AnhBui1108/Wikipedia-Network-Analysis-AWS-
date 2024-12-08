# LargeScaleDA-P2
# Submission Details

## Includes:
1. **Entry Point for EMR Step:** `entrypoint.py`  
2. **Dependencies:** A `main.zip` file containing:  
   - The driver class: `main.py`  
   - The method class: `method.py`  
3. **Automated Test Suite:** `test.py`  
4. **Synthetic Dataset**  
5. **README File**

---
## How to Run the Automated Test Suite:
The `test.py` file is designed to run on your local machine. Follow these steps to execute it:  

1. Download the synthetic dataset to your local machine.  
2. Open `test.py` and update the file path:  
   Replace `./TestData/` in the line  
   ```python
   path = f"./TestData/{path}"
