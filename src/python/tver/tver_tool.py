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


def request_get(url):
  headers = {
    "x-tver-platform-type": "web"
  }

  response = requests.get(url, headers=headers)
  response.raise_for_status()  # エラー時に例外
  json_data = response.json()
  return json_data


def get_description(id:str):

  if id.startswith("sr"):
    url = f"https://statics.tver.jp/content/series/{id}.json"
  elif id.startswith("ep"):
    url = f"https://statics.tver.jp/content/episode/{id}.json"
  else:
    url = f"https://statics.tver.jp/content/special/{id}.json"

  data = request_get(url)
  return data


def line_break(strings:str):
  lb_html_str = strings.replace("\n", "<br>")
  return lb_html_str


def gen_html(episode_images, series_images, content, series_title, series_id, start_at, end_at, broadcastDateLabel, production_provider_name):
  html_template = f"""\
    <body>
      <img src="{series_images}">

      <hr>

      <div>🎞️ {series_title}
        <a href="https://tver.jp/series/{series_id}" target="_blank" rel="noopener noreferrer">🔗</a>
      </div>

      <table>
        <th>
          <td>
            <div>🕘 配信開始 : {start_at}</div>
            <div>🕓 配信終了 : {end_at}</div>
          </td>
        </th>
        <th>
          <td>
            <div>🗓️ 放送&emsp; : {broadcastDateLabel}</div>
            <div>📡 放送局 : {production_provider_name}</div>
          </td>
        </th>
      </table>

      <hr>

      <img src="{series_images}">

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

        <hr>

        <p>
          {content}
        </p>
      </div>\
    """

    return sp_main_html_template



def time_iso():
  tokyo_time   = datetime.now(ZoneInfo("Asia/Tokyo")).replace(microsecond=0)
  iso_time_now =  tokyo_time.isoformat()
  return iso_time_now