from pyfakefs.fake_filesystem_unittest import TestCase
from arthash.journals import index_files


class IndexFilesTest(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_branch_single(self):
        self.fs.create_file('journals/00')
        actual = '\n'.join(index_files.link_lines('journals'))
        self.assertEqual(actual, SINGLE.strip())

    def test_branch_many(self):
        for i in range(17):
            self.fs.create_file('journals/%02x' % i)
        actual = '\n'.join(index_files.link_lines('journals'))
        self.assertEqual(actual, MANY.strip())

    def test_json_double(self):
        self.fs.create_file('journals/00.json')
        self.fs.create_file('journals/01.json')
        actual = '\n'.join(index_files.link_lines('journals'))
        self.assertEqual(actual, DOUBLE.strip())


SINGLE = """
<table>
    <tr>
        <td><a href="00/index.html"><pre>00</pre></a></td>
    </tr>
</table>
"""

MANY = """
<table>
    <tr>
        <td><a href="00/index.html"><pre>00</pre></a></td>
        <td><a href="01/index.html"><pre>01</pre></a></td>
        <td><a href="02/index.html"><pre>02</pre></a></td>
        <td><a href="03/index.html"><pre>03</pre></a></td>
        <td><a href="04/index.html"><pre>04</pre></a></td>
        <td><a href="05/index.html"><pre>05</pre></a></td>
        <td><a href="06/index.html"><pre>06</pre></a></td>
        <td><a href="07/index.html"><pre>07</pre></a></td>
        <td><a href="08/index.html"><pre>08</pre></a></td>
        <td><a href="09/index.html"><pre>09</pre></a></td>
        <td><a href="0a/index.html"><pre>0a</pre></a></td>
        <td><a href="0b/index.html"><pre>0b</pre></a></td>
        <td><a href="0c/index.html"><pre>0c</pre></a></td>
        <td><a href="0d/index.html"><pre>0d</pre></a></td>
        <td><a href="0e/index.html"><pre>0e</pre></a></td>
        <td><a href="0f/index.html"><pre>0f</pre></a></td>
    </tr>
    <tr>
        <td><a href="10/index.html"><pre>10</pre></a></td>
    </tr>
</table>
"""

DOUBLE = """
<table>
    <tr>
        <td><a href="00.json"><pre>00</pre></a></td>
        <td><a href="01.json"><pre>01</pre></a></td>
    </tr>
</table>
"""
