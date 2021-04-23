import MySQLdb

DB = ""
HOST = "localhost"
USER = "root"
PASSWORD = ""
PORT = 3306


class DataBase:

    def create_connection_and_cursor(self, db_name: str = "") -> None:
        self.conn = MySQLdb.connect(host=HOST, user=USER, password=PASSWORD, port=PORT, db=db_name)
        self.conn.autocommit(True)
        self.cursor = self.conn.cursor()

    def conn_and_cursor_exist(self) -> bool:
        try:
            self.conn
            self.cursor
            return True
        except AttributeError:
            return False

    def is_database_selected(self) -> bool:
        try:
            self.cursor.execute("CREATE TABLE temp_table (teste varchar(1))")
            self.cursor.execute("DROP TABLE temp_table")
            return True
        except Exception:
            return False

    def change_current_database(self, new_database_name: str) -> None:
        self.conn.select_db(new_database_name)

    def convert_list_to_sql_string(self, data: list) -> str:
        converted_to_sql_data = [f"'{value}'"
                                 if isinstance(value, str) and value.upper() != "DEFAULT" and value.upper() != "NULL"
                                 else str(value)
                                 for value in data]
        string_values = ",".join(converted_to_sql_data)
        return string_values

    def insert_data(self, table_to_insert: str, data: list) -> bool:
        if not self.conn_and_cursor_exist():
            raise Exception("Connetion or cursor is not defined!")
        if not self.is_database_selected():
            raise Exception("Database is not selected!")
        if not isinstance(data, list):
            raise TypeError("Data is not a list!")

        string_values = self.convert_list_to_sql_string(data)
        sql = f"""INSERT INTO {table_to_insert} VALUES ({string_values})"""

        try:
            affected_rows = self.cursor.execute(sql)
            if affected_rows > 0:
                return True
        except:
            return False

        return False

    def read_all_data(self, table_to_read: str):
        if not self.conn_and_cursor_exist():
            raise Exception("Connetion or cursor is not defined!")
        if not self.is_database_selected():
            raise Exception("Database is not selected!")

        # string_values = self.convert_list_to_sql_string(data)
        sql = f"""SELECT * FROM {table_to_read}"""
        lista = []
        try:
            affected_rows = self.cursor.execute(sql)

            for i in self.cursor.fetchall():
                lista.append(i)

            if affected_rows > 0:
                return lista
        except:
            return lista

        return False

    def read_selected_data(self, table_to_read: str, column_to_reference: str, value_to_reference: str):
        if not self.conn_and_cursor_exist():
            raise Exception("Connetion or cursor is not defined!")
        if not self.is_database_selected():
            raise Exception("Database is not selected!")

        # string_values = self.convert_list_to_sql_string(data)
        sql = f"""SELECT * FROM {table_to_read} WHERE {column_to_reference} = '{value_to_reference}'"""

        try:
            affected_rows = self.cursor.execute(sql)

            for i in self.cursor.fetchall():
                return i

            if affected_rows > 0:
                return True
        except:
            return False

        return False

    def convert_dict_to_sql_string(self, data: dict, separator=",") -> str:
        converted_to_sql_data = []
        for key, value in data.items():
            if isinstance(value, str) and value.upper() != "DEFAULT" and value.upper() != "NULL":
                converted_to_sql_data.append(f"{key} = '{value}'")
            else:
                converted_to_sql_data.append(f"{key} = {value}")

        string_values = f"{separator}".join(converted_to_sql_data)
        return string_values

    def update_data(self, table_to_uptade: str, values_to_uptade: dict, column_to_reference: str, value_to_reference: str):
        if not self.conn_and_cursor_exist():
            raise Exception("Connetion or cursor is not defined!")
        if not self.is_database_selected():
            raise Exception("Database is not selected!")

        # keys_and_values = dict(Nome="Julia", Idade=15, Altura=1.88, CPF="10010010013")
        data_to_update = DataBase().convert_dict_to_sql_string(values_to_uptade)
        sql = f"""UPDATE {table_to_uptade} SET {data_to_update} WHERE 
                {column_to_reference} = '{value_to_reference}'"""

        try:
            affected_rows = self.cursor.execute(sql)
            if affected_rows > 0:
                return True
        except:
            return False

        return False

    def delete_data(self, table_to_delete: str, column_to_reference: str, value_to_reference: str):
        if not self.conn_and_cursor_exist():
            raise Exception("Connetion or cursor is not defined!")
        if not self.is_database_selected():
            raise Exception("Database is not selected!")

        sql = f"""DELETE FROM {table_to_delete} WHERE {column_to_reference} = '{value_to_reference}'"""

        try:
            affected_rows = self.cursor.execute(sql)
            if affected_rows > 0:
                return True
        except:
            return False

        return False


teste = DataBase()
teste.create_connection_and_cursor("testunit")
teste.conn_and_cursor_exist()
teste.is_database_selected()
# teste.insert_data("tabela1", ["Gusta", 11, 1.44, "10010010015"])
teste.read_all_data("tabela1")
# print(teste.read_selected_data("tabela1", "Nome", "Laura"))
# teste.update_data("tabela1", "Idade", "13", "Nome", "João")
# teste.update_data("tabela1", "Nome, Idade", "João da Silva, 12", "Nome", "João")
# keys_and_values = dict(Nome="Nádia")
# teste.update_data("tabela1", keys_and_values, "CPF", "10010010012")
# teste.delete_data("tabela1", "Nome", "João")

# def upate_data(self, table_to_uptade: str, column_to_update: str, value_to_update: str,
#                column_to_reference: str, value_to_reference: str):
#     if not self.conn_and_cursor_exist():
#         raise Exception("Connetion or cursor is not defined!")
#     if not self.is_database_selected():
#         raise Exception("Database is not selected!")
#
#     sql = f"""UPDATE {table_to_uptade} SET {column_to_update} = '{value_to_update}' WHERE
#             {column_to_reference} = '{value_to_reference}'"""
#
#     try:
#         affected_rows = self.cursor.execute(sql)
#         if affected_rows > 0:
#             return True
#     except:
#         return False
#
#     return False


