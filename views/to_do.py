from PySide6.QtWidgets import  QFrame,QWidget,QSizePolicy,QVBoxLayout,QHBoxLayout, QCheckBox,QLabel, QLineEdit,QBoxLayout, QPushButton, QStyleFactory
from models.to_do import ToDo
from PySide6.QtCore import Signal,Qt
from PySide6.QtGui import QFont
class TodoListView(QFrame):
    refreshItem = Signal()
    todoItems = None
    def __init__(self):
        super().__init__()
        vLayout = QVBoxLayout()
        self.setLayout( vLayout)
        vLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vLayout = vLayout

    
    def render(self, todoList: list[ToDo]):
        self.clearList()

        for todoItem in todoList:

            todoItemFrame = ToDoItemView(todoItem)
            self.vLayout.addWidget(todoItemFrame)
            self.todoItems.append(todoItemFrame)
        self.refreshItem.emit()

    def clearList(self):
        if self.todoItems:
            for todoItem in self.todoItems:
                self.vLayout.removeWidget(todoItem)

                todoItem.deleteLater()

        self.todoItems = []
class ToDoItemView(QFrame):
    clicked = Signal(int)
    checkedItem = Signal(int, bool)
    editMode = False
    editItem = Signal(int, str)
    def __init__(self,  todoItem: ToDo) -> None:
        super().__init__()
        self.setStyleSheet("border-width: 1px;")

        self.todoItem = todoItem
       
        boxLayout = QBoxLayout( QBoxLayout.Direction.TopToBottom)

        self.boxLayout = boxLayout
        self.innerViewItemMain(todoItem)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setLayout(boxLayout)

    def innerViewItemMain(self,todoItem):
        hLayoutItem = QHBoxLayout()
        
        todoInfoWidget = self.innerViewMainTodoInfo(todoItem.name)
        todoInfoWidget.setStyleSheet("border-width: 0px;")

        todoChecked = self.innerViewDetail(todoItem.isDone)
        todoChecked.setStyleSheet("border-width: 0px;")

        hLayoutItem.addWidget(todoInfoWidget)
        hLayoutItem.addWidget(todoChecked)
        
        frameMain = QFrame()
        frameMain.setStyleSheet("border-width: 0px;")
        frameMain.setLayout(hLayoutItem)
        self.currentFrame = frameMain
        self.boxLayout.addWidget(frameMain)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.clicked.emit(self.todoItem.id)

    def setEditMode(self, value: bool):
        self.editMode = value
    def innerViewDetail(self, isDone: bool):
        vLayout = QVBoxLayout()
        editButtonl = QPushButton("Edit")
  
        editButtonl.clicked.connect( lambda:  self.changeLayout(True))
        checkBoxItem = QCheckBox("Done")
        with open('styles/checkbox.qss') as f:
            checkBoxItem.setStyleSheet(f.read())
        checkBoxItem.setProperty("border-width", "1px")
        if isDone:
            check = Qt.CheckState.Checked
        else:
            check = Qt.CheckState.Unchecked

        checkBoxItem.setCheckState(check)
        checkBoxItem.checkStateChanged.connect(self.emitCheckedItem)

        vLayout.addWidget(editButtonl)
        vLayout.addWidget(checkBoxItem)
        auxWidget = QWidget()
        auxWidget.setLayout(vLayout)
        auxWidget.setStyleSheet("border-width: 0px;")
        vLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        return auxWidget

    def innerViewMainTodoInfo(self, name):
        vLayout = QVBoxLayout()

        nameLabel = QLabel(name)
        nameLabel.setFont(QFont("Arial", 12, QFont.Weight.Bold))

        nameLabel.setWordWrap(True)
        vLayout.addWidget(nameLabel)

        auxWidget = QWidget()
        auxWidget.setLayout(vLayout)
        return auxWidget

    def innerViewEditMode(self):
        hLayout = QHBoxLayout()

        todoEdit = QLineEdit()
        todoEdit.setText(self.todoItem.name)

        editItemButton = QPushButton("Done")

        editItemButton.clicked.connect( lambda: self.changeLayout(False))
        editItemButton.clicked.connect(lambda: self.editItem.emit(self.todoItem.id, todoEdit.text()))

        hLayout.addWidget(todoEdit)
        hLayout.addWidget(editItemButton)
        frameEdit = QFrame()
        frameEdit.setLayout(hLayout)
        self.currentFrame = frameEdit
        self.boxLayout.addWidget(frameEdit)
    def emitCheckedItem(self, val):

        valueFInal = True if val == Qt.CheckState.Checked else False
        self.checkedItem.emit(self.todoItem.id, valueFInal)
    
    def changeLayout(self,val):
        self.editMode = val
        if self.editMode:
            self.boxLayout.removeWidget(self.boxLayout.takeAt(0).widget())
            self.currentFrame.deleteLater()
            self.innerViewEditMode()
        else:   
            self.boxLayout.removeWidget(self.boxLayout.takeAt(0).widget())   
            self.currentFrame.deleteLater()
            self.innerViewItemMain(self.todoItem)

class AddTodoInput(QFrame):
    addItem = Signal(str)
    def __init__(self):
        super().__init__()
  
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        bLayout = QHBoxLayout()
        self.setLayout(bLayout)

        todoEdit = QLineEdit()
        self.todoEdit = todoEdit
        bLayout.addWidget(todoEdit)
        addButton = QPushButton("Add")
        bLayout.addWidget(addButton)

        bLayout.setSpacing(20)
        addButton.clicked.connect(self.emitAddItem )

    def emitAddItem(self):
        self.addItem.emit(self.todoEdit.text())


