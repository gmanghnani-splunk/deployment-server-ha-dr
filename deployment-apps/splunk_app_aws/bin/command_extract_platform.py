import sys
import splunk.Intersplunk
import reserved_instance.reserved_instance_const as const
import re

regex_delimiters = '|'.join(const.DELIMITERS)

def _contains_required_keywords(platform, location_words):
    # return True only if platform is a subset of location_words
    platform_words = const.PLATFORM_MAP[platform]
    return sum([1 if word in platform_words else 0 for word in location_words]) == len(platform_words)

def _parse_platform(dict, location, old_platform):
    if location not in dict:
        new_platform = 'Windows' if old_platform == 'windows' else 'Linux/UNIX'
        # only consider images provided by amazon
        location_words = re.split(regex_delimiters, location.lower())
        # map to unified key words and use set to dedup
        location_words = list(set([const.WORDS_MAP[word] if word in const.WORDS_MAP else ''
                                    for word in location_words]))

        for platform in const.PLATFORM_ORDER:
            if _contains_required_keywords(platform, location_words):
                new_platform = platform
                break

        dict[location] = new_platform

    return dict[location]

results = splunk.Intersplunk.readResults(None, None, True)
location_platform_dict = {}

for record in results:
    if 'platform' in record:
        location = ''
        if 'location' in record:
            location = record['location']
        old_platform = record['platform']
        record['platform'] = _parse_platform(location_platform_dict, location, old_platform)
    else:
        record['platform'] = 'Linux/UNIX'
    
  
splunk.Intersplunk.outputResults(results)
