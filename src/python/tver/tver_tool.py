import requests
from datetime import datetime
from zoneinfo import ZoneInfo


# 新着取得API · dongaba/TVerRec Wiki
# https://github.com/dongaba/TVerRec/wiki/%E6%96%B0%E7%9D%80%E5%8F%96%E5%BE%97API

# https://image-cdn.tver.jp/images/content/thumbnail/series/xlarge/{series_id}.jpg
# https://image-cdn.tver.jp/images/content/thumbnail/episode/xlarge/{episode_id}.jpg

class get_uid_and_token:

  url = "https://platform-api.tver.jp/v2/api/platform_users/browser/create"

  headers = {
    "Accept"          : "*/*",
    "Origin"          : "https://s.tver.jp",
    "Referer"         : "https://s.tver.jp/",
    "Content-Type"    : "application/x-www-form-urlencoded",
    "Connection"      : "keep-alive",
    "Sec-Fetch-Dest"  : "empty",
    "Sec-Fetch-Mode"  : "cors",
    "Sec-Fetch-Site"  : "same-site",
  }

  data = {
    "device_type" : "pc"
  }

  def __init__(self):
    response  = requests.post(self.url, headers=self.headers, data=self.data)
    json_data = response.json()

    self.platform_uid   = json_data['result']['platform_uid']
    self.platform_token = json_data['result']['platform_token']


def request_get(url, headers):
  response = requests.get(url, headers=headers)
  response.raise_for_status()  # エラー時に例外
  json_data = response.json()
  return json_data


class get_description:
  def __init__(self, id:str):
    if id.startswith("sr"):
      self.url = f"https://statics.tver.jp/content/series/{id}.json"
    elif id.startswith("ep"):
      self.url = f"https://statics.tver.jp/content/episode/{id}.json"
    else:
      self.url = f"https://statics.tver.jp/content/special/{id}.json"

    self.headers = {
      "x-tver-platform-type": "web"
    }

  def request_get(self):
    response = requests.get(self.url, headers=self.headers)
    response.raise_for_status()
    self.data = response.json()




class line_break:
  def __init__(self):
    pass

  def enable_line_break(self, strings:str):
    self.en_lb_str = strings.replace("\\n", "\n")

  def disable_line_break(self, strings:str):
    self.dis_lb_str = strings.replace("\n", "\\n")



def gen_xhtml(img_url, img_alt, content):

  xhtml_template = f"""\
    <div xmlns="http://www.w3.org/1999/xhtml">
      <img src="{img_url}" alt="[{img_alt}]" />
      <p>
        {content}
      </p>
    </div>\
  """

  return xhtml_template





def time_iso():
  tokyo_time = datetime.now(ZoneInfo("Asia/Tokyo")).replace(microsecond=0)
  iso_time_now   = tokyo_time.isoformat()
  return iso_time_now