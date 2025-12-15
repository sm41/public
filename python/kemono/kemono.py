import requests
from os import getenv, path, makedirs
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import urllib.parse

service_id = "patreon"
creator_id = "86508534"

post_url = f"https://kemono.cr/api/v1/{service_id}/user/{creator_id}/posts"
prof_url = f"https://kemono.cr/api/v1/{service_id}/user/{creator_id}/profile"

headers = {
  # "Accept": "application/json"
  "Accept": "text/css"
}

rrr = urllib.parse.urlparse(post_url)

post_res = requests.get(post_url, headers=headers)
post_res.raise_for_status()  # エラー時に例外
post_json = post_res.json()

prof_res = requests.get(prof_url, headers=headers)
prof_res.raise_for_status()
prof_json = prof_res.json()

def convert_isotime(anytime):
  dt          = datetime.fromisoformat(anytime)
  dt_utc      = dt.replace(tzinfo=timezone.utc)
  dt_tokyo    = dt_utc.astimezone(ZoneInfo("Asia/Tokyo"))
  publish_iso = dt_tokyo.isoformat()
  return publish_iso

def generating_feed():
  fg = FeedGenerator()
  fg.id(prof_json['name'])
  fg.title(prof_json['name'])
  fg.updated(convert_isotime(prof_json['updated']))
  # fg.link("https://tver.jp/")
  fg.author({
      "name": "John Doe",
      "email": "john@example.com"
    }
  )

  for iii in reversed(post_json):

    id        = f"https://kemono.cr/{service_id}/user/{creator_id}/post/{iii['id']}"
    title     = iii['title']
    published = convert_isotime(iii['published'])
    content = iii['substring']

    if iii.get('file', {}).get('path'):
      link = f"https://img.kemono.cr/thumbnail/data{iii['file']['path']}"
    else:
      link = "none"

    fe = fg.add_entry()
    fe.id(id)
    fe.title(title)
    fe.updated(published)
    fe.content(content)
    fe.link(href=link)

  atom_xml = fg.atom_str(pretty=True)
  return atom_xml


atom_name = f"{prof_json['id']}_{prof_json['public_id']}.atom"
workspace = getenv("GITHUB_WORKSPACE")
home_dir  = getenv("HOME")

path_to_use = workspace if workspace else home_dir
atom_dir = path.join(path_to_use, "server", f"[{rrr.netloc}]")

makedirs(atom_dir, exist_ok=True)

atom_path = path.join(atom_dir, atom_name)



def main():
  atom_xml = generating_feed()

  with open(atom_path, "wb") as f:
    f.write(atom_xml)



if __name__ == '__main__':
  main()
