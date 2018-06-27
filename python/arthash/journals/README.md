We want to potentially store a trillion hashes but we don't want too many files
in any directory.

    one trillion = 10**12 = (10**2) ** 6 = (10**3) ** 4

or `(2 ** 10) ** 4 = 2 ** 40 = (2 ** 8) ** 5`

So the hashes go into:

    arthash.org/hashes/00/00/00/00.json
    arthash.org/hashes/00/00/00/01.json
    ...
    arthash.org/hashes/00/00/00/ff.json
    arthash.org/hashes/00/00/01/00.json
    arthash.org/hashes/00/00/01/01.json

Each file has 256 hashes, so the total number is:

    (256 * 256 * 256)  *    256    *      256
       directories    files/directory   hashes/file

or 1099511627776.

Now, if we actually put 256 ** 4 or 4 gig files on a filesystem there would be
trouble, but long before we got to that point, we'd have some virtual filesystem
in place which would do the trick.

If we ever get over a trillion hashes, we can easily extend the length of the
top-level directory names indefinitely - there would be a little special purpose
code for backward compatibility but `hex(dirname)` would still work perfectly
well.
