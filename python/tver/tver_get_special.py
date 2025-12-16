from os import getenv, environ, path, makedirs
import tver_tool
from feedgen.feed import FeedGenerator
import urllib.parse

rrr = tver_tool.get_uid_and_token()
platform_uid   = rrr.platform_uid
platform_token = rrr.platform_token

post_header = {
  "x-tver-platform-type": "web"
}

rrr = urllib.parse.urlparse("https://tver.jp/")

url_1 = "https://service-api.tver.jp/api/v1/callSpecial"

json_data = tver_tool.request_get(url_1, headers=post_header)
iso_time_now  = tver_tool.time_iso()

contents_1 = json_data['result']['contents']

def get_sp_sub_id(sp_main_id):

  url_2 = f"https://platform-api.tver.jp/service/api/v1/callSpecialContents/{sp_main_id}?platform_uid={platform_uid}&platform_token={platform_token}&require_data=later"

  kkk = tver_tool.request_get(url_2, post_header)
  sp_sub_id = kkk['result']['specialContents'][0]['content']['id']
  return sp_sub_id


def generating_feed():

  fg = FeedGenerator()
  fg.id("https://tver.jp/")
  fg.title("特集")
  fg.updated(iso_time_now)
  # fg.link("https://tver.jp/")
  fg.author({
      "name": "John Doe",
      "email": "john@example.com"
    }
  )

  for item in reversed(contents_1):
    special_main_id    = item['content']['id']
    special_main_title = item['content']['title']
    special_sub_id     = get_sp_sub_id(special_main_id)
    link               = f"https://tver.jp/specials/{special_main_id}/{special_sub_id}"

    sss = tver_tool.get_description(special_sub_id)
    sss.request_get()

    lb = tver_tool.line_break()
    lb.disable_line_break(sss.data['description'])

    fe = fg.add_entry()
    fe.id(link)
    fe.title(special_main_title)
    fe.updated(iso_time_now)
    fe.content(lb.dis_lb_str)
    fe.link(href=link)

  atom_xml = fg.atom_str(pretty=True)
  return atom_xml






workspace = getenv("GITHUB_WORKSPACE")
home_dir  = getenv("HOME")

path_to_use = workspace if workspace else home_dir
middle_dir  = "feed"
atom_file   = "special_main.atom"

# atom_dir = path.join(path_to_use, middle_dir, f"[{rrr.netloc}]")
atom_dir = path.join(path_to_use, middle_dir, "tver")

makedirs(atom_dir, exist_ok=True)

atom_path = path.join(atom_dir, atom_file)



with open(environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"atom_file={atom_file}\n")
    # f.write("publish_repo=public\n")
    # f.write(f"atom_path={atom_path}\n")




def main():
  atom_xml = generating_feed()

  with open(atom_path, "wb") as f:
    f.write(atom_xml)

if __name__ == '__main__':
  main()
