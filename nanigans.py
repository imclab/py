import requests


def main():
    """
    De-dupe and sum the key/values from two given input files.

    The basic idea is to pull all of the input into one long, new-line
    deliniated string, use a dictionary (ie, hash table) to keep track of
    existing values and help with de-deuping, then create a list to
    maintain order and sort the keys and finally iterate over that
    sorted list to print out the summaries in order.
    """

    # get the content of the two indivudal files
    content_1 = fetch_content("http://www.nanigans.com/files/file1.txt")
    content_2 = fetch_content("http://www.nanigans.com/files/file2.txt")

    # combine their content into one string
    content = "{part_1}\n{part_2}".format(part_1=content_1, part_2=content_2)

    # initialize the dict we'll be using to de-dupe keys
    data = {}

    # iterate over each line of the file
    for line in content.split("\n"):

        # parse out the key/value contained in this line
        key, value = line.strip().split("=")

        # increment the data dict at this key by this value
        existing_value = data.setdefault(key, 0)
        data[key] = existing_value + int(value)

    # created a new list with the sorted keys
    sorted_keys = sorted(data.keys())

    # iterate over the list of sorted keys and pring the total value for that key
    for key in sorted_keys:
        print "{key}={value}".format(key=key, value=data[key])


def fetch_content(url):
    """
    Takes a URL and returns the body of the HTTP response as a string.

    Since the `requests` lib makes it easy to access the entire response
    body with .text, we'll just use that and read the entire response into
    memory at once. If the files were succificiently large, we might want
    to use urllib to open a connection and `read` the response line by
    line, more like a file.
    """
    return requests.get(url).text

if __name__ == "__main__":
    main()
