#!/usr/bin/env python3
'''
    File location: /core/optimization/get_routes.py
    Shortest path route declarations
'''

import folium
from flask import jsonify, request, render_template, redirect, url_for, flash
from flask_login import login_required
from core.optimization import get_route_bp
from core.utils.functions import calculate_shortest_route, geocode_address
from shapely.geometry import Point


# Get start point and destination
@get_route_bp.route('/get-route')
@login_required
def get_route_form():
    return render_template('route.html')


@get_route_bp.route('/get-route', methods=['POST'])
@login_required
def get_route():
    try:
        # Parse starting and ending points from the request
        start_point_coords = request.form.get("start_point_coords")
        end_point_coords = request.form.get("end_point_coords")
        mode_of_travel = request.form.get("mode_of_travel").lower()

        # Check if start_point and end_point are empty strings
        if not start_point_coords.strip() or not end_point_coords.strip() or not mode_of_travel.strip():
            flash('Start, end points and mode cannot be empty')
            return redirect(url_for('route.get_route_form'))

        # Geocode the start and end points
        start_location = tuple(reversed(geocode_address(start_point_coords)))
        end_location = tuple(reversed(geocode_address(end_point_coords)))

        # Ensure that the geocoded points are in SRID 4326
        start_point_geom = Point(start_location[1], start_location[0])  # Assuming the tuple has (latitude, longitude) order
        end_point_geom = Point(end_location[1], end_location[0])  # Assuming the tuple has (latitude, longitude) order

        if start_point_geom.is_valid and end_point_geom.is_valid:
            # Execute Dijkstra's algorithm using pgrouting
            map_file = calculate_shortest_route(
                start_point_geom, end_point_geom, mode_of_travel=mode_of_travel)

            if map_file != "":
                # Render HTML template
                # , folium_route=folium_route)
                return render_template(map_file)
            else:
                flash('No route found.')
                return redirect(url_for('route.get_route_form'))
        else:
            flash('Please enter a valid start point and destination.')
            return redirect(url_for('route.get_route_form'))

    except Exception as e:
        # Handle exceptions and errors gracefully
        flash(f'Error: {str(e)}')
        return jsonify({'error': str(e)})
