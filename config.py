import os
import local_settings

"""TODO: --ffmpeg-location PATH           Location of the ffmpeg/avconv binary;
                                     either the path to the binary or its
                                     containing directory.
    --restrict-filenames             Restrict filenames to only ASCII
                                     characters, and avoid "&" and spaces in
                                     filenames
"""

class Config(object):
	SECRET_KEY = os.environ.get("SECRET_KEY") or "sske89822Jl..234BBB--=SSS298234"
	MAX_CONCURRENT_DL = 3
	FFMPEG_LOCATION = local_settings.FFMPEG_LOCATION
	OUTPUT_TEMPLATE = local_settings.OUTPUT_TEMPLATE
	TEMPLATES_AUTO_RELOAD = local_settings.TEMPLATES_AUTO_RELOAD

