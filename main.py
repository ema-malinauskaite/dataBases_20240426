import SQLCRUD as sql

#------------------------------------------------------------------------------------------------------
print('  -- Customer names:')

sakilaData = sql.getSQLData('''
    SELECT * FROM sakila.actor 
''')

for i in range(len(sakilaData)):
    if i < 5:
        print(sakilaData[i][1:3])
    if i == 5:
        print('Only first 5 rows printed.')

#------------------------------------------------------------------------------------------------------
print('  -- Number of money spend and movies rented:')

sakilaData = sql.getSQLData('''
    SELECT
        cust.first_name,
        cust.last_name,
        SUM(pay.amount),
        COUNT(inv.film_id)
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
    ORDER BY
    SUM(pay.amount) DESC
''')

for i in range(len(sakilaData)):
    row = list(sakilaData[i])
    row[2] = float(row[2])
    if i < 5:
        print(row)
    if i == 5:
        print('Only first 5 rows printed.')

#------------------------------------------------------------------------------------------------------
print('  -- Number of movies actors played in:')

sakilaData = sql.getSQLData('''
    SELECT 
        actor.first_name,
        actor.last_name,
        COUNT(film.title) AS films_number
    FROM 
        sakila.actor
    JOIN 
        film_actor filmactor ON actor.actor_id = filmactor.actor_id
    JOIN 
        film film ON filmactor.film_id = film.film_id
    GROUP BY 
        actor.actor_id, actor.first_name, actor.last_name
    ORDER BY 
        films_number DESC
''')

for i in range(len(sakilaData)):
    if i < 5:
        print(sakilaData[i])
    if i == 5:
        print('Only first 5 rows printed.')

#------------------------------------------------------------------------------------------------------
print('  -- Number of actors that played in movies:')

sakilaData = sql.getSQLData('''
    SELECT 
        film.title,
        COUNT(filmactor.actor_id) AS actor_number
    FROM 
        sakila.film
    LEFT JOIN 
        film_actor filmactor ON film.film_id = filmactor.film_id
    GROUP BY 
        film.film_id, film.title
    ORDER BY 
        actor_number DESC
''')

for i in range(len(sakilaData)):
    if i < 5:
        print(sakilaData[i])
    if i == 5:
        print('Only first 5 rows printed.')

#------------------------------------------------------------------------------------------------------
print('  -- Number of customers  by store:')

sakilaData = sql.getSQLData('''
    SELECT 
        store.store_id,
        COUNT(cust.customer_id) AS customers
    FROM 
        sakila.store
    JOIN 
        customer cust ON store.store_id = cust.store_id
    GROUP BY 
        store.store_id
    ORDER BY 
        customers DESC
''')

for row in sakilaData:
    print(row)

#------------------------------------------------------------------------------------------------------
print('   -- Number of movies rented by store:')

sakilaData = sql.getSQLData('''
    SELECT 
        store.store_id,
        COUNT(invent.inventory_id) AS films_number
    FROM 
        sakila.store
    JOIN 
        inventory invent ON store.store_id = invent.store_id
    GROUP BY 
        store.store_id
    ORDER BY 
        films_number DESC
''')

for row in sakilaData:
    print(row)


print('  -- Profit by store:')
sakilaData = sql.getSQLData('''
    SELECT 
        store.store_id,
        SUM(pay.amount) AS profit
    FROM 
        sakila.store
    JOIN 
        staff staff ON store.manager_staff_id = staff.staff_id
    JOIN 
        payment pay ON staff.staff_id = pay.staff_id
    GROUP BY 
        store.store_id
    ORDER BY 
        profit DESC
''')

for row in sakilaData:
    row = list(row)
    row[1] = float(row[1])
    print(row)
