import waybackpy

url = "https://dlmf.nist.gov/"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) snap Chromium/74.0.3729.169 " \
             "Chrome/74.0.3729.169 Safari/537.36"

wayback = waybackpy.Url(url, user_agent)

total_archives = wayback.total_archives()
print(total_archives)


cdx = waybackpy.Cdx(url=url, user_agent=user_agent, start_timestamp=2020,
                    end_timestamp=2020)

snapshots = cdx.snapshots()

for snapshot in snapshots:
    print(snapshot.archive_url)
