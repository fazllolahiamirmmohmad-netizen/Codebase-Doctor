def get_user(user_id, name, age, email, role, status, country):
    users = {
        1: "Ali",
        2: "Sara",
    }
    return users.get(user_id)