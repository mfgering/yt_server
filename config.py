import os

class Config(object):
	SECRET_KEY = os.environ.get("SECRET_KEY") or "sske89822Jl..234BBB--=SSS298234"
	MAX_CONCURRENT_DL = 3
	OUTPUT_TEMPLATE = "//alpha.dawson/test/vids/yt/%(title)s.%(ext)s"
	TEMPLATES_AUTO_RELOAD = True