def update_users(db_document, users, origin):
    for user in users:
        pk = user['pk']
        user['origin'] = origin
        db_document.find_one_and_update(
                {'pk': pk}, {'$set': user}, upsert=True
        )
