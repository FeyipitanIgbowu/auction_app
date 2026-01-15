class UserRepository:

    def find_by_id(self, id):
        return User.query.get(id)

    def save(self, user):
        db.session.add(user)
        db.session.commit()

    def delete(self, user):
        db.session.delete(user)
        db.session.commit()