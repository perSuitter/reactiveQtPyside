### Example To Do App showing reactive pyside framework

## Installation

```console
git clone https://github.com/perSuitter/reactiveQtPyside.git
```
#### Python version

Python 3.10.12

#### Set virtual env

```console
python -m venv myenv
```

#### Install dependencies

```console
pip install -r requirements.txt
```

#### Start application

```console
python  main.py
```
## Examples

Models must implement set and get methods to notify changes

#### Example todo List Ordered Model reacts to todo List Model

```python 
    ModelBridge(
        todoListModel, [
            todoOrderedModel
        ]
    )
```
#### Example todo List Model reacts to adding item input event

```python 
    ViewBridge(
        todoInput, [
            todoListModel.add
        ],
       [ "addItem"]
    )
```
