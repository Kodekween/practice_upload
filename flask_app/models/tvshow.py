from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Show:
    db_name = 'tvshows'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.network = db_data['network']
        self.release_date = db_data['release_date']
        self.description = db_data['description']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.posted_by = ""
        

    @classmethod
    def save(cls,data):
        query = "INSERT INTO shows (title, network,release_date, description, user_id) VALUES (%(title)s,%(network)s,%(release_date)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_shows = []
        for row in results:
            print(row['release_date'])
            all_shows.append( cls(row) )
        return all_shows
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM shows WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_one_show_with_posted_by(cls, data):   
        query = "SELECT * FROM shows JOIN users ON users.id = user_id WHERE shows.id = %(show_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        show= cls(results[0])
        show.posted_by = results[0]["first_name"]
        return show

    @classmethod
    def update(cls, data):
        query = "UPDATE shows SET title=%(title)s, network=%(network)s, release_date=%(release_date)s, description=%(description)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM shows WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show['title']) < 3:
            is_valid = False
            flash("Must be at least 3 characters","show")
        if len(show['network']) < 3:
            is_valid = False
            flash("Network must be at least 3 characters","show")
        if len(show['release_date']) < 3:
            is_valid = False
            flash("Release must be at least date","show")
        return is_valid
