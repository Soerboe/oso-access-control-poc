from oso import Oso, NotFoundError, ForbiddenError

from database import User, Patient, Calendar, database

oso = Oso()
oso.register_class(User)
oso.register_class(Calendar)
oso.register_class(Patient)

oso.load_files(['main.polar'])


def check_permission(user: User, resource, action: str = ''):
    try:
        oso.authorize(user, action, resource)
        print(f'{user.name} is ALLOWED {action} access to {resource}')
    except (NotFoundError, ForbiddenError) as e:
        print(f'{user.name} is DENIED {action} access to {resource}')


if __name__ == '__main__':
    print('RBAC')
    check_permission(database.find_user('Sue'), database.calendars[0], 'read')
    check_permission(database.find_user('Sue'), database.calendars[0], 'write')

    check_permission(database.find_user('Terry'), database.calendars[0], 'read')
    check_permission(database.find_user('Terry'), database.calendars[0], 'write')
    check_permission(database.find_user('Terry'), database.calendars[0], 'delete')

    check_permission(database.find_user('Adam'), database.calendars[0], 'delete')

    print('ABAC')
    check_permission(database.find_user('Terry'), database.find_patient('Perry'))
    check_permission(database.find_user('Terry'), database.find_patient('Ned'))
