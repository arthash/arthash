## Deliverables

There are two:

* a server named `artHashD`
* a client named `artHashEr`

## `artHashD`

The `artHashD` server is a *nix daemon written in Python with a little bit of
`bash` glue code.

The `artHashD` server provides just one service: _arthash journaling_.

`artHashD` is sent a hash by a client, writes that hash into a JSON file that's
called a _journal_, and sends back the URL of the journal page.

As a side effect, the server requests that archive.org archives the journal
page - this must be performed in a separate thread and rate limited.

## `artHashEr`

 The `artHashEr` client is a cross-platform command line application written in
Python. On some platforms like MacOS there will also be a drag-and-drop
front-end.

The `artHashEr` client provides two services: _arthashing_,
and _arthash certificate verification_.

## Arthashing

Calling `artHashEr` with a single file or directory (either from the command
line, or through drag-and-drop) _arthashes_ that file or directory:

1. Arthashing starts by generating a public/private key pair.

2. Then it produces the hash digest: starting with an empty hash, it then hashes
a sequence of file names and file contents into it to get a final _arthash_, 64
hex digits from 0-9, a-f.

2. The arthash is then sent anonymously to an `artHashD` server, which responds
with a journal URL.

3. The `artHashEr` client takes the arthash, the journal URL and loads the
_certificate generator page_ in a browser.

4. The _certificate generator page_ is prefilled with the arthash and journal
URL , and possibly metadata extracted from the original file or directory.
The generator page is stored local to the client so no personally identifiable
data ever leaves the local machine.

5. The user fills out the certificate generator page and presses submit, leading
to the _arthash certificate page_, an HTML page with enough information to
legally establish copyright. The arthash certificate page is be saved to disk as
the arthash certificate file.

6. The user can choose to keep that saved arthash certificate secret and reveal
it at the appropriate moment,  publish the certificate somewhere else, or keep
it a secret forever.


## Arthash certificate verification

Calling `artHashEr` with two files or directories (either from the command
line, or through drag-and-drop) performs arthash certificate verification.

Exactly one of the two files or directories must be an arthash certificate file.

The arthash of the other item is computed, and compared with the certificate
file for verification.  In addition, the journal URL in the certificate is
verified to see that it contains the arthash.
