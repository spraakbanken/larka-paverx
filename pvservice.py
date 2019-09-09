#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 colorcolumn=120

import bottle
import mpv

PORT = 12380
BASEDIR = 'data'


@bottle.get('/<language>')
def get_list(language):
    return mpv.get_index(language)


@bottle.get('/<language>/random/<max_cefr_level>')
def get_random_pv(language, max_cefr_level):
    languages = bottle.request.query.langs.split(',') if bottle.request.query.langs else None
    exclude = [int(x) for x in bottle.request.query.exclude.split(',')] if bottle.request.query.exclude else None
    res = mpv.get_random_particle_verb(language, max_cefr_level, languages, exclude)
    return res if res else {'error': 'no data available'}


@bottle.get('/<language>/<verb>/<particle>')
def get_pv(language, verb, particle):
    res = mpv.get_particle_verb(language, verb, particle)
    return res if res else {'error': 'no data available'}


if __name__ == '__main__':
    mpv = mpv.MPV(basedir=BASEDIR)
    bottle.run(server='waitress', workers=1, host='0.0.0.0', port=PORT)
