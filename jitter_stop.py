import paramiko

ssh = paramiko.SSHClient()
key = paramiko.AutoAddPolicy()
ssh.set_missing_host_key_policy(key)
ssh.connect('10.0.0.1',22,'xiaokun', '063059',timeout=5)

ssh.exec_command('sudo tc qdisc del dev eth0 root')
ssh.exec_command('sudo tc qdisc del dev eth1 root')
ssh.close()