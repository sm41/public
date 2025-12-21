from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import locale
from os      import getenv, environ, path, makedirs
import re
import tver_tool
from feedgen.feed import FeedGenerator
import urllib.parse

url = "https://service-api.tver.jp/api/v1/callNewerDetail/drama"

headers = {
  "x-tver-platform-type": "web"
}

rrr = urllib.parse.urlparse("https://tver.jp/")

locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
data = tver_tool.request_get(url, headers)
iso_time_now = tver_tool.time_iso()

contents = data['result']['contents']['contents']

def check_conditions(item):
  c = item['content']

  return {
    "ribbon"  : (c['ribbonID'] != 0),
    "bs"      : bool(re.match('(BS|ＢＳ)', c['productionProviderName'])),
    "year"    : bool(re.match('[0-9]{4}年', c['broadcastDateLabel'])),
    "ck"      : bool(re.match('(中国|.?韓)', c['seriesTitle'])),
    "comment" : bool(re.search('解説放送', c['title'])),
  }

def call_new():
  month_day_items = []
  blocked_items   = []
  year_items      = []

  for item in reversed(contents):

    conds = check_conditions(item)  # ← 全部の True/False を取る

    if conds['ck'] or conds['bs'] or conds['ribbon'] or conds['comment']:
      blocked_items.append({
        "item": item,
        "conditions": conds,
      })
      continue

    if conds['year']:
      year_items.append({
        "item": item,
        "conditions": conds,
      })

    if not conds['year']:
      month_day_items.append({
        "item": item,
        "conditions": conds,
      })

  return blocked_items, month_day_items, year_items


def process_items(lilili:list):

  workspace = getenv("GITHUB_WORKSPACE")
  home_dir  = getenv("HOME")

  path_to_use = workspace if workspace else home_dir
  publish_dir = "docs"
  middle_dir  = "feed"

  atom_dir = path.join(path_to_use, publish_dir, middle_dir, "tver")

  makedirs(atom_dir, exist_ok=True)

  for ddd in lilili:

    feed_title  = ddd['title']
    filename_id = ddd['filename_id']

    fg = FeedGenerator()
    fg.id("https://tver.jp/")
    fg.title(feed_title)
    # fg.icon("https://tver.jp/favicon.ico")
    fg.updated(iso_time_now)
    fg.link(href="https://sm41.github.io/public/")
    fg.author({
      "name": "John Doe",
      "email": "john@example.com"
      }
    )

    for item in ddd['items']:
      series_title             = item['item']['content']['seriesTitle']
      # series_id                = item['item']['content']['seriesID']
      episode_title            = item['item']['content']['title']
      episode_id               = item['item']['content']['id']
      broadcast_date           = item['item']['content']['broadcastDateLabel']
      production_provider_name = item['item']['content']['productionProviderName']

      start_jst                = datetime.fromtimestamp(item['item']['startAt'], ZoneInfo("Asia/Tokyo"))
      start_iso                = start_jst.isoformat()
      start_date               = start_jst.strftime("%Y年%m月%d日(%a)-%H時%M分")

      end_jst                  = datetime.fromtimestamp(item['item']['endAt'], ZoneInfo("Asia/Tokyo"))
      # end_iso                  = end_jst.isoformat()
      end_date                 = end_jst.strftime("%Y年%m月%d日(%a)-%H時%M分")

      # series_images            = f"https://image-cdn.tver.jp/images/content/thumbnail/series/xlarge/{series_id}.jpg"
      episode_images           = f"https://image-cdn.tver.jp/images/content/thumbnail/episode/xlarge/{episode_id}.jpg"

      # sss = tver_tool.get_description(series_id)
      # sss.request_get()

      eee = tver_tool.get_description(episode_id)
      eee.request_get()

      lb = tver_tool.line_break()
      lb.lb_html(eee.data['description'])
      hhh = lb.lb_html_str

      # html = tver_tool.gen_html(episode_images, episode_title, hhh, start_at, end_at, broadcast_date, production_provider_name)
      html = tver_tool.gen_html(episode_images, hhh, start_date, end_date, broadcast_date, production_provider_name)


      fe = fg.add_entry()
      fe.id(f"https://tver.jp/episodes/{episode_id}")
      fe.title(f"{series_title}_[{episode_title}]")
      fe.updated(start_iso)
      fe.content(html)
      fe.link(href=f"https://tver.jp/episodes/{episode_id}")

    atom_file = f"newer_{filename_id}.atom"
    atom_path = path.join(atom_dir, atom_file)

    if workspace:
      with open(environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"filename_id={filename_id}\n")

    atom_xml  = fg.atom_str(pretty=True)

    with open(atom_path, "wb") as f:
      f.write(atom_xml)



def main():
  blocked_items, month_day_items, year_items = call_new()

  ready = [
    {
      "title"        : "新着/ドラマ/year",
      "filename_id"  : "year",
      "items"        : year_items
    },
    {
      "title"        : "新着/ドラマ/month",
      "filename_id"  : "month",
      "items"        : month_day_items
    }
  ]

  process_items(ready)


if __name__ == '__main__':
  main()