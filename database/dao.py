from database.DB_connect import DBConnect
from model.gene import Gene # Importo la classe Gene

class DAO:

    # Ci servono tutti i cromosomi per averli come vertici del grafo
    @staticmethod
    def get_cromosomi():
        conn = DBConnect.get_connection()

        result = []

        if conn is None:
            print('Errore di connessione al database!')
            return None

        cursor = conn.cursor(dictionary=True)
        query=""" SELECT DISTINCT cromosoma FROM gene WHERE cromosoma!=0"""
        cursor.execute(query)
        # E' necessario che non ci siano ripetizioni !!!
        for row in cursor:
            result.append(row['cromosoma'])

        cursor.close()
        conn.close()
        return result # Restituisce una lista di stringhe

    @staticmethod
    def get_geni():
        conn = DBConnect.get_connection()

        result = []

        if conn is None:
            print('Errore di connessione al database!')
            return None

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM gene """
        cursor.execute(query)

        for row in cursor:
            result.append(Gene(**row))  # Modo compatto per fare la mappatura degli attributi

        cursor.close()
        conn.close()
        return result  # Restituisce una lista di oggetti

    @staticmethod
    def get_geni_connessi():
        conn=DBConnect.get_connection()
        result = []

        if conn is None:
            print('Errore di connessione al database!')
            return None

        cursor = conn.cursor(dictionary=True)
        query=""" 
        SELECT g1.id AS gene1, g2.id AS gene2, i.correlazione
        FROM interazione i, gene g1, gene g2
        WHERE g1.id=i.id_gene1 AND g2.id=i.id_gene2
                AND g2.cromosoma != g1.cromosoma
                AND g2.cromosoma != 0 AND g1.cromosoma != 0
        GROUP BY g1.id, g2.id
        """
        # Per ogni coppia di geni

        cursor.execute(query)
        for row in cursor:
            result.append((row['gene1'], row['gene2'], row['correlazione']))
            # Lista fatta di tuple da 3 elementi ciascuna

        cursor.close()
        conn.close()
        return result
