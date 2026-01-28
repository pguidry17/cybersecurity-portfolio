def check_password_policy(password: str) -> list[str]:
    'Return a list of policy violations. Empty list means the password passed.'
    has_letter = False
    has_number = False
    has_special = False

    special_chars = '!@#$%^&*'

    for ch in password:
        if ch.isalpha():
            has_letter = True
        elif ch.isdigit():
            has_number = True
        elif ch in special_chars:
            has_special = True

    violations = []

    if len(password) < 8:
        violations.append('Password Rejected; Too short')
    if not has_letter:
        violations.append('Password Rejected; Needs a letter')
    if not has_number:
        violations.append('Password Rejected; Needs a number')
    if not has_special:
        violations.append('Password Rejected; Needs a special character')

    return violations


# - - - - main program - - - -

for attempt in range(3):
    password = input(f' Attempt{attempt + 1}: Enter a password: ')

    violations = check_password_policy(password)

    if not violations:
        print('Password Accepted. ')
        break
    else:
        print(f' Rejected: {", ".join(violations)}')
else:
    print(' Too many failed attempts. Access denied.' )
