from fabric import Connection
result = Connection('169.254.82.80').run('whoami', hide=True)
msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
print(msg.format(result))