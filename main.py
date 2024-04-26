# reikejo terminale paleist kodus:
# pip install mysql.connector
# pip install mysql-connector-python[cext]

import mysql.connector

hostname = "localhost"
username = "root"
password = "pipiriukaS56"
database = "sakila"
portAddress = 3317

connection = None
cursor = None

def getSQLData(SQLquery):
    try:
        connection = mysql.connector.connect(host=hostname, port=portAddress, user=username, password=password, database=database)
        #print("Connection successful!")

        cursor = connection.cursor()
        query = SQLquery
        cursor.execute(query)
        results = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Connection error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    #print("Connection closed.")
    return results

#------------------------------------------------------------------------------------------------------
#atvaizduoti visus customerius
print('---uzd1---')

results = getSQLData('''
    SELECT * FROM actor 
''')

names = []
for row in results:
    names.append(row[1]+' '+row[2])
print(names)

#------------------------------------------------------------------------------------------------------
# atvaizduoti visus customerius ir stulpelį kuriame būtų atvaizduota kiek pinigų kiekvienas jų yra išleidęs nuomai, ir kiek filmų nuomavesis
print('---uzd2---')
results = getSQLData('''
    SELECT
        cust.first_name AS 'customerFirstName',
        cust.last_name AS 'customerLastName',
        SUM(pay.amount) AS 'amountSpent',
        COUNT(inv.film_id) AS 'filmCount'
    FROM
        sakila.customer cust
            JOIN
        sakila.payment pay ON cust.customer_id = pay.customer_id
            JOIN
        sakila.rental rent ON pay.rental_id = rent.rental_id
            JOIN
        sakila.inventory inv ON rent.inventory_id = inv.inventory_id
    GROUP BY
    cust.first_name,
    cust.last_name
''')

for row in results:
    row = list(row)
    row[2] = float(row[2])
    print(row)
#------------------------------------------------------------------------------------------------------
# atvaizduoti aktorius ir keliuose filmuose jie yra filmavesi
print('---uzd3---')
results = getSQLData('''
    SELECT 
        actor.actor_id,
        actor.first_name,
        actor.last_name,
        COUNT(film.title) AS films_number
    FROM 
        actor actor
    JOIN 
        film_actor filmactor ON actor.actor_id = filmactor.actor_id
    JOIN 
        film film ON filmactor.film_id = film.film_id
    GROUP BY 
        actor.actor_id, actor.first_name, actor.last_name
    ORDER BY 
        actor.actor_id
''')

for row in results:
    print(row)

#------------------------------------------------------------------------------------------------------
# atvaizduoti visus filmus ir kiek aktorių juose vaidino
print('---uzd4---')
results = getSQLData('''
SELECT 
        film.film_id,
        film.title,
        COUNT(filmactor.actor_id) AS aktoriu_kiekis
    FROM 
        film film
    LEFT JOIN 
        film_actor filmactor ON film.film_id = filmactor.film_id
    GROUP BY 
        film.film_id, film.title
    ORDER BY 
        film.film_id
        ''')

for row in results:
    print(row)
#------------------------------------------------------------------------------------------------------
# su pitono pagalba: nustatyti kuris nuomos punktas:
#--turi daugiau customerių
print('---uzd5---')
results = getSQLData('''
SELECT 
        store.store_id,
        COUNT(cust.customer_id) AS nuomininkai
    FROM 
        store store
    JOIN 
        customer cust ON store.store_id = cust.store_id
    GROUP BY 
        store.store_id
    ORDER BY 
        nuomininkai DESC
        ''')

for row in results:
    print(row)

#--išnuomavo daugiau(ir kiek kiekvienas) filmų
print('---uzd6---')
results = getSQLData('''
  SELECT 
        store.store_id,
        COUNT(invent.inventory_id) AS filmuSkaicius
    FROM 
        store store
    JOIN 
        inventory invent ON store.store_id = invent.store_id
    GROUP BY 
        store.store_id
    ORDER BY 
        filmuSkaicius DESC
        ''')

for row in results:
    print(row)

#--kiek sugeneravo pajamų
print('---uzd6---')
results = getSQLData('''
 SELECT 
        store.store_id,
        SUM(pay.amount) AS pelnas
    FROM 
        store store
    JOIN 
        staff staff ON store.manager_staff_id = staff.staff_id
    JOIN 
        payment pay ON staff.staff_id = pay.staff_id
    GROUP BY 
        store.store_id
    ORDER BY 
        pelnas DESC
        ''')

for row in results:
    row = list(row)
    row[1] = float(row[1])
    print(row)