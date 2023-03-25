from Helpers.Connection import *
import time
import datetime

class Note:
    id: int
    slug: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime
    
    def __init__(self, id, slug, title, content, created_at, updated_at, deleted_at):
        self.id = id
        self.slug = slug
        self.title = title
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
    
    @staticmethod
    def all():
        cursor.execute("SELECT * FROM notes WHERE deleted_at IS NULL")
        result = cursor.fetchall()
        notes = []
        
        if(result):
            for note in result:
                notes.append(
                    Note(
                        note['id'],
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
        if(Note.exists(data['slug'])):
            Note.update(data)
        else:
            Note.store(data)
            
    @staticmethod
    def delete(unique: str):
        if(Note.exists(unique)):
            Note.destroy(unique)
    
    @staticmethod
    def store(data: dict):
        query = 'INSERT INTO notes (slug, title, content) VALUES (%s, %s, %s)'
        values = (data['slug'], data['title'], data['content'])
        
        cursor.execute(query, values)
        return connection.commit()
    
    @staticmethod
    def update(data: dict):
        query = 'UPDATE notes SET title = %s, content = %s, deleted_at = NULL WHERE slug = %s'
        values = (data['title'], data['content'], data['slug'])
        
        cursor.execute(query, values)
        return connection.commit()
    
    @staticmethod
    def destroy(unique: str):
        query = 'UPDATE notes SET deleted_at = %s WHERE slug = %s'
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        values = (timestamp, unique)
        
        cursor.execute(query, values)
        return connection.commit()
    
    @staticmethod
    def exists(unique: str):
        query = 'SELECT EXISTS (SELECT 1 FROM notes WHERE slug = %s) AS `exists`'
        values = (unique,)
        
        cursor.execute(query, values)
        return cursor.fetchone()['exists']
            
    