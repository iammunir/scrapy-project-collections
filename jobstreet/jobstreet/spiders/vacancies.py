import scrapy


class VacanciesSpider(scrapy.Spider):
    name = 'vacancies'
    allowed_domains = ['www.jobstreet.co.id']
    start_urls = [
        'https://www.jobstreet.co.id/id/job-search/job-vacancy/1/?ojs=1']

    def parse(self, response):
        cards = response.xpath(
            "//div[@class='FYwKg _31UWZ fB92N_1 _1pAdR_1 FLByR_1 _2QIfI_1 _2cWXo _1Swh0 HdpOi']")
        for card in cards:
            title = card.xpath(".//div/div[2]/h1/a/div/text()").get()
            link = response.urljoin(card.xpath(
                ".//div/div[2]/h1/a/@href").get())
            company = card.xpath(
                ".//div/div[2]/span/text()").get() or "Perusahaan dirahasiakan"

            yield {
                'title': title,
                'link': link,
                'company': company,
            }
            # yield response.follow(url=link, callback=self.parse_detail, meta=data_init)

        next_page = response.xpath(
            "//div[@class='FYwKg _20Cd9 _36UVG_1']/div/a/@href").get()

        if next_page:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    def parse_detail(self, response):
        title = response.request.meta['title']
        company = response.request.meta['company']

        location = response.xpath(
            "//div[@class='FYwKg d7v3r _3122U_1']/div[1]/div/span/text()").get()
        date = response.xpath(
            "//div[@class='FYwKg d7v3r _3122U_1']/div[2]/span/text()").get()
        job_categories = response.xpath(
            "//div[@class='FYwKg _2cWXo _194Ob _3gDk-_1']/div[5]/div/div/div[2]/span/a/text()").getall()

        yield {
            'title': title,
            'company': company,
            'location': location,
            'date': date,
            'categories': job_categories
        }
