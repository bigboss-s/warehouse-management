import sqlite3


class DatabaseManager:
    def __init__(self):
        self.con = sqlite3.connect('inventory.db')
        self.con.row_factory = sqlite3.Row
        self.init_db()

    def init_db(self):
        cur = self.con.cursor()

        cur.executescript("""
            DROP TABLE IF EXISTS Item;
            CREATE TABLE IF NOT EXISTS Item (
                id INTEGER PRIMARY KEY ASC,
                name varchar(50) NOT NULL,
                description varchar(250),
                price DOUBLE NOT NULL,
                num_of_available_items INTEGER NOT NULL
            )""")

        sample_items = (
            (None, "Item 1", "Something", 25.5, 10),
            (None, "Item 2", "Nothing", 123, 5),
            (None, "Item 3", "-", 0.99, 20),
            (None, "metI", "-", 420, 30)
        )
        cur.executemany("INSERT INTO Item VALUES(?, ?, ?, ?, ?)", sample_items)
        self.con.commit()

    def fetch_all_items(self):
        cur = self.con.cursor()
        cur.execute('SELECT * FROM Item')
        return cur.fetchall()

    def search_by_id(self, query):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM item WHERE id = ?", (query,))
        return cur.fetchall()

    def search_by_name(self, query):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM item WHERE name LIKE ?", ("%" + query + "%",))
        return cur.fetchall()

    def insert_item(self, item):
        cur = self.con.cursor()
        cur.execute("INSERT INTO item VALUES(?, ?, ?, ?, ?)",
                    (None, item.get_name(), item.get_description(),
                     item.get_price(), item.get_num_of_available_items()))
        self.con.commit()

    def edit_item(self, item):
        cur = self.con.cursor()
        cur.execute("UPDATE item SET name = ?, description = ?, "
                    "price = ?, num_of_available_items = ? WHERE id = ?", (item.get_name(),
                                                                           item.get_description(),
                                                                           item.get_price(),
                                                                           item.get_num_of_available_items(),
                                                                           item.get_id()))
        self.con.commit()

    def delete_items(self, item_ids):
        cur = self.con.cursor()
        cur.executemany("DELETE FROM item WHERE id = ?", [(id, ) for id in item_ids])

    def close(self):
        self.con.close()

    def fetch_items_by_price(self, min, max):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM item WHERE price BETWEEN ? AND ?", (min, max,))
        return cur.fetchall()

    def fetch_items_by_amount(self, min, max):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM item WHERE num_of_available_items BETWEEN ? AND ?", (min, max,))
        return cur.fetchall()
