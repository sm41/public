from os import getenv, environ, path, makedirs
import tldextract
import tver_tool
from feedgen.feed import FeedGenerator

origin_url = "https://tver.jp/"
url_1      = "https://service-api.tver.jp/api/v1/callSpecial"


def get_sp_sub_id(sp_main_id, platform_uid, platform_token):

  url_2 = f"https://platform-api.tver.jp/service/api/v1/callSpecialContents/{sp_main_id}?platform_uid={platform_uid}&platform_token={platform_token}&require_data=later"

  kkk = tver_tool.request_get(url_2)
  sp_sub_id = kkk['result']['specialContents'][0]['content']['id']
  return sp_sub_id


def generating_feed():

  rrr          = tver_tool.get_uid_and_token()
  iso_time_now = tver_tool.time_iso()
  json_data    = tver_tool.request_get(url_1)
  contents_1   = json_data['result']['contents']

  fg = FeedGenerator()
  fg.id(origin_url)
  fg.title("特集")
  # fg.icon("https://tver.jp/favicon.ico")
  fg.updated(iso_time_now)
  fg.link(href="https://sm41.github.io/public/")
  fg.author({
      "name": "John Doe",
      "email": "john@example.com"
    }
  )

  for item in reversed(contents_1):
    special_main_id    = item['content']['id']
    special_main_title = item['content']['title']
    special_sub_id     = get_sp_sub_id(special_main_id, rrr.platform_uid, rrr.platform_token)
    special_images     = f"https://image-cdn.tver.jp/images/content/thumbnail/specialMain/xlarge/{special_main_id}.jpg"

    ooo = tver_tool.get_description(special_sub_id)
    hhh = tver_tool.line_break(ooo['description'])

    html = tver_tool.get_sp_main_html(special_images, hhh)

    fe = fg.add_entry()
    fe.id(f"https://tver.jp/specials/{special_main_id}/{special_sub_id}")
    fe.title(special_main_title)
    fe.updated(iso_time_now)
    fe.content(html, type='html')
    fe.link(href=f"https://tver.jp/specials/{special_main_id}/{special_sub_id}")

  atom_xml = fg.atom_str(pretty=True)
  return atom_xml


def main():

  ext = tldextract.extract(origin_url)

  workspace = getenv("GITHUB_WORKSPACE")
  home_dir  = getenv("HOME")

  path_to_use = workspace if workspace else home_dir
  publish_dir = "docs"
  middle_dir  = "feed"
  atom_file   = "special_main.atom"

  atom_dir = path.join(path_to_use, publish_dir, middle_dir, ext.domain)

  makedirs(atom_dir, exist_ok=True)

  atom_path = path.join(atom_dir, atom_file)
  atom_xml  = generating_feed()

  with open(atom_path, "wb") as f:
    f.write(atom_xml)


if __name__ == '__main__':
  main()
