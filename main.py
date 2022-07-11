# script to scrape joinmyband for drummers teehee
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def scrape_ads(url):
    # url = 'https://www.joinmyband.co.uk/classifieds/scotland-east-f20.html'
    html_page = urlopen(url)
    soup = BeautifulSoup(html_page, 'html.parser')
    ads = soup.find_all("div", {"class": re.compile('topic-row row.')})
    ad_dict = {}
    for ad in ads:
        # Finds ad title via <a href> tag, chops tags off start/end
        title = (re.search('(html"\>.*\<\/a)', str(ad)).group(1))[6:-3]
        date_tag = ad.find("p", {"class": "small"})
        # Finds ad date via small class, chops off end of opening <p> tag and removes "by {username}"
        date = ((re.search('(small"\>.*by)', str(date_tag)).group(1))[7:-3])
        # Finds location by searching for contents in parenthesis () between <span> tag, only one per ad
        location = (re.search('(\<span\>\(.*\)\<\/span\>)', str(ad)).group(1)[6:-7])
        link = f"https://www.joinmyband.co.uk/classifieds/{((re.search('(href=.*html)', str(ad)).group(1))[6:])}"
        ad_dict[link] = (title, location, date)
    return ad_dict


def generate_pg_2(regions):
    new_regions = []
    for region in regions:
        pg2 = '-s25.html'
        new_regions.append(region)
        new_regions.append(region[0:-5] + pg2)
    return new_regions


def split_regions(regions):
    scotland_regions = []
    ireland_regions = []
    wales_regions = []
    england_regions = []
    for region in regions:
        if 'scotland' in region:
            scotland_regions.append(region)
        elif 'ireland' in region:
            ireland_regions.append(region)
        elif 'wales' in region:
            wales_regions.append(region)
        elif 'national' in region:
            None
        else:
            england_regions.append(region)
    locations_by_region = {
        "scotland": scotland_regions,
        "ireland": ireland_regions,
        "wales": wales_regions,
        "england": england_regions,
    }
    return locations_by_region


def main():
    #
    # Probably gonna break this up, there's a LOT going on in main
    #
    site = 'https://www.joinmyband.co.uk/'
    html_page = urlopen(site)
    soup = BeautifulSoup(html_page, 'html.parser')
    all_regions = []
    # Find the unordered list of links classed as "regions"
    region_links = soup.find_all("ul", class_="regions")
    # Makes bs object 'regions' into a string, splits it by line to a list, chops off the <ul> and </ul> at start/end,
    # Then cycles through the list items to strip the html part from the url to use later
    for list_item in (str(region_links[0]).split("\n"))[1:-1]:
        # Finds the page address for each region by matching the start of the href target
        list_item = re.search('(classifieds\/.*\.html)', str(list_item)).group(1)
        all_regions.append(list_item)
    # Adds second page links to region page links
    all_regions = generate_pg_2(all_regions)
    # Splits all_regions into lists in the dictionary locations_by_region
    locations_by_region = split_regions(all_regions)
    for region in locations_by_region["scotland"]:
        #
        # old code, made redundant by generate_pg_2()
        #
        # if 's25' not in region:
        #    region_name = ((re.match('(.*-)', (region[12:])).group(1))[0:-1])
        # print(10 * "=" + region_name.upper() + 10 * "=" + "\n")
        url = site + region
        a_dict = (scrape_ads(url))
        for key, val in a_dict.items():
            if 'drum' in str(key).lower():
                None
                # print(f'{val[0]}\n{val[1]}\n{val[2]}\n{key}\n')
        # print("\n")

    # for key, val in locations_by_region.items():
    #     if "england" not in key:
    #         print(key)
    #         for region in val:
    #             print(region)
    #
    # Not sure how I'll use this, but England is unmanageable without further division. May go for North/South divide.
    #
    # counties = []
    # for a in locations_by_region["england"]:
    #     # snips the full html page name thinger down to just the county by running a regex match for anything up to
    #     # the last -, then chopping the - off the end. Match is run against the string excluding the classifieds part
    #     trunc = (re.search('(.*-f)', (a[12:])).group(1))[0:-2]
    #     if trunc not in counties:
    #        counties.append(trunc)


if __name__ == "__main__":
    # ad_scraper_v2()
    main()
