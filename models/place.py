#!/usr/bin/python3
"""Defines the Place class."""
from models.base_model import BaseModel


class Place(BaseModel):
    """
    Represent a place.

    Attributes:
        latitude(float): Latitude location details.
        longitude(float): Longitude location details.
        city_id(str): City id.
        amenity_ids(list): List of Amenities available.
        user_id(str): User id.
        name(str): Name of place.
        description(str): Description about the place.
        number_rooms(int): No. of rooms in the place.
        number_bathrooms(int): No. of bathrooms in the place.
        max_guest(int): Max no. of guests that can be accomodated.
        price_by_night(int): Price per night stay.
    """

    latitude = 0.0
    longitude = 0.0
    city_id = ""
    amenity_ids = []
    user_id = ""
    name = ""
    description = ""
    max_guest = 0
    number_rooms = 0
    number_bathrooms = 0
    price_by_night = 0
