"""
Qualio Technical Assessment - Ben Field - v0.1
"""
import json
from functools import partial

import requests
from haversine import haversine


class DistanceFinder(object):
    """
    DistanceFinder: Determines the distance between two cities stored within
    it's cache.

    Attributes:
        points (dict): A dictionary of cities, sourced from a JSON file.
        home (string): The name of a home city, simplies usage.
    """

    points = {}
    home = "london"

    def set_home(self, city):
        """Set the DistanceFinder's "Home" city. For use with 'home_to_point'
            method.

            Args:
                city (string): The name of the city to used as a starting point
                for distance calculations.
            Raises:
                KeyError: If the specified cannot be found, raise a KeyError
        """

        try:
            lcity = city.lower()
            self.home = self.points.get(lcity) and lcity or None
        except KeyError:
            raise KeyError("Unable to set Home City to {0}"
                           .format(city))

    def point_to_point(self, p_a, p_b, kilometer=True):
        """Attempt to find the great-circle distance between two cities.

        Args:
            a (string): The name of the "Home" city
            b (string): The name of "Destination" city

        Returns: A float representation of the distance between the two
                 specified cities.

        Raises:
            KeyError: If the cities specified cannot be located in the points of
                      interest dict, raise a KeyError

        """
        try:
            point_a = self.points.get(p_a)
            point_b = self.points.get(p_b)

        except KeyError, exc:
            raise KeyError("%s: Unable to locate points" % exc)

        else:
            return haversine((point_a.get('lat'), point_a.get('lon')),
                             (point_b.get('lat'), point_b.get('lon')),
                             miles=(not kilometer))

    def home_to_point(self, target, kilometer=True):
        """Returns the distance between the DistanceFinder instance's Home
        location, and a target city.

        Args:
            target (string): The name of the city of interest.

        Returns: A float of the distance between the two cities.
        """
        return self.point_to_point(self.home, target, kilometer=kilometer)


    def ranged_poi(self, rng, kilometer=True):
        """Returns a list of points of interest sorted alphabetically, within
        the range specified

        Args:
            rng (int):
            km (bool): A boolean parameter that determines whether or not we are
                       measuring distance in KM, or Miles.

        Returns: A list of city names sorted alphabetically that are within the
                 target radius
        """

        try: # Don't just naively accept what we're given. Users make mistakes.
            rng = int(rng)
        except ValueError:
            raise ValueError("Invalid Range Parameter: Please use a number (float, int).")

        in_range = partial(lambda r, x: self.home_to_point(x, kilometer=kilometer) < r, rng)
        #points_in_range = filter(in_range, self.points)
        #return sorted(points_in_range)
        return sorted([i for i in self.points if in_range(i)])

#This would ideally be called a MarathonRunner :D
class DistanceRunner(DistanceFinder):
    """DistanceRunner: This is the base class for interacting with the DistanceFinder.
    It's purpose is to source the list of Cities for processing, and setup the home location.
    """

    def __init__(self, **kwargs):

        try:
            src = kwargs.get("src")
            self.import_poi(src)
        except IOError:
            raise IOError("Unable to load cities from {0}".format(src))

        self.set_home(kwargs.get("home", "dublin"))

    def import_poi(self, src):
        """ Dummy import method. Must populate self.points with data.
        """
        pass


class FileDistanceRunner(DistanceRunner):
    """FileDistanceRunner: This class sources cities from a JSON file from the local filesystem.

    Inherits:
        DistanceRunner
    """

    def import_poi(self, path):
        with open(path) as srcf:
            self.points = json.load(srcf)

class WebDistanceRunner(DistanceRunner):
    """WebDistanceRunner: Sources Cities from a JSON feed using the URL provided.

    Inherits:
        DistanceRunner
    """

    def import_poi(self, url):
        req = requests.get(url)
        self.points = req.json()


if __name__ == "__main__":

    DISTF = WebDistanceRunner(src='https://goo.gl/dE04nJ', home="Dublin")
    print "Cities within 500km of Dublin: \n{0}".format(DISTF.ranged_poi(500))

    #for i in [FileDistanceRunner, WebDistanceRunner]:
    #    df= i(src='res/cities.json', home="Dublin")
    #    print df.ranged_poi(500)
    #    print df.point_to_point("geneva", "shanghai")
