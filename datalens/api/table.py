class Table(object):
    def __init__(self, cursor) -> None:
        self._cursor = cursor
        self._name = ""

    def _exists(self, ) ->bool:
        self._cursor.execute("SHOW TABLES")
        for x in self._cursor:
            if x[0] == self._name:
                return True
            
    def _row_exists(self, row_id:int) ->bool:
        for file in self.get_rows():
            if file[0] == str(row_id):
                return True