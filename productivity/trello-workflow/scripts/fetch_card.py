"""Fetch Trello card by shortLink/id + its actions (triage helper).

Usage: python fetch_card.py <shortLink_or_id>
Reads TRELLO_API_KEY / TRELLO_TOKEN from ~/AppData/Local/hermes/.env.
Strips CRLF (\r) from .env values — Windows/MSYS \r pitfall.
Python-only (urllib) — tránh bash-loop \r + blocklist trên pattern có nháy kép.
"""

import json
import os
import sys
import urllib.parse
import urllib.request


def load_creds():
    with open(os.path.expanduser('~/AppData/Local/hermes/.env')) as f:
        env = {}
        for line in f:
            line = line.strip()
            if '=' in line:
                k, v = line.split('=', 1)
                env[k] = v.rstrip('\r').strip()
        return env


def main():
    if len(sys.argv) < 2:
        print('usage: python fetch_card.py <card_shortlink_or_id>')
        sys.exit(1)
    card_id = sys.argv[1]
    env = load_creds()
    key, token = env['TRELLO_API_KEY'], env['TRELLO_TOKEN']

    def api(path, params=None):
        url = 'https://api.trello.com/1/' + path + '?key=' + key + '&token=' + token
        if params:
            url += '&' + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url) as r:
            return json.loads(r.read().decode())

    card = api('cards/' + card_id, {'fields': 'name,id,desc,url,idList,dateLastActivity'})
    print('=== CARD ===')
    print(json.dumps(card, ensure_ascii=False, indent=2))
    print()
    print('=== ACTIONS (commentCard/updateCard/createCard) ===')
    acts = api('cards/' + card_id + '/actions', {'filter': 'commentCard,updateCard,createCard', 'limit': 30})
    for a in acts:
        t = a.get('type')
        d = a.get('data', {})
        m = a.get('memberCreator', {}).get('fullName', '?')
        date = a.get('date', '')
        if t == 'commentCard':
            print(f'[{date}] {m} COMMENT: {d.get("text", "")}')
        elif t == 'createCard':
            print(f'[{date}] {m} CREATE: {d.get("card", {}).get("name", "")}')
        elif t == 'updateCard':
            print(f'[{date}] {m} MOVE -> {d.get("listAfter", {}).get("name", "")}')


if __name__ == '__main__':
    main()
