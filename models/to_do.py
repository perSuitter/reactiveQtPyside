
from typing import Optional

from services.to_do import ToDo, createToDo, getToDos, markAsDone, updateToDo

class TodoListModel:
    todoList: Optional[list[ToDo]] =[]
    initiated =False
    def __init__(self):
        self.set(getToDos())
        self.initiated= True

    def set(self, _list: list[ToDo] = None):

        self.todoList = _list 
       
    def get(self):
        return self.todoList
    
    def add(self, _todo: dict):

        createToDo(_todo)
        self.set(getToDos())
    def checkItem(self, idItem, value):

        markAsDone(idItem, value)
        self.set(getToDos())
    def editName(self, idItem, newName):
        updateToDo(idItem, newName, self.todoList[idItem].isDone)
        self.set(getToDos())
class OrderedListModel():
    todoList = None
    def __init__(self):
        pass

    def set(self, listTodo):

        self.todoList = sorted(listTodo, key=lambda x: x.isDone)

    def get(self):
        return self.todoList