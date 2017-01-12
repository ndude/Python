import paramiko
import time
import yaml

#
# Command("command to run", <options>)
#
# Where options can be:
#	 success="<string>" String to find when command is successful
#	 error="<string>" String to find when command fails
#	 wait=.5 Number of seconds to wait for the command to run
#	 output=False Show the output of the command
class Command(object):
	def __init__(self, cmd=None, success=None, error=None, wait=.5, output=False):
		self.cmd = cmd
		self.success = success
		self.error = error
		self.wait = wait
		self.output = output

	def do(self, connection):
		connection.send(self.cmd+"\n")
		time.sleep(self.wait) # Wait the configurable amount of time
		output = connection.recv(65535)

		# Only show output if turned on
		if self.output == True:
			print output

		if self.error != None and self.error in output:
			return False

		if self.success != None and self.success not in output:
			print "WARNING: Unknown result! Continuing..."

		return True

# Connect and run all of commands on host
def runCommands(host, commands):
	print "Connecting to "+host['addr']+"..."
	remote_conn_pre = paramiko.SSHClient()
	remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	remote_conn_pre.connect(host['addr'], port=22, username=host['user'],
	                        password=host['pass'],
	                        look_for_keys=False, allow_agent=False)

	remote_conn = remote_conn_pre.invoke_shell()
	output = remote_conn.recv(65535)

	for cmd in commands:
	    if cmd.do(remote_conn) == False:
	    	print "Something went wrong, stopping..."
	    	exit(1)
	print "Done on "+host['addr']
	print ""


# Load all the hosts we're connecting to
hosts = []
with open("devices/hosts.yaml", 'r') as stream:
    try:
        hosts = yaml.load(stream)['hosts']
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

# Load all the commands we're running
commands = []
with open("devices/commands.yaml", 'r') as stream:
    try:
        for cmd in yaml.load(stream)['commands']:
        	commands.append(Command(cmd, output=True, wait=3))
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

# Do it!
for host in hosts:
	runCommands(host, commands)
