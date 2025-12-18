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
special_sub_id = "all25_1129"
url = f"https://platform-api.tver.jp/service/api/v1/callSpecialContentsDetail/{special_sub_id}?platform_uid={platform_uid}&platform_token={platform_token}&sort_key=recommend&require_data=mylist%2Clater"



json_data    = tver_tool.request_get(url, headers=post_header)
iso_time_now = tver_tool.time_iso()

json_content  = json_data['result']['contents']['content']
sp_main_id    = json_content['specialMainID']
sp_main_title = json_content['specialMainTitle']
list          = json_content['contents']



def generating_feed():

  fg = FeedGenerator()
  fg.id("https://tver.jp/")
  fg.title(sp_main_title)
  fg.updated(iso_time_now)
  # fg.link(href="https://tver.jp/")
  fg.author({
      "name": "John Doe",
      "email": "john@example.com"
    }
  )

  for iii in reversed(list):
    series_title = iii['content']['title']
    series_id    = iii['content']['id']
    link         = f"https://tver.jp/series/{series_id}"

    sss = tver_tool.get_description(series_id)
    sss.request_get()

    lb = tver_tool.line_break()
    lb.disable_line_break(sss.data['description'])

    fe = fg.add_entry()
    fe.id(link)
    fe.title(series_title)
    fe.updated(iso_time_now)
    fe.content(lb.dis_lb_str)
    fe.link(href=link)
  # f"https://image-cdn.tver.jp/images/content/thumbnail/series/xlarge/{series_id}.jpg"

  atom_xml = fg.atom_str(pretty=True)
  return atom_xml





workspace = getenv("GITHUB_WORKSPACE")
home_dir  = getenv("HOME")

path_to_use = workspace if workspace else home_dir
middle_dir  = "feed"
atom_file   = f"sp_[{sp_main_id}]_[{special_sub_id}].atom"

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
