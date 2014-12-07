"""Assignment 3: Files and Streaming Data

Write code to read, and write data in CSV format and do some simple
processing. This seems complex however it should be quite easy using
the methods on str, the standard file operations, and the gzip module.

All the functions should be written so they never hold the whole data
set in memory at once. So use generators.

NOTE!!! Do not use the csv module.
"""

import gzip
def read_csv(filename):
    """Parse the given (possibly gzipped) CSV file and "yield" each
    row.

    You may assume that the individual values (cells in spreadsheet
    terms) do not contain commas. Real CSV parsers handle quoting
    values, but you do not need to.

    Make sure to open the file using UTF-8 encoding.

    This function must be a generator and should not buffer more than
    one row at a time. Because of this, it should be possible to read
    files larger than the available memory using this function.

    Make sure the file is closed when you are done even if an error
    occurs.

    Do not use the csv module.

    Args:
      filename: The name of the CSV file to open. This file may be
        compressed with gzip in which case it should be decompressed
        while reading (see the gzip module).
    Yields:
      One tuple per row.

    If the input file "test" is:
      1,2,three
      2, test
    Then read_csv("test") = [(1,2,"three"),(2," test")]. Note the
    leading space on the string in the second row. It should also
    support unicode strings as UTF-8, however I don't show that here
    in case someone has an editor that doesn't support UTF-8.
    """
    # mime = mimetypes.guess_type(filename)
    # mime_type = mime.guess_type(filename)
    # print(mime)
    GZIP_MAGIC = b"\x1F\x8B"
    try:
        fb = open(filename, mode="rb")
        magic = fb.read(len(GZIP_MAGIC))
    finally:
        fb.close()
    if magic == GZIP_MAGIC:
        with gzip.open(filename, mode='rb') as fi:
             while True:
                line = fi.readline()
                if not line:
                    fi.close()
                    break
                line = line.decode()
                line = line.strip('\n').split(",")
                yield tuple(line)
    else:
        with open(filename, encoding = 'utf-8', mode="r") as fi:
            while True:
                line = fi.readline()
                if not line:
                    fi.close()
                    break
                line = line.strip('\n').split(",")
                yield tuple(line)


def generator(length):
    """
    help function: generator
    """
    for x in range(length):
        yield x


def write_csv(filename, data, compress):
    """Write out the given data as a (possibly gzipped) CSV file.

    You must support at least str and int and the str support must be
    UTF-8.

    This should support streams of data larger than memory. Make sure
    the file is closed when you are done even if an error occurs.

    Do not use the csv module.

    Args:
      filename: The filename to store to.
      data: An iterable of sequences.
      compress: If this is True compress the output file.

    write_csv("out", read_csv("in")) must generate an identical "out"
    file as it read on "in" (except that you don't need to worry about
    which line end character was used). Also if d is a sequence of
    tuples containing only str and int then following must not fail:
      write_csv("test", d)
      assert d == read_csv("test")

    write_csv("test", [(1, 2, "three"), (4, 5)]) should write the
    following to "test":
      1,2,three
      4,5
    (It should also support unicode strings as UTF-8, however I don't
    show that here in case someone has an editor that doesn't support
    UTF-8)
    """
    wGenerator = generator(len(data))
    if compress:
        with gzip.open(filename, 'wb') as fi:
            for i in wGenerator:
                data[i] = list(data[i])
                for j in range(len(data[i])):
                    data[i][j] = str(data[i][j])
                fi.write(bytes(",".join(data[i]), 'utf-8'))
                fi.write(bytes("\n", 'utf-8'))
    else:
        with open(filename, encoding = 'utf-8', mode="w") as fi:
            for i in wGenerator:
                data[i] = list(data[i])
                for j in range(len(data[i])):
                    data[i][j] = str(data[i][j])
                fi.write(",".join(data[i]))
                fi.write("\n")


def tuples_to_int_tuples(iterable):

    """Given an iterable of tuples, yield tuples where all the
    elements are ints.

    For each element in each tuple:
      If it is an int leave it unchanged.
      If it is an str convert it to an int.
      Otherwise you may do whatever you want or fail.

    Write this using a generator comprehension not using the yield
    keyword.

    For example:
      list(tuples_to_int_tuples([(1, "48")])) = [(1, 48)]
      list(tuples_to_int_tuples([(1, "0xf")])) = [(1, 15)]
      list(tuples_to_int_tuples([(1, "junk")])) fails
      list(tuples_to_int_tuples([([3], 4)])) fails
    """

    return (tuple(int(str(v), base=0) for v in x) for x in iterable)


def compute_totals(iterable):
    """Compute the row and column totals for an iterable of tuples.

    You should "yield" the results as they are computed and should not
    store all of the data at any point. This should support streams of
    data larger than memory.

    For each row add an int at the beginning that is the total of the
    row. Once the entire input has been processed add a final row with
    the totals of every column in the input. This should include the
    initial total column and you should treat columns that are missing
    on a given row as zeros. The row totals are the first column
    instead of the last (as is more common) because it makes rows of
    different length easier to handle.

    compute_totals([
      (1, 2, 3),
      (4, 5)])
     ==
    [(6, 1, 2, 3),
     (9, 4, 5),
     (15, 5, 7, 3)]
    """
    lastRow = []
    for item in iterable:
        item = list(item)
        item.insert(0,sum(item))
        yield tuple(item)
        if len(item) > len(lastRow):
            for i in range(len(item)-len(lastRow)):
                lastRow.append(0)
        else:
            for i in range(len(lastRow)-len(item)):
                item.append(0)
        lastRow = [sum(x) for x in zip(lastRow,item)]
    yield tuple(lastRow)

