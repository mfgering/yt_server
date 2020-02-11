import os
import local_settings

"""TODO:    --restrict-filenames             Restrict filenames to only ASCII
                                     characters, and avoid "&" and spaces in
                                     filenames
"""

class Config(object):
	SECRET_KEY = os.environ.get("SECRET_KEY") or "sske89822Jl..234BBB--=SSS298234"
	MAX_CONCURRENT_DL = 3
	TEMPLATES_AUTO_RELOAD = False
	DEFAULT_DOWNLOAD_NAME_PATTERN = '%(title)s.%(ext)s'
	FFMPEG_LOCATION = None
	RESTRICT_FILENAMES = True

_local_members = [attr for attr in dir(local_settings) if not callable(getattr(local_settings, attr)) and not attr.startswith("__")]
for local_member in _local_members:
	setattr(Config, local_member, getattr(local_settings, local_member))
