import grequests
from progress.bar import IncrementalBar
import os


class TileDownloader(object):
    def __init__(self, tiles_path, tiles_json, key, skip=True):
        tiles = tiles_json['tiles']
        self.tiles_path = tiles_path
        self.key = key

        self.config = tiles_json['config']
        self.primary = tiles['primary']
        self.half = tiles['half']
        self.skip = skip

    def download(self):
        print 'Full tiles...'
        self.download_tiles(self.primary)
        print 'Half tiles...'
        self.download_tiles(self.half, prefix='half-')

    def download_tiles(self, tiles, prefix=''):
        bar = IncrementalBar('Downloading', max=len(tiles))

        if self.skip:
            # Filter out tiles that exist if skipping
            tiles = filter(
                lambda tile: not self.tile_exists(tile, prefix),
                tiles
            )
            bar.next(bar.max - len(tiles))

        requests = [
            grequests.get(
                tile['url'],
                params={'key': self.key},
                # Hack: include a reference back to the tile index
                # so I can get the tile inside imap below.
                headers={'X-Ref': idx},
            )
            for idx, tile in enumerate(tiles)
        ]

        def error_handler(request, exception):
            print 'Error!', exception

        for response in grequests.imap(requests, size=10, exception_handler=error_handler):
            bar.next()
            #import pdb; pdb.set_trace()
            if response and response.status_code == 200:
                idx = int(response.request.headers['X-Ref'])
                tile = tiles[idx]
                file_name = tile_path(self.tiles_path, prefix, tile['x'], tile['y'])
                save_response_to(response, file_name)
            else:
                print 'Error downloading tile!', response

        bar.finish()

    def tile_exists(self, tile, prefix):
        return os.path.isfile(tile_path(self.tiles_path, prefix, tile['x'], tile['y']))

def tile_path(directory, prefix, x, y):
    return os.path.join(directory, '{prefix:s}{x:d}x{y:d}'.format(prefix=prefix, x=x, y=y))

def save_response_to(response, path):
    with open(path, 'wb') as f:
        for chunk in response.iter_content():
            f.write(chunk)
