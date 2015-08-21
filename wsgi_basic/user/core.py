from wsgi_basic import exception
from wsgi_basic.common import dependency
from wsgi_basic.db.mysql import DB


@dependency.provider("user_api")
class Manager(object):

    def create_user(self, username, password, role):
        with DB() as db:
            db.execute("LOCK TABLES USERS WRITE")
            db.execute("SELECT name FROM USERS WHERE name='{n}'".format(
                n=username
            ))
            data = db.fetchall()
            if len(data) > 0:
                db.execute("UNLOCK TABLES")
                raise exception.UserAlreadyExist(name=username)
            else:
                db.execute("INSERT INTO USERS(name, password, role) "
                           "VALUES('{n}', PASSWORD('{p}'), "
                           "'{r}')".format(n=username, p=password,
                                            r=role))
                db.execute("UNLOCK TABLES")
                db.execute("SELECT id, name, role FROM "
                           "USERS WHERE name='{n}'".format(
                    n=username
                ))
                data = db.fetchall()
                return dict(user_id=data[0]["id"],
                            name=data[0]["name"],
                            role=data[0]["role"])

    def delete_user(self, user_id):
        with DB() as db:
            db.execute("DELETE FROM USERS WHERE id={i}".format(i=user_id))

    def update_user(self, user_id, password):
        with DB() as db:
            db.execute("UPDATE USERS SET password=PASSWORD('{p}') "
                       "WHERE id={id}".format(p=password,
                                              id=user_id))
            # TODO(tianhuan) User may be delete by others
            db.execute("SELECT id, name, role FROM "
                       "USERS WHERE id={i}".format(
                i=user_id
            ))
            data = db.fetchall()
            return dict(user_id=data[0]["id"],
                        name=data[0]["name"],
                        role=data[0]["role"])

    def get_user(self, user_id):
        with DB() as db:
            db.execute("SELECT id, name, role FROM "
                       "USERS WHERE id={i}".format(
                i=user_id
            ))
            data = db.fetchall()
            if len(data) == 0:
                raise exception.UserNotFound(user_id=user_id)
            return dict(user_id=data[0]["id"],
                        name=data[0]["name"],
                        role=data[0]["role"])

    def get_users(self):
        with DB() as db:
            db.execute("SELECT id, name, role FROM USERS")
            data = db.fetchall()
            users = list()
            for d in data:
                users.append(
                    dict(user_id=d["id"],
                         name=d["name"],
                         role=d["role"])
                )
            return users
