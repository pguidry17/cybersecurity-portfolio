from datetime import datetime

def log_event(message: str):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('auth.log', 'a') as logfile:
        logfile.write(f'{timestamp} - {message}\n')


def is_valid_ipv4(ip: str) -> bool:
    parts = ip.split('.')
    if len(parts) != 4:
        return False

    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False

    return True    


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
        violations.append('Password too short')
    if not has_letter:
        violations.append('Password needs a letter')
    if not has_number:
        violations.append('Password needs a number')
    if not has_special:
        violations.append('Password needs a special character')

    return violations



# - - - settings  - - -

USER_MAX_ATTEMPTS = 3          #per-user (session) lockout
IP_MAX_FAILS = 5              # per-IP lockout threshold


# - - - per-IP tracking  - - -
ip_fail_counts = {}           # example: {'10.0.0.5': 2}
blocked_ips = set()           # example: {'10.0.0.66'}


# - - - user context - - -

username = input('username: ').strip()

source_ip = input('Source IP (IPv4): ').strip()
while not is_valid_ipv4(source_ip):
    print('Invalid IPv4 format. Example: 192.168.1.10')
    source_ip = input('Source IP (IPv4): ').strip()

context = f'user={username} ip={source_ip}'    
log_event(f'{context} - SESSION START')


# - - - account lockout simulation (user attempts)- - -

attempts_used = 0
locked_user = False

while not locked_user:
    # Per-IP block check at the start of each attempt
    if source_ip in blocked_ips:
        print(' This IP is BLOCKED due to too many failed attempts.')
        log_event(f'{context} - BLOCKED: IP is blocked')
        break
    
    password = input('Create a password: ')
    violations = check_password_policy(password)

    if not violations:
        print('Password Accepted, Account Setup Complete')
        log_event('Success: Password Accepted')
        break
    
    # Failure Path
    attempts_used +=1
    attempts_left = USER_MAX_ATTEMPTS - attempts_used


    #Update per-IP fail count
    ip_fail_counts[source_ip] = ip_fail_counts.get(source_ip, 0) + 1
    ip_fails = ip_fail_counts[source_ip]
    ip_remaining = IP_MAX_FAILS - ip_fails
    

    print('Password Rejected. Reasons: ')
    for v in violations:
        print('-', v)

    reasons = ';'.join(violations)
    log_event(
        f'{context} - Failed password attempt'
        f'(user_remaining={attempts_left}, ip_fails={ip_fails}) - reasons={reasons}')


    # If IP exceeded threshold, block it

    if ip_fails >= IP_MAX_FAILS:
        blocked_ips.add(source_ip)
        print('Too many failures from this IP. IP is now BLOCKED.')
        log_event(f'{context} - IP BLOCKED after {ip_fails} failed attempts')
        break

    # Otherwise handle user-attempt lockout

    if attempts_left > 0:
        print(f'Attempts Remaining (user): {attempts_left}\n')
        print(f'Failures reamining before IP block: {ip_remaining}\n')
        
    else:
        locked_user = True
        print('Too many failed attempts. User session is now LOCKED')
        log_event(f'{context} - USER LOCKED after {USER_MAX_ATTEMPTS} failed attempts')
