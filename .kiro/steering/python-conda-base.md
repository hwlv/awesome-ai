---
inclusion: always
---

# Python Environment

For Python work in this repository, prefer the conda `base` environment instead of bare system `python3` or `pip`.

- Run Python scripts with `conda run -n base python ...`
- Install Python dependencies with `conda run -n base python -m pip install ...`
- Check the interpreter with `conda run -n base python -c "import sys; print(sys.executable)"`
- Avoid using bare `python3`, `python`, `pip`, or `pip3` unless the user explicitly asks for a different environment
- If a command fails because conda is unavailable, report that clearly before falling back
- If the user explicitly requests another env such as `.venv` or a named conda env, follow the user's request

Example commands:

```bash
conda run -n base python main.py
conda run -n base python -m pip install -r requirements.txt
```
