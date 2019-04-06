from lxml import etree
import requests

BASE_DOMAIN = 'https://dytt8.net'
HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)\
	AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0\
	.2743.116 Safari/537.36',
	'Accept-Language': 'zh-CN,zh;q=0.8'
}
#获取构造下载电影的链接
def get_detail_urls(url):
	response = requests.get(url,headers=HEADERS)
	text = response.text
	html = etree.HTML(text)
	detail_urls = html.xpath('//table[@class="tbspan"]//a/@href')
	detail_urls = map(lambda url:BASE_DOMAIN + url,detail_urls)
	return detail_urls

def parse_detail_page(url):
	movie = {}
	response = requests.get(url,headers=HEADERS)
	text = response.content.decode('gbk')
	html = etree.HTML(text)
	title = html.xpath('//div[@class="title_all"]//font[@color="#07519a"]/text()')[0]
	movie['title'] = title
	zoomE = html.xpath('//div[@id="Zoom"]')[0]
	imgs = zoomE.xpath(".//img/@src")
	cover = imgs[0]
	screenshot = imgs[1]
	movie["cover"] = cover
	movie["screenshot"] = screenshot

	def parse_info(info,rule):
		return info.replace(rule,"").strip()
	infos = zoomE.xpath('.//text()')
	for index,info in enumerate(infos):
		if info.startswith("◎年　　代"):
			info = parse_info(info,"◎年　　代")
			movie['year'] = info
		elif info.startswith("◎产　　地"):
			info = parse_info(info,"◎产　　地")
			movie['origin'] = info
		elif info.startswith("◎视频尺寸"):
			info = parse_info(info,"◎视频尺寸")
			movie['size'] = info
		elif info.startswith("◎主　　演"):
			info = parse_info(info,"◎主　　演")
			actors = [info]
			for x in range(index+1,len(infos)):
				actor = infos[x].strip()
				if actor.startswith("◎"):
					break
				actors.append(actor)
			movie['actors'] = actors
	download_url = html.xpath('//td[@bgcolor="#fdfddf"/a/@href]')[0]
	movie['download_url'] = download_url
	return movie


#获取构造要下载的页数链接
def main():
	base_url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_1.html'
	movies = []
	for x in range(1,8):
		url = base_url.format(x)
		detail_urls = get_detail_urls(url)
		for detail_url in detail_urls:
				#遍历一页里面所有电影的详情url
			movie = parse_detail_page(detail_url)
			movies.append(movie)
			print(movie)
if __name__ == '__main__':
	main()