import requests
from bs4 import BeautifulSoup
import re
import json
import psycopg2


class GrandExchange:
    def create_conn(self):
        """Create DB connection & Cursor"""
        self.conn = psycopg2.connect(
            database="grand_exchange",
            user="postgres",
            password="Oosstt123",
            host="localhost",
        )
        self.cursor = self.conn.cursor()

    def close_conn(self):
        """Closes connection & Cursor """
        self.cursor.close()
        self.conn.close()

    def display_top_twenty(self, category):
        # https://stackoverflow.com/questions/61400692/how-to-bypass-bot-detection-and-scrap-a-website-using-python
        # don't send more than 2 requests/sec
        """MOST TRADED = 0 ,VALUABLE TRADES = 1, PRICE RISES  = 2, PRICE FALLS = 3\n
        Returns the 100 Item IDs"""
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "referer": "https://www.google.com/",
        }
        r = requests.get(
            f"https://secure.runescape.com/m=itemdb_oldschool/top100?list={category}&scale=0",
            headers=header,
        )
        soup = BeautifulSoup(r.content, "html.parser")
        tbody = soup.select_one("tbody")
        tbody = tbody.find_all("tr")

        links = []
        first_twenty = []
        for t in tbody:
            t = t.select_one("td")
            items = t.select_one("span")
            id = t.find("a")
            id = id["href"]
            items = items.text
            first_twenty.append(items)
            links.append(id)

        counter = 1
        links = links[:100]
        first_twenty = first_twenty[:100]
        object_ids = []
        for f, l in zip(first_twenty, links):
            x = re.search(r"obj=(.*)$", l)
            # print(f"{counter}. {f} id: {x.group(1)}")
            object_id = x.group(1)
            object_ids.append(object_id)
            counter += 1
        return object_ids

    def item_information(self, id):
        """ Extracts information about an item such as icon, type, name, description, price etc. In a dictionary format """
        r = requests.get(
            f"http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item={id}"
        )
        content = r.content
        values = json.loads(content)  # return dictionary
        # Example of how to extract certain values.
        # name = values["item"]["name"]
        # item_id = values["item"]["id"]
        # membership = values["item"]["members"]
        return values

    def populatedb_items(self, ids):
        """ Will populate the database with their names & id"""

        not_working_id = []

        for id in ids:
            # get request
            r = requests.get(
                f"http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item={id}"
            )

            if r.status_code == 200:

                # store name, id in a variable.
                # add it to database.

                content = r.content
                values = json.loads(content)
                name = values["item"]["name"]
                item_id = values["item"]["id"]

                try:
                    # Connect to your postgres DB
                    self.create_conn()
                    self.cursor.execute(
                        'INSERT INTO "GE_item"(item_name, item_id) VALUES (%s, %s)',
                        (name, item_id),
                    )
                    self.cursor.execute('SELECT * FROM "GE_item";')
                    self.conn.commit()
                    self.close_conn()
                    print(f"Added {name} to the database.")
                except Exception as e:
                    print(e)

            else:
                print(f"{r.status_code} - Item doesn't exist in the osrs database.")
                not_working_id.append(id)

        if len(not_working_id) != 0:
            print("Below are the id's which failed")
            print(not_working_id)

    def extract_items(self):
        """ Extract ID from DB """
        self.create_conn()
        self.cursor.execute(
            'SELECT * FROM "GE_item";'
        )
        items = self.cursor.fetchall()
        return items
    
    def populatedb_values(self, items):
        #extract items
       for item in items:

            r = requests.get(
                f"http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item={item[1]}"
            )

            r_graph = requests.get(
                f"https://services.runescape.com/m=itemdb_rs/api/graph/{item[1]}.json"
            )

            if r.status_code == 200:
                content = r.content
                values = json.load(content)
                price = values["item"]["price"]
                self.create_conn()
                self.cursor.execute(
                    'SELECT CAST( current_date AS Date ) ;'
                )
                date = self.cursor.fetchall()
                self.cursor.execute(
                    'INSERT INTO "GE_itemvalue"(item_id, price, date, volume) VALUES (%s, %s, %s, %s )',
                    (item[1], price, date , volume)
                )


