from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
# the regex
import re	
# create a regular expression object that we'll use later   


class Medications:
    schema = "medpass"
    table = "medication"

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.instructions = data['instructions']
        self.side_effects = data['side_effects']
        self.given_date = data['given_date']
        self.expiration_date = data['expiration_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posted_by = ['']

# this method is not a normal query for table in most use cases
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM medication;"
        results = connectToMySQL(cls.schema).query_db(query)
        # print(results)
        medication = []
        for row in results:
            medication.append(cls(row))
        return medication


#pulls medication by ID
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM medication WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        return cls(results[0])

#pulls medication info by 
    @classmethod
    def get_by_side_effects(cls, data):
        query = "SELECT * FROM medication WHERE side_effects = %(side_effects)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    

#creates new medication
    @classmethod
    def create(cls, data):
        query = """INSERT INTO medication(user_id,instructions, expiration_date, side_effects, given_date, created_at, updated_at)
        VALUES (%(user_id)s, %(instructions)s, %(expiration_date)s, %(side_effects)s, %(given_date)s, NOW(), NOW());"""
        return connectToMySQL(cls.schema).query_db(query, data)

    @classmethod
    def update_one(cls, data):
        query = "UPDATE medication SET instructions = %(instructions)s, side_effects = %(side_effects)s, given_date = %(given_date)s, expiration_date = %(expiration_date)s, updated_at = NOW() WHERE id = %(id)s;"
        connectToMySQL(cls.schema).query_db(query, data)


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM medication WHERE id = %(id)s;"
        connectToMySQL(cls.schema).query_db(query, data)

    @staticmethod
    def medication_validate(post_data):
        is_valid = True
#confirms 
        if not post_data['instructions']:
            flash('instructions is required', 'instructions')
            is_valid = False
        elif len(post_data['instructions']) < 2:
            flash('instructions must be at least 2 characters', 'instructions')
            is_valid = False

        if not post_data['side_effects']:
            flash('side_effects is required', 'side_effects')
            is_valid = False
        elif len(post_data['side_effects']) < 1:
            flash('side_effects must be at least 3 characters', 'side_effects')
            is_valid = False

        if not post_data['expiration_date']:
            flash('expiration_date is required', 'expiration_date')
            is_valid = False
        elif len(post_data['expiration_date']) < 3:
            flash('expiration_date must be at least 3 characters', 'expiration_date')
            is_valid = False
            
        return is_valid
        

