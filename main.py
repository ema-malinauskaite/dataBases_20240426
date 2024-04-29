import functions
import yaml

print('eCustomer names:')
sakilaData = functions.getSQLData('''
    SELECT first_name, last_name FROM sakila.actor 
''')
functions.print5Rows(sakilaData)

print('\nNumber of money spend and movies rented:')
sakilaData = functions.getSQLData('''
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
sakilaData = functions.changeToFloat(sakilaData, 2)
functions.print5Rows(sakilaData)

print('\nNumber of movies actors played in:')
sakilaData = functions.getSQLData('''
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
functions.print5Rows(sakilaData)

print('\nNumber of actors that played in movies:')
sakilaData = functions.getSQLData('''
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
functions.print5Rows(sakilaData)

print('\n Information on stores:')

print('Number of customers  by store:')
sakilaData = functions.getSQLData('SELECT store_id, customer_id FROM sakila.customer')
customersByStore = functions.sumBy(sakilaData, 0)
print(yaml.dump(customersByStore, default_flow_style=False))

print('Number of movies rented by store:')
sakilaData = functions.getSQLData('SELECT staff_id, rental_id FROM sakila.rental')
moviesByStore = functions.sumBy(sakilaData, 0)
print(yaml.dump(moviesByStore, default_flow_style=False))

print('Profit by store:')
sakilaData = functions.getSQLData('SELECT staff_id, amount FROM sakila.payment')
sakilaData = functions.changeToFloat(sakilaData, 1)
profitByStore = functions.sumBy(sakilaData, 0, addValueFromIndex=1, count=False)
print(yaml.dump(profitByStore, default_flow_style=False))

