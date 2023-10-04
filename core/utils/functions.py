#!/usr/bin/env python3
'''
    File location: /core/utils/functions.py
    Declares application functions
'''
import os
import re
import math
import logging
import folium
import requests
import psycopg2
import osmnx as ox
import networkx as nx
from flask.json import dumps
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from shapely.wkt import dumps
from shapely.geometry import Point
from core.extensions import db_params


url = "https://valhalla1.openstreetmap.de/route"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "insomnia/8.1.0"
}

# Checks for a valid email address
def is_valid_email(email):
    # Regular expression for email validation (covers most common cases)
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check is email is valid and is less than 320 characters
    if re.search(email_regex, email) and len(email) <= 320:
        return True
    else:
        return False


# Checks if password meets criteria
def is_valid_password(password):
    # Password criteria constants
    MIN_LENGTH = 8
    HAS_UPPERCASE = lambda s: any(char.isupper() for char in s)
    HAS_LOWERCASE = lambda s: any(char.islower() for char in s)
    HAS_DIGIT = lambda s: any(char.isdigit() for char in s)
    HAS_SPECIAL = lambda s: any(char in "!@#$%^&*()_-+=<>?/[]{}|" for char in s)

    # Check each password criterion
    return (
        len(password) >= MIN_LENGTH and
        HAS_UPPERCASE(password) and
        HAS_LOWERCASE(password) and
        HAS_DIGIT(password) and
        HAS_SPECIAL(password)
    )


# Displays password requirements
def get_password_requirements():
    # Define the password requirements and return as a string
    requirements = [
        "At least 8 characters",
        "At least one uppercase letter",
        "At least one lowercase letter",
        "At least one digit",
        "At least one special character (!@#$%^&*()_-+=<>?/[]{}|)",
    ]

    return ", ".join(requirements)


# Get database connection
def establish_database_connection(db_params):
    try:
        return psycopg2.connect(**db_params)
    except psycopg2.Error as error:
        logging.error(f"Error connecting to the database: {error}")
        raise ConnectionError(f"Error connecting to the database: {error}")


# Find the nearest node
def find_nearest_node(cursor, geom_point, table_name='ken_2po_4pgr'):
    cursor.execute("""
        SELECT id, ST_AsText(geom_way)
        FROM {0}
        ORDER BY geom_way <-> ST_SetSRID(ST_GeomFromText(%s), 4326)
        LIMIT 1;
    """.format(table_name), (dumps(geom_point),))
    return cursor.fetchone()


# Clean up route text
def clean_route_text(route_text):
    route_text = route_text.replace("MULTILINESTRING", "")
    route_text = route_text.replace("((", "")
    route_text = route_text.replace("))", "")
    route_text = route_text.replace("(", "")
    route_text = route_text.replace(")", "")
    route_text = route_text.replace(")(", ",")
    return route_text


# Calculate the nearest network nodes for start and end points
def calculate_nearest_nodes(G, start_point_geom, end_point_geom):
    nearest_start_node = None
    nearest_end_node = None
    min_start_distance = float('inf')
    min_end_distance = float('inf')

    for node in G.nodes():
        node_coords = (G.nodes[node]['y'], G.nodes[node]['x'])

        # Calculate distance from start and end points to the current node using geodesic
        start_distance = geodesic((start_point_geom.x, start_point_geom.y), node_coords).kilometers
        end_distance = geodesic((end_point_geom.x, end_point_geom.y), node_coords).kilometers

        # Update nearest nodes if a closer node is found
        if start_distance < min_start_distance:
            nearest_start_node = node
            min_start_distance = start_distance

        if end_distance < min_end_distance:
            nearest_end_node = node
            min_end_distance = end_distance

    return nearest_start_node, nearest_end_node


# Function to calculate shortest route
def calculate_shortest_route(start_point_geom, end_point_geom, mode_of_travel):
    """
    Calculates the route between two points.
    """

    # Define coordinate list
    latlon = [(start_point_geom.y, start_point_geom.x), (end_point_geom.y, end_point_geom.x)]

    # Define region of interest
    place_name = "Nairobi, Kenya"

    # Define weight
    optimizer = 'time'

    # Download OSM data for region of interest
    graph = ox.graph_from_place(
        place_name, network_type=mode_of_travel)

    # Create a NetworkX graph
    G = nx.Graph(graph)

    # Calculate the nearest nodes
    nearest_start_node, nearest_end_node = calculate_nearest_nodes(G, start_point_geom, end_point_geom)

    # Find the shortest route
    shortest_route = nx.shortest_path(
        G, source=nearest_start_node, target=nearest_end_node,
        weight=optimizer, method='bellman-ford')

    if shortest_route != []:
        # Create a Folium map centered around the start location
        map_center = [start_point_geom.x, start_point_geom.y]
        shortest_route_map = folium.Map(
            location=map_center, zoom_start=14)

        # Create markers for start and end locations
        start_marker = folium.Marker(
            [start_point_geom.x, start_point_geom.y], tooltip="Start")
        end_marker = folium.Marker(
            [end_point_geom.x, end_point_geom.y], tooltip="End")

        # Add markers to the map
        start_marker.add_to(shortest_route_map)
        end_marker.add_to(shortest_route_map)

        payload = {
            "locations": [
                {
                    "lat": latlon[0][1],
                    "lon": latlon[0][0]
                },
                {
                    "lat": latlon[1][1],
                    "lon": latlon[1][0]
                }
            ],
            "costing": "auto"
        }

        # Send an HTTP GET request to the routing service then parse the
        # response as JSON and store it in the 'response' variable.
        response = requests.get('https://valhalla1.openstreetmap.de/route', json=payload, headers=headers).json()

        # Decode the coordinates of the route obtained in the JSON response.
        route = [ list(reversed(point)) for point in decode(response['trip']['legs'][0]['shape'])]

        # Extract maneuver instructions for the route from the JSON response.
        instructions = [maneuvers['instruction'] for maneuvers in response['trip']['legs'][0]['maneuvers']]

        # Add the polyline to the map
        folium.PolyLine(route,
                        color='blue',
                        weight=5,
                        opacity=0.6).add_to(shortest_route_map)

        shortest_route_map.fit_bounds(shortest_route_map.get_bounds())

        # Get the current directory
        script_dir = os.path.dirname(__file__)

        # Specify the file name (e.g., 'shortest_path_map.html')
        file_name = 'shortest_route_map.html'

        # Save the map to the specified directory
        shortest_route_map.save(os.path.join(
            script_dir, '..', 'templates', file_name))

        return 'shortest_route_map.html'
    else:
        # Return empty list if no path is found
        return []


# Function to return address geocode
def geocode_address(address):
    '''
        Returns address geocoding
    '''
    geolocator = Nominatim(user_agent="RouteRover")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None


# Function to decode an encoded set of geocoordinates
def decode(encoded):
    # Define the inverse scaling factor for precision (1 divided by 1e6)
    inv = 1.0 / 1e6

    # Initialize an empty list to store decoded coordinates
    decoded = []

    # Initialize the previous coordinate values
    previous = [0, 0]

    # Initialize the index for iterating through the encoded data
    i = 0

    # Iterate through each byte in the encoded data
    while i < len(encoded):
        # Initialize a list to store longitude and latitude values
        ll = [0, 0]

        # Iterate for longitude (index 0) and latitude (index 1)
        for j in [0, 1]:
            shift = 0
            byte = 0x20

            # Continue decoding bytes until a complete coordinate is obtained
            while byte >= 0x20:
                # Decode the current byte
                byte = ord(encoded[i]) - 63
                i += 1

                # Extract and store coordinate bits
                ll[j] |= (byte & 0x1f) << shift
                shift += 5

            # Calculate the final value by adding the previous offset
            # and remember it for the next coordinate
            if ll[j] & 1:
                ll[j] = previous[j] + (~(ll[j] >> 1))
            else:
                ll[j] = previous[j] + (ll[j] >> 1)

            # Update the previous coordinate value for the next iteration
            previous[j] = ll[j]

        # Scale the coordinates by the precision factor and format as lon, lat
        decoded.append([float('%.6f' % (ll[1] * inv)), float('%.6f' % (ll[0] * inv))])

    # Return the list of decoded coordinates
    return decoded
