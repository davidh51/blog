def user_schema(user)-> dict:

    return {'id': str(user['_id']), #str espera nuestro modelo pydantic, y en mongo es un objeto
            'title': str(user['title']),
            'body': str(user['body']),
            'author_name': str(user['author_name']),
            'author_id': str(user['author_id']),
            'created_at': str(user['created_at'])}

def users_schema(users) -> list:
    return [user_schema (user) for user in users]