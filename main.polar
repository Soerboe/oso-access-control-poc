actor User {}

resource Calendar {
    permissions = ["read", "write", "delete"];
    roles = ["CalendarReader", "CalendarWriter", "Admin"];

    "read" if "CalendarReader";

    "write" if "CalendarWriter";
    "CalendarReader" if "CalendarWriter";

    "delete" if "Admin";
    "CalendarWriter" if "Admin";
}

has_role(actor: User, role_name: String, _: Calendar) if
    role in actor.roles and
    role_name = role.name;

allow(actor, action, resource) if
    has_permission(actor, action, resource);

allow(user: User, _role_name: String, patient: Patient) if
    user in patient.therapists;