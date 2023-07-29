from PyQt5 import QtWidgets

class WorkspaceTree( QtWidgets.QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setRootIsDecorated(False)
        self.setSortingEnabled(True)
        self.header().sectionsMovable()
 
        self.header().setSectionHidden(0, True) # ID
        self.header().setSectionHidden(1, True) # Path

    def remove_tree_item(self):
        selected_items = self.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            parent = item.parent()
            if parent is None:
                index = self.indexOfTopLevelItem(item)
                self.takeTopLevelItem(index)
            else:
                parent.removeChild(item)
        return item