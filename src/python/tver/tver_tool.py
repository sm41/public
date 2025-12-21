import requests
from datetime import datetime
from zoneinfo import ZoneInfo


# 新着取得API · dongaba/TVerRec Wiki
# https://github.com/dongaba/TVerRec/wiki/%E6%96%B0%E7%9D%80%E5%8F%96%E5%BE%97API

# https://image-cdn.tver.jp/images/content/thumbnail/series/xlarge/{series_id}.jpg
# https://image-cdn.tver.jp/images/content/thumbnail/episode/xlarge/{episode_id}.jpg


headers = {
  "x-tver-platform-type": "web"
}

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


def request_get(url):
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


  def request_get(self):
    self.data = request_get(self.url)




class line_break:
  def __init__(self):
    pass

  def lb_html(self, strings:str):
    self.lb_html_str = strings.replace("\n", "<br>")




def gen_html(img_url, content, start_at, end_at, broadcastDateLabel, production_provider_name):

  html_template = f"""\
    <body>
      <img src="{img_url}">

      <table style=width:100%;>
        <tr style=text-align:left;>
          <th>🕘 配信開始</th>
          <th>🗓️ 放送</th>
        </tr>

        <tr style=text-align:center;>
          <td>{start_at}</td>
          <td>{broadcastDateLabel}</td>
        </tr>

        <tr style=text-align:left;>
          <th>🕓 配信終了</th>
          <th>📡 放送局</th>
        </tr>

        <tr style=text-align:center;>
          <td>{end_at}</td>
          <td>{production_provider_name}</td>
        </tr>
      </table>

      <hr>

      <p>
        {content}
      </p>
    </body>\
  """

  return html_template



def get_sp_main_html(img_url, content):

    sp_main_html_template = f"""\
      <div>
        <img src="{img_url}">

        <hr style="border:0; border-top:1px solid yellow">

        <p>
          {content}
        </p>
      </div>\
    """

    return sp_main_html_template



def time_iso():
  tokyo_time = datetime.now(ZoneInfo("Asia/Tokyo")).replace(microsecond=0)
  iso_time_now   = tokyo_time.isoformat()
  return iso_time_now