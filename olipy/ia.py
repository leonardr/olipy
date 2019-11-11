"""Code for dealing with the Internet Archive."""
import datetime
import internetarchive as ia
import requests
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

class Item(object):
    "Wraps the ia.item class with extra utilities."""

    MEDIA_TYPE = None
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    _session = None

    def __init__(self, identifier):
        item = metadata = None
        if isinstance(identifier, ia.item.Item):
            # This is an actual Item object from the underlying
            # API wrapper.
            item = identifier
            identifier = item.identifier
            metadata = item.metadata
        elif isinstance(identifier, dict):
            # This is raw metadata from the underlying API wrapper
            item = None
            metadata = identifier
            identifier = identifier['identifier']
        self.identifier = identifier
        self._item = item
        self._metadata = metadata
        self._files = None

    @classmethod
    def session(cls, set_to=None):
        """Keep one ArchiveSession object for the whole program.

        The session doesn't seem to keep any state so this should be
        fine.
        """
        if set_to:
            cls._session = set_to
        if not cls._session:
            cls._session = ia.session.ArchiveSession()
        return cls._session

    @classmethod
    def recent(cls, query="", cutoff=None, fields=None, sorts=None, page=100, *args, **kwargs):
        """Find all the items that match `query` that were added since
        `date`.
        """
        if isinstance(cutoff, basestring):
            cutoff = datetime.datetime.strptime(cutoff, cls.DATE_FORMAT)
        sorts = sorts or []
        sorts.insert(0, 'publicdate desc')

        fields = fields or []
        for item in cls.search(query, *args, fields=fields, sorts=sorts, **kwargs):
            if cutoff and item.date('publicdate') < cutoff:
                break
            yield item


    @classmethod
    def search(cls, query, collection=None, fields=None, sorts=None, *args, **kwargs):
        """Search Internet Archive items.
        :param fields: Retrieve these metadata fields for each item. List of
            fields: https://archive.org/services/search/v1/fields
            By default, 'title', 'publidate', and 'identifier' are retrieved.
        :param sorts: A list of fields to use as sort order. Add
            " asc" or " desc" to the name of the field to specify
            ascending or descending order.
        """
        fields = fields or []
        for mandatory in ['title', 'publicdate']:
            if not mandatory in fields:
                fields.append(mandatory)
        query = cls.modified_query(query, collection)
        search = ia.search.Search(
            cls.session(), query, *args, fields=fields, sorts=sorts,
            **kwargs
        )
        for i in search.iter_as_results():
            yield cls(i)

    @classmethod
    def modified_query(cls, query, collection):
        addenda = []
        if collection:
            addenda.append("collection:%s" % collection)
        if cls.MEDIA_TYPE:
            addenda.append("mediatype:%s" % cls.MEDIA_TYPE)
        if not addenda:
            return query
        if query:
            query += ' and '
        extra = " and ".join(addenda)
        return query + extra

    def date(self, field="date"):
        """Parse a date field associated with this item."""
        if not field.endswith('date'):
            field += 'date'
        data = self.metadata.get(field)
        if not data:
            return None
        parsed = datetime.datetime.strptime(data, self.DATE_FORMAT)
        return parsed

    @property
    def item(self):
        if not self._item:
            self._item = ia.get_item(self.identifier)
        return self._item

    @property
    def files(self):
        if not self._files:
            self._files = list(self.item.get_files())
        return self._files

    @property
    def metadata(self):
        if not self._metadata:
            self._metadata = self.item.metadata
        return self._metadata


class Text(Item):
    """This class knows about the IA book reader."""

    MEDIA_TYPE = "texts"

    # The URL to a specific page in the IA book reader.
    reader_template = "https://archive.org/details/%(identifier)s/page/n%(page)d"

    # The URL to the actual image of a specific page used in the IA book reader.
    reader_image_template = "https://%(server)s/BookReader/BookReaderImages.php?zip=%(zip_path)s&file=%(image_path)s"

    # The path to a ZIP file on an IA server, used to fill in %(zip_path)s in
    # reader_image_template
    zip_path_template = "/%(directory_number)s/items/%(identifier)s/%(archive_filename)s"

    @property
    def pages(self):
        """How many pages are in this book?

        i.e. how many images are in this text?
        """
        return int(self.metadata.get('imagecount', 0))

    @property
    def jp2_url(self):
        """Find the URL to the JP2 version of this text.

        This is essential to finding working image URLs.
        """
        jp2 = [
            x for x in self.files
            if x.format == u'Single Page Processed JP2 ZIP'
            and x.exists
        ]
        if not jp2:
            return None
        return jp2[0].url

    def reader_url(self, page):
        """Generate the URL to the Internet Archive reader for page X."""
        return self.reader_template % dict(
            identifier=self.identifier,
            page=page
        )

    def image_url(self, page, **kwargs):
        """Generate the URL to an image for page X.

        Before using the image you might want to make a HEAD request
        to make sure the image is actually there. The URL generation
        works pretty reliably, but I've seen cases where the book is
        shorter than reported.

        :param kwargs: Will be appended to the URL as extra arguments.
        Useful arguments include 'scale' and 'rotate'.
        """

        # Get the URL to the JP2 version of the text. This is the
        # version used by the web reader, so it's important to know
        # what it's called.
        jp2_url = self.jp2_url

        # Make a HEAD request to the jp2 URL to see which server the
        # file is on and which directory it's in.
        response = requests.head(jp2_url)
        if response.status_code != 302 or not 'location' in response.headers:
            return None
        location = response.headers['location']
        parsed = urlparse.urlparse(location)

        # ZIP files are hosted at servers whose URLs look like this:
        # https://ia600106.us.archive.org/
        server = parsed.netloc

        path = parsed.path.split("/")
        directory_number = path[1]
        jp2_filename = path[-1]

        # The ZIP lives on the server at a path that looks like:
        # /30/items/identifier/A_Great_Book/A_Great_Book_jp2.zip
        zip_path = self.zip_path_template % dict(
            directory_number=directory_number,
            identifier=self.identifier,
            archive_filename=jp2_filename,
        )

        # ZIP files for texts contain one JP2 file per page, in a
        # directory named after the ZIP file:
        # A_Great_Book_jp2/A_Great_Book_0000.jp2
        with_format_identifier = jp2_filename[:-len('.zip')]
        filename_base = jp2_filename[:-len("_jp2.zip")]
        image_filename = filename_base + "_%.4d.jp2" % page
        path_within_file = "/".join([with_format_identifier, image_filename])

        image_url = self.reader_image_template % dict(
            server=server,
            zip_path=zip_path,
            image_path=path_within_file,
        )
        extra = "&".join("%s=%s" % (k, v) for k, v in kwargs.items())
        if extra:
            image_url += "&" + extra
        return image_url


class Audio(Item):
    """This class knows about audio items."""
    MEDIA_TYPE = "audio"
