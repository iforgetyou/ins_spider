import sys

sys.path.append('/Applications/google-cloud-sdk/platform/google_appengine/')
sys.path.append('/Applications/google-cloud-sdk/platform/google_appengine/lib/yaml/lib/')
if 'google' in sys.modules:
    del sys.modules['google']

# import google
# print google.__path__

class InsImage(object):
    def __init__(self):
        self.id = None
        self.image_url = None
        self.video_url = None
        self.owner = None


