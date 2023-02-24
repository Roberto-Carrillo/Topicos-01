def load_text(file_path):
    """A convenience function for reading in the files used for the site's text"""
    with open(file_path) as in_file:
        return in_file.read()
