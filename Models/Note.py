from Helpers.Connection import *
import time
import datetime
import json

class Note:
    id: int
    slug: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime
    
    def __init__(self, id, user_id, slug, title, content, created_at, updated_at, deleted_at):
        self.id = id
        self.user_id = user_id
        self.slug = slug
        self.title = title
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
    
    @staticmethod
    def all():
        notes = []
                
        with open('assets/user.json') as file:
            user = json.loads(file.read())
            cursor.execute("SELECT * FROM notes WHERE deleted_at IS NULL AND user_id = %s", (user['id'],))
            result = cursor.fetchall()
            
            if(result):
                for note in result:
                    notes.append(
                        Note(
                            note['id'],
                            note['user_id'],
                            note['slug'],
                            note['title'],
                            note['content'],
                            note['created_at'],
                            note['updated_at'],
                            note['deleted_at'],
                        )
                    )
                
        return notes
    
    @staticmethod
    def save(data: dict):
        if(Note.exists(data['id'])):
            return Note.update(data)
        else:
            return Note.store(data)
            
    @staticmethod
    def delete(unique: str):
        if(Note.exists(unique)):
            Note.destroy(unique)
    
    @staticmethod
    def store(data: dict):
        query = 'INSERT INTO notes (user_id, slug, title, content) VALUES (%s, %s, %s, %s)'
        values = (data['user_id'], data['slug'], data['title'], data['content'])
        
        cursor.execute(query, values)
        connection.commit()
        
        latest = 'SELECT MAX(`id`) AS `id`  FROM notes'
        cursor.execute(latest)
        
        return cursor.fetchone()['id']
    
    @staticmethod
    def update(data: dict):
        query = 'UPDATE notes SET title = %s, slug = %s, content = %s, deleted_at = NULL WHERE id = %s'
        values = (data['title'], data['slug'], data['content'], data['id'])
        
        cursor.execute(query, values)
        connection.commit()
        
        return data['id']
    
    @staticmethod
    def destroy(unique: str):
        query = 'UPDATE notes SET deleted_at = %s WHERE id = %s'
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        values = (timestamp, unique)
        
        cursor.execute(query, values)
        
        return connection.commit()
    
    @staticmethod
    def exists(id: str):
        query = 'SELECT EXISTS (SELECT 1 FROM notes WHERE id = %s) AS `exists`'
        values = (id,)
        
        cursor.execute(query, values)
        
        return cursor.fetchone()['exists']
            
    