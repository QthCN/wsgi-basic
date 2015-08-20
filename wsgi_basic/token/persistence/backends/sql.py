import datetime

from oslo_config import cfg

from wsgi_basic import exception
from wsgi_basic.db.mysql import DB, MYSQL_DATETIME_FMT
from wsgi_basic.token.persistence.core import Driver


CONF = cfg.CONF


class Token(Driver):

    def validate_user(self, username, password):
        with DB() as db:
            db.execute("SELECT * FROM USERS WHERE name='{username}' "
                       "AND password=PASSWORD('{password}')".format(
                username=username,
                password=password
            ))
            data = db.fetchall()
            return len(data) > 0

    def create_token(self, token_id, data):
        if "username" not in data:
            raise exception.NotFound(target="username")
        create_time = datetime.datetime.now()
        expire_time = create_time + datetime.timedelta(
            seconds=CONF.token.expiration
        )

        with DB() as db:
            db.execute("INSERT INTO TOKENS(token_id, username, create_time,"
                       "expire_time) VALUES('{token_id}', '{username}',"
                       "'{create_time}', '{expire_time}')".format(
                token_id=token_id,
                username=data.get("username"),
                create_time=create_time.strftime(MYSQL_DATETIME_FMT),
                expire_time=expire_time.strftime(MYSQL_DATETIME_FMT)
            ))

    def delete_token(self, token_id):
        with DB() as db:
            db.execute("DELETE FROM TOKENS WHERE "
                       "token_id='{token_id}'".format(token_id=token_id))

    def get_token(self, token_id):
        with DB() as db:
            db.execute("SELECT username FROM TOKENS "
                       "WHERE token_id='{token_id}' "
                       "AND expire_time > NOW()".format(token_id=token_id))
            data = db.fetchall()
            if len(data) == 0:
                raise exception.TokenNotFound(token_id=token_id)
            user_info = data[0]
            db.execute("SELECT id, role FROM USERS WHERE "
                       "name='{username}'".format(
                username=user_info["username"]
            ))
            data = db.fetchall()
            user_info["role"] = data[0]["role"]
            user_info["user_id"] = data[0]["id"]
            return user_info

