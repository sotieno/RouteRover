#!/usr/bin/env python3
'''
    File location: /core/deliveries/delivery_routes.py
    Declares delivery routes
'''

from core.deliveries import delivery_bp
from flask import jsonify, request, redirect, url_for

# Create delivery location
@delivery_bp.route('/deliveries', methods=['POST'])
def create_delivery():
    '''
    Creates a delivery location from the request body
    '''

    try:
        # Parse JSON data from the request body
        data = request.get_json()

        # Extract delivery details from the JSON data
        name = data['name']
        address = data['address']
        delivery_time = data['delivery_time']
        package_size = data['package_size']
        latitude = data['latitude']
        longitude = data['longitude']

        # Get database connection from the pool
        conn = db_pool.getconn()

        try:
            with conn.cursor() as cursor:
                # Insert new delivery record into the 'deliveries' table
                cursor.execute(
                    """
                    INSERT INTO deliveries (name, address, delivery_time,
                    package_size, latitude, longitude)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (name, address, delivery_time, package_size,
                        latitude, longitude))

                delivery_id = cursor.fetchone()[0]

                # Commit the transaction
                conn.commit()
                return jsonify(
                    message='Delivery created successfully',
                    delivery_id=delivery_id), 201

        except Exception as error:
            # Handle database-related errors
            return jsonify(error=str(error)), 400

    except Exception as error:
        # Handle database-related errors
        return jsonify(error=str(error)), 400

    finally:
        # Return the connection to the pool for reuse
        db_pool.putconn(conn)


# Retrieve delivery locations
@delivery_bp.route('/deliveries', methods=['GET'])
def get_deliveries():
    '''
    Retrieves all delivery locations from the "deliveries" table
    '''

    try:
        # Get database connection from the pool
        conn = db_pool.getconn()

        with conn.cursor() as cursor:
            # Fetch all deliveries from the 'deliveries' table
            cursor.execute("SELECT * FROM deliveries;")
            deliveries = cursor.fetchall()

            # Format the result as a list of dictionaries
            delivery_list = []
            for delivery in deliveries:
                delivery_dict = {
                    'id': delivery[0],
                    'name': delivery[1],
                    'address': delivery[2],
                    'delivery_time': delivery[3].isoformat(),
                    'package_size': delivery[4],
                    'latitude': delivery[5],
                    'longitude': delivery[6]
                }
                delivery_list.append(delivery_dict)

            return jsonify(deliveries=delivery_list)

    except Exception as error:
        # Handle database-related errors
        return jsonify(error=str(error)), 400

    finally:
        # Return the connection to the pool for reuse
        db_pool.putconn(conn)


# Retrieve delivery location by ID
@delivery_bp.route('/deliveries/<int:delivery_id>', methods=['GET'])
def get_delivery(delivery_id):
    '''
    Retrieves delivery locations by ID
    '''

    try:
        # Get database connection from the pool
        conn = db_pool.getconn()

        with conn.cursor() as cursor:
            # Fetch the delivery with the specified ID from
            # the 'deliveries' table
            cursor.execute(
                "SELECT * FROM deliveries WHERE id = %s;", (delivery_id,))
            delivery = cursor.fetchone()

            if delivery:
                delivery_dict = {
                    'id': delivery[0],
                    'name': delivery[1],
                    'address': delivery[2],
                    'delivery_time': delivery[3].isoformat(),
                    'package_size': delivery[4],
                    'latitude': delivery[5],
                    'longitude': delivery[6]
                }
                return jsonify(delivery=delivery_dict)

            return jsonify(message='Delivery not found'), 404

    except Exception as error:
        # Handle database-related errors
        return jsonify(error=str(error)), 400

    finally:
        # Return the connection to the pool for reuse
        db_pool.putconn(conn)


# Update a delivery location
@delivery_bp.route('/deliveries/<int:delivery_id>', methods=['PUT'])
def update_delivery(delivery_id):
    '''
    Updates delivery location details
    '''

    try:
        # Parse JSON data from the request body
        data = request.get_json()

        # Extract updated delivery details from the JSON data
        name = data['name']
        address = data['address']
        delivery_time = data['delivery_time']
        package_size = data['package_size']
        latitude = data['latitude']
        longitude = data['longitude']

        # Get database connection from the pool
        conn = db_pool.getconn()

        with conn.cursor() as cursor:
            # Update the delivery record in the 'deliveries' table
            cursor.execute(
                """UPDATE deliveries SET name=%s, address=%s,
                delivery_time=%s, package_size=%s, latitude=%s,
                longitude=%s WHERE id=%s;""",
                (name, address, delivery_time, package_size, latitude,
                    longitude, delivery_id))

        # Commit the transaction
        conn.commit()

        return jsonify(message='Delivery updated successfully'), 200

    except Exception as error:
        # Handle database-related errors
        return jsonify(error=str(error)), 400

    finally:
        # Return the connection to the pool for reuse
        db_pool.putconn(conn)


# Delete delivery location
@delivery_bp.route('/deliveries/<int:delivery_id>', methods=['DELETE'])
def delete_delivery(delivery_id):
    '''
    Deletes a delivery location no longer in use
    '''

    try:
        # Get database connection from the pool
        conn = db_pool.getconn()

        with conn.cursor() as cursor:
            # Delete the delivery record from the 'deliveries' table
            cursor.execute(
                "DELETE FROM deliveries WHERE id = %s;", (delivery_id,))

        # Commit the transaction
        conn.commit()

        return jsonify(message='Delivery deleted successfully'), 200

    except Exception as error:
        # Handle database-related errors
        return jsonify(error=str(error)), 400

    finally:
        # Return the connection to the pool for reuse
        db_pool.putconn(conn)
