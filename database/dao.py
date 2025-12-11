from database.DB_connect import DBConnect
from model.rifugio import Rifugio
from model.connessione import Connessione


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    @staticmethod
    def getAllRifugio():
        result = []
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT id AS id_rifugio, nome, localita, altitudine "
                 "FROM rifugio r "
                 "ORDER BY r.id")
        cursor.execute(query)

        for row in cursor:
            rifugio = Rifugio(row['id_rifugio'],
                              row['nome'],
                              row['localita'],
                              row['altitudine'])
            result.append(rifugio)

        cnx.close()
        cursor.close()
        return result

    @staticmethod
    def readAllConnection(year):
        result = []
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT id, id_rifugio1, id_rifugio2, distanza, difficolta, anno "
                 "FROM connessione c "
                 "WHERE c.anno <= %s")
        cursor.execute(query, (year,))

        for row in cursor:
            connessione = Connessione(row['id'],
                                      row['id_rifugio1'],
                                      row['id_rifugio2'],
                                      row['distanza'],
                                      row['difficolta'],
                                      row['anno'])
            result.append(connessione)
        cnx.close()
        cursor.close()
        return result
    # TODO
