def chunk(sequence, num_chunks):
    """
    Split a sequence into equal-ish length chunks.

    # From https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
    """
    k, m = divmod(len(sequence), num_chunks)
    return (sequence[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in xrange(num_chunks))


def paginate(page):
    """
    Generates a sequence of items to paginate through.

    Yields a tuple of three items:

    * Item display value
    * Item link value
    * Whether to linkify

    """
    for p in page.paginator.page_range:
        p = page.paginator.page(p)

        yield p.number, p.url, p.number != page.number
