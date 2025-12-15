from os import getenv, environ, path, makedirs
import tver_tool
# import sys
from feedgen.feed import FeedGenerator
import urllib.parse

rrr = tver_tool.get_uid_and_token()
platform_uid   = rrr.platform_uid
platform_token = rrr.platform_token

post_header = {
  "x-tver-platform-type": "web"
}

rrr = urllib.parse.urlparse("https://tver.jp/")

# special_sub_id = sys.argv[1]
series_id = "srm706pd6g"
url_1 = f"https://platform-api.tver.jp/service/api/v1/callSeriesSeasons/{series_id}?platform_uid={platform_uid}&platform_token={platform_token}&require_data=later"

json_data_1 = tver_tool.request_get(url_1, headers=post_header)

season_id = json_data_1['result']['contents'][0]['content']['id']
url_2 = f"https://platform-api.tver.jp/service/api/v1/callSeasonEpisodes/{season_id}?platform_uid={platform_uid}&platform_token={platform_token}&require_data=later"

json_data_2 = tver_tool.request_get(url_2, headers=post_header)
iso_time_now    = tver_tool.time_iso()

title = json_data_2['result']['contents'][0]['content']['seriesTitle']

contents = json_data_2['result']['contents']

def generating_feed():

  fg = FeedGenerator()
  fg.id("https://tver.jp/")
  fg.title(title)
  fg.updated(iso_time_now)
  # fg.link("https://tver.jp/")
  fg.author({
      "name": "John Doe",
      "email": "john@example.com"
    }
  )

  for item in reversed(contents):
    episode_id    = item['content']['id']
    episode_title = item['content']['title']
    link          = f"https://tver.jp/episodes/{episode_id}"

    if not episode_id.startswith("ep"):
      continue

    eee = tver_tool.get_description(episode_id)
    eee.request_get()

    lb = tver_tool.line_break()
    lb.disable_line_break(eee.data['description'])

    fe = fg.add_entry()
    fe.id(link)
    fe.title(episode_title)
    fe.updated(iso_time_now)
    fe.content(lb.dis_lb_str)
    fe.link(href=link)

  atom_xml = fg.atom_str(pretty=True)
  return atom_xml


workspace = getenv("GITHUB_WORKSPACE")
home_dir  = getenv("HOME")

path_to_use = workspace if workspace else home_dir
middle_dir  = "server"
atom_file   = f"sr_[{series_id}]_[{season_id}].atom"

atom_dir = path.join(path_to_use, "server", f"[{rrr.netloc}]")

makedirs(atom_dir, exist_ok=True)

atom_path = path.join(atom_dir, atom_file)


with open(environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"atom_file={atom_file}\n")
    f.write("publish_repo=public\n")




def main():
  atom_xml = generating_feed()

  with open(atom_path, "wb") as f:
    f.write(atom_xml)

if __name__ == '__main__':
  main()

