import dataclasses


@dataclasses.dataclass
class ToDo:
    _id: int
    name: str
    isDone: bool

    @property
    def id(self):
        return self._id

todoList = [ToDo(_id=0, name="read a book" ,isDone=True)]
def createToDo(name):
    newTodo = ToDo(len(todoList), name, False)
    todoList.append(newTodo)

def getToDos():

    return todoList

def getToDo(id):
    return todoList[id]

def deleteToDo(id):
    todoList.pop(id)

def updateToDo(id, name, is_done):
    todoList[id].name = name
    todoList[id].isDone = is_done

def markAsDone(_id, value: bool):
    itemTarget = next((item for item in todoList if item.id == _id) , None)
    if itemTarget:
        itemTarget.isDone = value
