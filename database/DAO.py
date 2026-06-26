from database.DB_connect import DBConnect
from model.order import Order

from model.store import Store


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from stores"

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(store):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT o.order_id, o.customer_id, o.order_status, o.order_date, o.required_date, o.shipped_date, o.store_id, o.staff_id
                    FROM orders o, stores s 
                    WHERE o.store_id = s.store_id 
                    and s.store_name = %s
                    group by o.order_id"""

        cursor.execute(query, (store,))

        for row in cursor:
            results.append(Order(row["order_id"], row["customer_id"], row["order_status"], row["order_date"], row["required_date"], row["shipped_date"], row["store_id"], row["staff_id"]))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getAllEdges(k, store, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT o1.order_id as id1, o2.order_id as id2, (sum(oi1.quantity) + sum(oi2.quantity)) / DATEDIFF(o2.order_date, o1.order_date) as peso
                    FROM orders o1, orders o2, stores s,
                    order_items oi1, order_items oi2
                    WHERE o1.store_id = s.store_id 
                    and s.store_id = o2.store_id 
                    and o1.order_id = oi1.order_id 
                    and o2.order_id = oi2.order_id 
                    and o1.order_date is not null
                    and o2.order_date is not null
                    and DATEDIFF(o2.order_date, o1.order_date) <= %s
                    and DATEDIFF(o2.order_date, o1.order_date) > 0
                    and s.store_name = %s
                    and o1.order_id < o2.order_id 
                    and o1.order_id != o2.order_id 
                    group by  o1.order_id, o2.order_id"""

        cursor.execute(query, (k, store))

        for row in cursor:
            c1 = idMap[row["id1"]]
            c2 = idMap[row["id2"]]
            peso = row["peso"]
            results.append((c1, c2, peso))

        cursor.close()
        conn.close()
        return results