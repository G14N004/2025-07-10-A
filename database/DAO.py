from database.DB_connect import DBConnect
from model.arco import Arco
from model.categoria import Categoria
from model.prodotto import Prodotto


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getCategorie():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """
        select *
        from categories c 
        """
        cursor.execute(query)
        for row in cursor:
            res.append(Categoria(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getNodi(cat_id):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """
        select p.*
        from categories c , products p 
        where c.category_id = p.category_id and c.category_id = %s
        """
        cursor.execute(query,(cat_id,))
        for row in cursor:
            res.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getArchi(cat_id,data_inizio,data_fine,idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """
        SELECT 
	p1.product_id AS nodo1, 
    COUNT(DISTINCT oi1.order_id) AS vendite_nodo1,
    p2.product_id AS nodo2, 
    COUNT(DISTINCT oi2.order_id) AS vendite_nodo2
FROM 
    categories c1, products p1, order_items oi1, orders o1,
    categories c2, products p2, order_items oi2, orders o2
WHERE 
	c1.category_id =p1.category_id and c1.category_id =%s and p1.product_id =oi1.product_id and oi1.order_id =o1.order_id 
	and o1.order_date between %s and %s and c2.category_id =p2.category_id and c2.category_id =%s and p2.product_id = oi2.product_id and oi2.order_id =o2.order_id 
	and o2.order_date between %s and %s and p1.product_id <>p2.product_id 
	
GROUP BY 
    p1.product_id, 
    p2.product_id

        """
        cursor.execute(query,(cat_id,data_inizio,data_fine,cat_id,data_inizio,data_fine))
        for row in cursor:
            res.append(Arco(idMap.get(row["nodo1"]),row["vendite_nodo1"],idMap.get(row["nodo2"]),row["vendite_nodo2"]))

        cursor.close()
        conn.close()
        return res




