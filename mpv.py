# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 colorcolumn=120

import os
import yaml
import random

LANGUAGES = ['en', 'sv']
CEFR = ['A1', 'A2', 'B1', 'B2', 'C1']


class MPV:
    index = {}
    cache = {}
    cefr_level = {}

    def __init__(self, basedir='.'):
        self.basedir = basedir
        for lang in LANGUAGES:
            try:
                with open(os.path.join(basedir, '{}/index.yml'.format(lang)), 'r') as file:
                    self.index[lang] = yaml.safe_load(file.read())
            except:
                raise Exception('index file could not be loaded for language {}'.format(lang))
            for level, pvlist in self.index[lang].items():
                for pv in pvlist:
                    self.cefr_level.setdefault(pv['v'], {}).setdefault(pv['p'], {
                        'l': level,
                        'id': pv['n']
                    })

    def get_index(self, language):
        if language not in self.index:
            raise Exception('language unknown ({})'.format(language))
        return self.index(language)

    def get_particle_verb(self, language, verb, particle):
        """Returns the requested PV object, or False if unavailable."""
        examples = self._particle_verb_raw(language, verb, particle)
        if examples:
            return {
                'id': self.cefr_level[verb][particle]['id'],
                'verb': verb,
                'particle': particle,
                'cefr': self.cefr_level[verb][particle]['l'],
                'examples': examples
            }
        else:
            return False

    def get_random_particle_verb(self, language, max_cefr_level, languages=None, exclude=None):
        """"Return "random PV object, or False if none is matching"""
        print("{}, {}, {}, {}".format(language, max_cefr_level, languages, exclude))
        if max_cefr_level not in CEFR:
            raise Exception('invalid CEFR level')
        pvlist = []
        for level in CEFR:
            pvlist += self.index[language][level]
            if level == max_cefr_level:
                break
        random.shuffle(pvlist)
        for pv in pvlist:
            if pv['n'] in exclude:
                continue
            res = self.get_particle_verb(language, pv['v'], pv['p'])
            if res:
                if languages:
                    for lang in languages:
                        if lang in res['examples']:
                            return res
                    return False
                else:
                    return res
        return False

    def _particle_verb_raw(self, language, verb, particle):
        """Returns examples sentences for a given PV, or False if none available."""
        key = '{}#{}#{}'.format(language, verb, particle)
        if key not in self.cache:
            filename = os.path.join(self.basedir, '{}/{}_{}.yml'.format(language, verb, particle))
            if os.path.isfile(filename):
                with open(filename, 'r') as file:
                    self.cache[key] = yaml.safe_load(file.read())
            else:
                self.cache[key] = False
        return self.cache[key]

