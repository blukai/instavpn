![img](http://i.imgur.com/67dwCdA.png)
========

### Requirements
* Ubuntu 14.04
* 512 MB RAM

### Install
```bash
curl -sS https://raw.githubusercontent.com/sockeye44/instavpn/master/instavpn.sh | sudo bash
```

### CLI
```bash
instavpn list                           # Show all credentials
instavpn stat                           # Show bandwidth statistics
instavpn psk get                        # Get pre-shared key
instavpn psk set <psk>                  # Set pre-shared key
instavpn user get <username>            # Get password
instavpn user set <username> <password> # Set password or create user if not exists
instavpn user delete <username>         # Delete user
instavpn user list                      # List all users
instavpn web mode [on|off]              # Turn on/off web UI
instavpn web set <username> <password>  # Set username/password for web UI
```
