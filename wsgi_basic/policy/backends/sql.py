from wsgi_basic import exception
from wsgi_basic.db.mysql import DB
from wsgi_basic.policy import Driver


class Policy(Driver):

    def enforce(self, credentials, action, target):
        target_roles_str = ""
        owner_is_ok = False

        with DB() as db:
            db.execute("SELECT action, role, owner FROM POLICIES "
                       "WHERE action='{a}'".format(a=action))
            data = db.fetchall()
            if len(data) == 0:
                raise exception.PolicyNotFound(policy_id=action)
            target_roles_str = data[0]["role"]
            owner_is_ok = (data[0]["owner"] == 1)

        target_roles = target_roles_str.split(":")
        if (credentials.get("role", None) in target_roles or
                (target.get("userid", -1) == credentials.get("userid") and
                 owner_is_ok is True)):
            return True
        raise exception.Unauthorized()
