### Example To Do App showing reactive pyside framework

## Python version

Python 3.10.12

## Set virtual env

```console
python -m venv myenv
```
## Install dependencies

```console
pip install -r requirements.txt
```

## Start application

```console
python  main.py
```

# Example todo List Ordered Model reacts to todo List Model

```python 
    ModelBridge(
        todoListModel, [
            todoOrdered
        ]
    )
```
# Example todo List Model reacts to adding item input event

```python 
ViewBridge(
        todoInput, [
            todoListModel.add
        ],
       [ "addItem"]
    )
```
