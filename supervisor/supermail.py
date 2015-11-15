#!/usr/bin/env python -u
##############################################################################
#
# Yoann QUERET - yoann@queret.net
#
##############################################################################

# A event listener meant to be subscribed to PROCESS_STATE_CHANGE
# events.  It will send mail when processes that are children of
# supervisord transition unexpectedly to the XXXXXX state.

# A supervisor config snippet that tells supervisor to use this script
# as a listener is below.
#
# [eventlistener:supermail]
# command=/usr/local/bin/supermail -o hostname -a -m notify-on@domain.com -s '/usr/sbin/sendmail -t -i -f notifier@domain.com'
# events=PROCESS_STATE
#
# Sendmail is used explicitly here so that we can specify the 'from' address.

doc = """\
supermail.py [-p processname] [-a] [-o string] [-m mail_address]
             [-s sendmail] URL

Options:

-p -- specify a supervisor process_name.  Send mail when this process
      transitions to the EXITED state unexpectedly. If this process is
      part of a group, it can be specified using the
      'process_name:group_name' syntax.

-a -- Send mail when any child of the supervisord transitions
      unexpectedly to the EXITED state unexpectedly.  Overrides any -p
      parameters passed in the same supermail process invocation.

-o -- Specify a parameter used as a prefix in the mail subject header.

-s -- the sendmail command to use to send email
      (e.g. "/usr/sbin/sendmail -t -i").  Must be a command which accepts
      header and message data on stdin and sends mail.  Default is
      "/usr/sbin/sendmail -t -i".

-m -- specify an email address.  The script will send mail to this
      address when supermail detects a process super.  If no email
      address is specified, email will not be sent.

The -p option may be specified more than once, allowing for
specification of multiple processes.  Specifying -a overrides any
selection of -p.

A sample invocation:

supermail.py -p program1 -p group1:program2 -m dev@example.com

"""

import os
import sys

from supervisor import childutils

def usage():
	print doc
	sys.exit(255)

class SuperMail:

	def __init__(self, programs, any, email, sendmail, optionalheader):
		self.programs = programs
		self.any = any
		self.email = email
		self.sendmail = sendmail
		self.optionalheader = optionalheader
		self.stdin = sys.stdin
		self.stdout = sys.stdout
		self.stderr = sys.stderr

	def runforever(self, test=False):
		while 1:
			# we explicitly use self.stdin, self.stdout, and self.stderr
			# instead of sys.* so we can unit test this code
			headers, payload = childutils.listener.wait(self.stdin, self.stdout)

			pheaders, pdata = childutils.eventdata(payload+'\n')
			
			#self.stderr.write(headers['eventname'] + '\n')
			#self.stderr.flush()
			
			if headers['eventname'] == 'PROCESS_STATE_UNKNOWN':
                                msg = ('Process %(processname)s in group %(groupname)s UNKNOWN from state %(from_state)s' % pheaders)
                                subject = ' %s UNKNOWN at %s' % (pheaders['processname'], childutils.get_asctime())
#			elif headers['eventname'] == 'PROCESS_STATE_STARTING':
#				msg = ('Process %(processname)s in group %(groupname)s STARTING from state %(from_state)s' % pheaders)
#				subject = ' %s STARTING at %s' % (pheaders['processname'], childutils.get_asctime())
			elif headers['eventname'] == 'PROCESS_STATE_RUNNING':
				msg = ('Process %(processname)s in group %(groupname)s RUNNING (pid %(pid)s) from state %(from_state)s' % pheaders)
				subject = ' %s RUNNING at %s' % (pheaders['processname'], childutils.get_asctime())
			elif headers['eventname'] == 'PROCESS_STATE_BACKOFF':
				msg = ('Process %(processname)s in group %(groupname)s BACKOFF from state %(from_state)s' % pheaders)
				subject = ' %s BACKOFF at %s' % (pheaders['processname'], childutils.get_asctime())
#			elif headers['eventname'] == 'PROCESS_STATE_STOPPING':
#				msg = ('Process %(processname)s in group %(groupname)s STOPPING from state %(from_state)s' % pheaders)
#				subject = ' %s STOPPING at %s' % (pheaders['processname'], childutils.get_asctime())
			elif headers['eventname'] == 'PROCESS_STATE_STOPPED':
				msg = ('Process %(processname)s in group %(groupname)s STOPPED from state %(from_state)s' % pheaders)
				subject = ' %s STOPPED at %s' % (pheaders['processname'], childutils.get_asctime())
			elif headers['eventname'] == 'PROCESS_STATE_EXITED':
				msg = ('Process %(processname)s in group %(groupname)s EXITED unexpectedly (pid %(pid)s) from state %(from_state)s' % pheaders)
				subject = ' %s EXITED at %s' % (pheaders['processname'], childutils.get_asctime())
			elif headers['eventname'] == 'PROCESS_STATE_FATAL':
				msg = ('Process %(processname)s in group %(groupname)s FATAL from state %(from_state)s' % pheaders)
				subject = ' %s FATAL at %s' % (pheaders['processname'], childutils.get_asctime())
			else:
				childutils.listener.ok(self.stdout)
				if test:
					self.stderr.write('non-exited event\n')
					self.stderr.flush()
					break
				continue
		
			if self.optionalheader:
				subject = self.optionalheader + ':' + subject

			self.stderr.write('unexpected exit, mailing\n')
			self.stderr.flush()

			self.mail(self.email, subject, msg)

			childutils.listener.ok(self.stdout)
			
			if test:
				break

	def mail(self, email, subject, msg):
		body =  'To: %s\n' % self.email
		body += 'Subject: %s\n' % subject
		body += '\n'
		body += msg
		m = os.popen(self.sendmail, 'w')
		m.write(body)
		m.close()
		self.stderr.write('Mailed:\n\n%s' % body)
		self.mailed = body

def main(argv=sys.argv):
	import getopt
	short_args="hp:ao:s:m:"
	long_args=[
		"help",
		"program=",
		"any",
		"optionalheader="
		"sendmail_program=",
		"email=",
		]
	arguments = argv[1:]
	try:
		opts, args = getopt.getopt(arguments, short_args, long_args)
	except:
		usage()

	programs = []
	any = False
	sendmail = '/usr/sbin/sendmail -t -i'
	email = None
	optionalheader = None

	for option, value in opts:

		if option in ('-h', '--help'):
			usage()

		if option in ('-p', '--program'):
			programs.append(value)

		if option in ('-a', '--any'):
			any = True

		if option in ('-s', '--sendmail_program'):
			sendmail = value

		if option in ('-m', '--email'):
			email = value

		if option in ('-o', '--optionalheader'):
			optionalheader = value

	#if not 'SUPERVISOR_SERVER_URL' in os.environ:
		#sys.stderr.write('supermail must be run as a supervisor event listener\n')
		#sys.stderr.flush()
		#return

	prog = SuperMail(programs, any, email, sendmail, optionalheader)
	prog.runforever()

if __name__ == '__main__':
	main()
