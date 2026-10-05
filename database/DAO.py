from database.DB_connect import DBConnect


class DAO():

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct country
from customer c 
                """

        cursor.execute(query)

        for row in cursor:

            results.append(row["country"])

        cursor.close()
        conn.close()
        return results
#OUTPUT COUNTRY

    @staticmethod
    def getCustomerByCountry(country):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ select distinct c.Customerid as cliente
from customer c ,invoice i 
where country = %s
and c.CustomerId = i.CustomerId """
        cursor.execute(query, (country,))
        for row in cursor:
            results.append(row["cliente"])
        cursor.close()
        conn.close()
        return results
#OUTPUT CLIENTE (filtrato per country)

    @staticmethod
    def getCustomerbyFatturato(country):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT
    i.CustomerId AS cliente,
    SUM(i.Total) AS TotFatturato
FROM invoice i ,customer c
where c.Country = %s
and i.CustomerId =c.CustomerId 
GROUP BY i.CustomerId """
        cursor.execute(query, (country,))
        for row in cursor:
            results.append((row["cliente"],row["TotFatturato"])) # doppie parentesi crean una tupla
        cursor.close()
        conn.close()
        return results
#output CLIENTE (filtrato per country) | TOT FATTTURATO
    @staticmethod
    def getCustomer1Customer2(country):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT
            c.CustomerId AS cliente1,
            c2.CustomerId AS cliente2,
            a1.ArtistId AS artista

        FROM customer c,
             invoice i,
             invoiceline i2,
             track t,
             album a1,

             customer c2,
             invoice i3,
             invoiceline i4,
             track t2,
             album a2

        WHERE c.Country = %s
        and c2.Country = %s

        -- PRIMO PERCORSO: cliente1 → artista------- 
        AND c.CustomerId = i.CustomerId
        AND i.InvoiceId = i2.InvoiceId
        AND i2.TrackId = t.TrackId
        AND t.AlbumId = a1.AlbumId

        -- SECONDO PERCORSO: cliente2 → artista --------
        AND c2.CustomerId = i3.CustomerId
        AND i3.InvoiceId = i4.InvoiceId
        AND i4.TrackId = t2.TrackId
        AND t2.AlbumId = a2.AlbumId

        -- ARTISTA IN COMUNE --------
        AND a1.ArtistId = a2.ArtistId

        -- Evita cliente1 = cliente2---
        -- ed evita di avere sia (1,10) che (10,1)--
        AND c.CustomerId < c2.CustomerId
    """
        cursor.execute(query, (country,country))

        for row in cursor:
         results.append(
            (row["cliente1"], row["cliente2"], row["artista"])
          )
        cursor.close()
        conn.close()

        return results