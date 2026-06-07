import requests
import sys
from textwrap import fill

API_BASE = 'https://openscriptureapi.org/api/scriptures/v1/lds/en/volume'

# Built-in volumes and book lists (slugs used by the API)
VOLUMES = {
    'Book of Mormon': {
        'slug': 'bookofmormon',
        'books': ['1Nephi','2Nephi','Jacob','Enos','Jarom','Omni','Words of Mormon','Mosiah','Alma','Helaman','3Nephi','4Nephi','Mormon','Ether','Moroni']
    },
    'Old Testament': {
        'slug': 'ot',
        'books': [
            'Genesis','Exodus','Leviticus','Numbers','Deuteronomy','Joshua','Judges','Ruth','1Samuel','2Samuel',
            '1Kings','2Kings','1Chronicles','2Chronicles','Ezra','Nehemiah','Esther','Job','Psalms','Proverbs',
            'Ecclesiastes','Song of Solomon','Isaiah','Jeremiah','Lamentations','Ezekiel','Daniel','Hosea','Joel',
            'Amos','Obadiah','Jonah','Micah','Nahum','Habakkuk','Zephaniah','Haggai','Zechariah','Malachi'
        ]
    },
    'New Testament': {
        'slug': 'nt',
        'books': ['Matthew','Mark','Luke','John','Acts','Romans','1Corinthians','2Corinthians','Galatians','Ephesians','Philippians','Colossians','1Thessalonians','2Thessalonians','1Timothy','2Timothy','Titus','Philemon','Hebrews','James','1Peter','2Peter','1John','2John','3John','Jude','Revelation']
    },
    'Doctrine & Covenants': {
        'slug': 'dc-testament',
        'books': ['Doctrine and Covenants']
    },
    'Pearl of Great Price': {
        'slug': 'pgp',
        'books': ['Moses','Abraham','Joseph Smith—Matthew','Joseph Smith—History','Articles of Faith']
    }
}

def _normalize_book_for_api(name: str) -> str:
    """Normalize a book name to the slug expected by the API (lowercase, no spaces or punctuation)."""
    return ''.join(ch.lower() for ch in name if ch.isalnum())


def get_summary(volume_slug: str, book: str, chapter: str, timeout=10):
    """Fetch chapter JSON from the OpenScripture API and return the chapter summary if present.

    volume_slug: API volume slug (e.g., 'bookofmormon', 'ot', 'nt')
    book: human-readable book name (will be normalized)
    chapter: chapter number or identifier as string
    """
    book_slug = _normalize_book_for_api(book)
    url = f"{API_BASE}/{volume_slug}/{book_slug}/{chapter}"
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        # some endpoints return the chapter under 'chapter'
        chapter_obj = data.get('chapter') or data
        summary = chapter_obj.get('summary')
        if summary:
            return summary
        # Fallback: try to build a short text from verses if no summary provided
        verses = chapter_obj.get('verses')
        if verses and isinstance(verses, list):
            # join first few verses as a fallback
            return ' '.join(v.get('text','') for v in verses[:6])
        return None
    except requests.HTTPError as e:
        raise RuntimeError(f'HTTP error: {e}')
    except requests.RequestException as e:
        raise RuntimeError(f'Network error: {e}')
    except ValueError:
        raise RuntimeError('Invalid JSON response from API')


def choose_from_list(prompt: str, options: list):
    for i, opt in enumerate(options, start=1):
        print(f"{i}. {opt}")
    while True:
        choice = input(prompt).strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
        # allow matching by name (case-insensitive, partial)
        lower = choice.lower()
        matches = [o for o in options if lower in o.lower()]
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            print('Multiple matches:', ', '.join(matches[:8]))
        else:
            print('Invalid selection. Enter a number or part of the book name.')


def print_header():
    print('='*70)
    print('Scripture Summary Tool — fetches chapter summaries from OpenScripture API')
    print('You can choose a volume, then a book and chapter to view a short summary.')
    print('='*70)


def run_summary_tool():
    print_header()
    # let user choose volume
    volume_names = list(VOLUMES.keys())
    while True:
        print('\nChoose a volume:')
        vol_choice = choose_from_list('Volume (number or name): ', volume_names)
        vol = VOLUMES[vol_choice]

        # select book
        print(f"\nBooks in {vol_choice}:")
        book = choose_from_list('Select book (number or name): ', vol['books'])

        # ask chapter
        chapter = input(f"Enter chapter number for {book}: ").strip()
        if not chapter:
            print('Chapter is required. Try again.')
            continue

        try:
            summary = get_summary(vol['slug'], book, chapter)
            if summary:
                print('\n' + '-'*60)
                print(f'Summary of {book} chapter {chapter}:')
                print(fill(summary, width=78))
                print('-'*60 + '\n')
            else:
                print('No summary available for that chapter.')
        except Exception as e:
            print(f'Error fetching summary: {e}')

        again = input('Would you like to view another (Y/N)? ').strip().lower()
        if again != 'y':
            print('Thank you for using the Scripture Summary Tool!')
            break


if __name__ == '__main__':
    try:
        run_summary_tool()
    except KeyboardInterrupt:
        print('\nExiting...')
        sys.exit(0)