from database.DB_connect import DBConnect
from model.circuiti import Circuito
from model.piazzamenti import Piazzamento


class DAO():
    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from circuits"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select `year`  from races r 
group by `year` """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row['year'])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getNodes():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        query = """select c.* from circuits c 
join races r
on c.circuitId = r.circuitId 
group by circuitId """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Circuito(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getPiazzamenti(a, id):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select r2.driverId, r2.`position`  from results r2 
join races r 
on r.raceId = r2.raceId 
where r.circuitId = %s and year = %s """
        cursor.execute(query, (id, a))

        res = []
        for row in cursor:
            res.append(Piazzamento(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getEdges(s, e):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        query = """select c1, c2, count(distinct d1) as n1, count(distinct d2) as n2 from ((select r2.circuitId as c1, r.driverId as d1, r.`position` as p1
from results r
join races r2 
on r.raceId = r2.raceId 
where r2.`year` >= %s and r2.`year` <= %s and r.`position` is not null
) tab1
join (select r2.circuitId as c2, r.driverId as d2, r.`position` as p2
from results r
join races r2 
on r.raceId = r2.raceId 
where r2.`year` >= %s and r2.`year` <= %s and r.`position` is not null) tab2
on c1 < c2)
where d1 <> d2
group by c1, c2"""
        cursor.execute(query, (s,e,s,e))

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res



