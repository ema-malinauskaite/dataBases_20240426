# reikejo terminale paleist kodus:
# pip install mysql.connector
# pip install mysql-connector-python[cext]

import SQLCRUD as sql
#------------------------------------------------------------------------------------------------------
#atvaizduoti visus customerius
print('---task 1---')

results = sql.getSQLData('''
    SELECT * FROM actor 
''')

for i in range(len(results)):
    if i < 5:
        print(results[i][1:3])
    if i == 5:
        print('Only first 5 rows printed.')

#------------------------------------------------------------------------------------------------------
# atvaizduoti visus customerius ir stulpelį kuriame būtų atvaizduota kiek pinigų kiekvienas jų yra išleidęs nuomai, ir kiek filmų nuomavesis
print('---task 2---')
results = getSQLData('''
    SELECT
        cust.first_name,
        cust.last_name,
        SUM(pay.amount),
        COUNT(inv.film_id)'
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

for i in range(len(results)):
    row = list(results[i])
    row[2] = float(row[2])
    if i < 5:
        print(results[i])
    if i == 5:
        print('Only first 5 rows printed.')
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

for i in range(len(results)):
    if i < 5:
        print(results[i])
    if i == 5:
        print('Only first 5 rows printed.')

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

for i in range(len(results)):
    if i < 5:
        print(results[i])
    if i == 5:
        print('Only first 5 rows printed.')
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
