
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import  QWidget,QMainWindow,QVBoxLayout
import sys


def main():
    
    app = QApplication(sys.argv)
    from framework.utilities import prepareProject
    prepareProject()
    from models.to_do import OrderedListModel
    from models.to_do import TodoListModel
    from views.to_do import AddTodoInput, TodoListView
    from framework.reactive  import ViewBridge,ModelBridge
    centralWidget = QWidget()
    todoListView = TodoListView()
    todoInput = AddTodoInput()

    todoListModel = TodoListModel()
    todoOrderedModel =  OrderedListModel()

    ViewBridge(
        todoInput, [
            todoListModel.add
        ],
       [ "addItem"]
    )

    ModelBridge(
        todoOrderedModel, [
            todoListView
        ]
    )
    def listTodoItems():
        for todoItemView in todoListView.todoItems:

            ViewBridge(
                todoItemView, [
                    todoListModel.checkItem
                ],
            [ "checkedItem"]
            )
            ViewBridge(
                todoItemView, [
                    todoListModel.editName
                ],
            [ "editItem"]
            )

    ViewBridge(
        todoListView, [
            listTodoItems
        ],
       [ "refreshItem"]
    )
    ModelBridge(
        todoListModel, [
            todoOrderedModel
        ]
    )
    
    mainItem = QMainWindow()
    with open('./styles/styles.qss') as f:
        mainItem.setStyleSheet(f.read())

    mainItem.setCentralWidget(centralWidget)
    centralWidget.setFixedWidth(400)
    vLayout = QVBoxLayout()
    centralWidget.setLayout(vLayout)
    vLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    vLayout.addWidget(todoInput)
    vLayout.addWidget(todoListView)

    w = 400
    h = 1320

    mainItem.resize(w, h)
    mainItem.show()
    app.exec()
    sys.exit(app.exit())



if __name__ == "__main__":
    main()