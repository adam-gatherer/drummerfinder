# script to scrape joinmyband for drummers teehee
import urllib.request
from bs4 import BeautifulSoup
import re


# unused, depreciated, hated, reviled
def ad_scraper(url):
    drum_ad_list = []
    # url = 'https://www.joinmyband.co.uk/classifieds/scotland-east-f20.html'
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, 'html.parser')
    ad_list = (soup.find_all('a'))
    for a in ad_list:
        if 'drum' in str(a):
            a = (re.search('"(.*)"', str(a)).group(1))
            if 'classifieds' in a:
                a = a[13:]
            a = f'https://www.joinmyband.co.uk/classifieds/{a}'
            drum_ad_list.append(a)
    return drum_ad_list


def ad_scraper_v2(url):
    # url = 'https://www.joinmyband.co.uk/classifieds/scotland-east-f20.html'
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, 'html.parser')
    # ads = soup.find_all("p", {"class": "title"})
    ads = soup.find_all("div", {"class": re.compile('topic-row row.')})
    ad_list = []
    ad_dict = {}
    for a in ads:
        title = (re.search('(html"\>.*\<\/a)', str(a)).group(1))[6:-3]
        date_class = a.find("p", {"class": "small"})
        date = ((re.search('(small"\>.*by)', str(date_class)).group(1))[7:-3])
        location = (re.search('(\<span\>\(.*\)\<\/span\>)', str(a)).group(1)[6:-7])
        link = f"https://www.joinmyband.co.uk/classifieds/{((re.search('(href=.*html)', str(a)).group(1))[6:])}"
        # ad_list.append(link)
        ad_dict[link] = [title, location, date]
    return ad_dict


def page_2_maker(region_list):
    new_region_list = []
    for a in region_list:
        pg2 = '-s25.html'
        new_region_list.append(a)
        new_region_list.append(a[0:-5] + pg2)
    return new_region_list


def main():
    #
    # probably gonna break this up, there's a LOT going on in main
    #
    site = 'https://www.joinmyband.co.uk/'
    html_page = urllib.request.urlopen(site)
    soup = BeautifulSoup(html_page, 'html.parser')
    region_list = []
    ad_dicts_list = []
    # find the unordered list of links classed as "regions"
    region_links = soup.find_all("ul", class_="regions")
    # makes bs object 'regions' into a string, splits it by line to a list, chops off the <ul> and </ul> at start/end,
    # then cycles through the list items to strip the html part from the url to use later
    for a in (str(region_links[0]).split("\n"))[1:-1]:
        a = (re.search('(classifieds\/.*\.html)', str(a)).group(1))
        region_list.append(a)
    # split the countries
    region_list_scot = []
    region_list_ire = []
    region_list_wales = []
    region_list_engl = []
    for a in region_list:
        if 'scotland' in a:
            region_list_scot.append(a)
        elif 'ireland' in a:
            region_list_ire.append(a)
        elif 'wales' in a:
            region_list_wales.append(a)
        elif 'national' in a:
            None
        else:
            region_list_engl.append(a)
    region_list_scot = page_2_maker(region_list_scot)
    # cycle through regions in list and run ad_scraper on the ad page for said region
    for a in region_list_scot:
        if 's25' not in a:
            region_name = ((re.match('(.*-)', (a[12:])).group(1))[0:-1])
            print(10 * "=" + region_name.upper() + 10 * "=" + "\n")
        url = site + a
        a_dict = (ad_scraper_v2(url))
        for key, val in a_dict.items():
            if 'drum' in str(key).lower():
                None
                print(f'{val[0]}\n{val[1]}\n{val[2]}\n{key}\n')
        print("\n")

    counties = []
    for a in region_list_engl:
        # snips the full html page name thinger down to just the county by running a regex match for anything up to the
        # last -, then chopping the - off the end. Match is run against the string excluding the classifieds part
        counties.append((re.match('(.*-)', (a[12:])).group(1))[0:-1])


if __name__ == "__main__":
    # ad_scraper_v2()
    main()
