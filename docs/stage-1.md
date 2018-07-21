## Deliverable for stage 1.

# Install

`pip install` should get the user:

* the artHash library installed
* a command line program `artHashD` that runs the server
* a command line program called `artHashEr` that runs the client

# Demo:

1. Open a terminal window
2. Run `artHashD` in it
3. Open a new terminal window
4. Run `artHashEr <your-file-name>` which does the following:
  1. Generate the public/private keys (ppkeys) and a hash.
  2. Sign the artHash with the private key to get the artHash signature.
  3. Contact the `artHashD` running on your machine and make a journal
  entry.
  4. Receive back the `timestamp`, `recordHash` and `journalURL`.
  5. Write a JSON file containing those values and the privateKey to the terminal
  6. open the journal page in the browser

# Integration tests

Automated tests that actually start a server, then run the client repeatedly
against that server, then interrogate the server's state when it is all done.
