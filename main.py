from model.main_db.admin import Admin
if __name__ == '__main__':
    admin_one = Admin(telegram_id = 1)
    print(admin_one.telegram_id)
    print(repr(admin_one))

