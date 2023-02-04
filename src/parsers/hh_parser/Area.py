import json

from src.parsers.hh_parser.config import pathHhAreasJSON

class Areas():
    areas = ""
    countries = {}
    regions = {}
    objects = {}

    def __init__(self):

        with open(pathHhAreasJSON, encoding='utf-8', mode='r') as f:
            self.areas = json.loads(f.read())

        self.initialization_areas()

    def filling_countries(self):
        for item in self.areas:
            self.countries[item['id']] = item['name']

    def filling_regions(self):
        for country in self.areas:
            regions_id = []
            for region in country['areas']:
                regions_id.append(region['id'])
            self.regions[country['id']] = regions_id

    def filling_objects(self):
        for country in self.areas:
            for region in country['areas']:
                objects_id = []
                for object in region['areas']:
                    objects_id.append(object['id'])
                self.objects[region['id']] = objects_id

    def initialization_areas(self):
        self.filling_countries()
        self.filling_regions()
        self.filling_objects()

    def get_country_name(self, id):
        region_id = ''
        country_id = ''

        for item in self.objects:
            if id in self.objects[item]:
                region_id = item
                break
        if region_id == '':
            region_id = id

        for item in self.regions:
            if region_id in self.regions[item]:
                country_id = item
                break
        if country_id == '':
            country_id = id

        for item in self.countries:
            if country_id == item:
                return self.countries[item]
        return None