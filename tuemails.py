#!/usr/bin/env python

import sys
import imaplib
import getpass
import email
import datetime

EMAIL_ADDRESS="YOURADDRESSHERE"
FOLDER='YOURFOLDERHERE'
M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    M.login(EMAIL_ADDRESS, getpass.getpass())
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!! "
    # ... exit or deal with failure...

# Note: This function definition needs to be placed
#       before the previous block of code that calls it.
def process_mailbox(M):
  rv, data = M.search(None, "ALL")
  if rv != 'OK':
      print "No messages found!"
      return

  for num in data[0].split():
      rv, data = M.fetch(num, '(RFC822)')
      if rv != 'OK':
          print "ERROR getting message", num
          return

      msg = email.message_from_string(data[0][1])
      #see representations of an email message: https://docs.python.org/2/library/email.message.html
      #and this Stackoverflow
      for part in msg.walk():
      	typ = part.get_content_type() 
      	if typ and typ.lower() == "text/plain": 
			# Found the first text/plain part 
			print part.get_payload(decode=True)  
      print 'Message %s: %s' % (num, msg['Subject'])



rv, data = M.select(FOLDER)
if rv == 'OK':
    print "Processing mailbox...\n"
    process_mailbox(M) # ... do something with emails, see below ...
    M.close()
M.logout()