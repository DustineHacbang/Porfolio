from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
# the regex
import re	
# create a regular expression object that we'll use later   


class Sightings:
    schema = "saquaches"
    table = "reports"

    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.num_saquaches = data['num_saquaches']
        self.sighting_date = data['sighting_date']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posted_by = ['']

# this method is not a normal query for table in most use cases
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM reports;"
        results = connectToMySQL(cls.schema).query_db(query)
        # print(results)
        reports = []
        for row in results:
            reports.append(cls(row))
        return reports


#pulls reports by ID
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM reports WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        return cls(results[0])

#pulls reports info by 
    @classmethod
    def get_by_num_saquaches(cls, data):
        query = "SELECT * FROM reports WHERE num_saquaches = %(num_saquaches)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    

#creates new reports
    @classmethod
    def create(cls, data):
        query = """INSERT INTO reports(user_id,location, what_happened, num_saquaches, sighting_date, created_at, updated_at)
        VALUES (%(user_id)s, %(location)s, %(what_happened)s, %(num_saquaches)s, %(sighting_date)s, NOW(), NOW());"""
        return connectToMySQL(cls.schema).query_db(query, data)

    @classmethod
    def update_one(cls, data):
        query = "UPDATE reports SET location = %(location)s, num_saquaches = %(num_saquaches)s, sighting_date = %(sighting_date)s, what_happened = %(what_happened)s, updated_at = NOW() WHERE id = %(id)s;"
        connectToMySQL(cls.schema).query_db(query, data)


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM reports WHERE id = %(id)s;"
        connectToMySQL(cls.schema).query_db(query, data)

    @staticmethod
    def sighting_validate(post_data):
        is_valid = True
#confirms 
        if not post_data['location']:
            flash('location is required', 'location')
            is_valid = False
        elif len(post_data['location']) < 2:
            flash('location must be at least 2 characters', 'location')
            is_valid = False

        if not post_data['num_saquaches']:
            flash('num_saquaches is required', 'num_saquaches')
            is_valid = False
        elif len(post_data['num_saquaches']) < 1:
            flash('num_saquaches must be at least 3 characters', 'num_saquaches')
            is_valid = False

        if not post_data['what_happened']:
            flash('what_happened is required', 'what_happened')
            is_valid = False
        elif len(post_data['what_happened']) < 3:
            flash('what_happened must be at least 3 characters', 'what_happened')
            is_valid = False
            
        return is_valid
        

