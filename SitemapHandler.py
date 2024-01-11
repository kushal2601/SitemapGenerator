import xml.etree.ElementTree as ET
from createSitemap import generate_sitemap, get_sitemap_element, get_url_element

def add_url_to_sitemap(url, urlIndex):
    ET.register_namespace("","http://www.sitemaps.org/schemas/sitemap/0.9")
    sitemapIndex = urlIndex//50000
    if urlIndex % 50000 == 0:
        # Crate a new sitemap file with fileName = "sitemap{sitemapIndex}.xml"
        fileName = f"sitemap{sitemapIndex}.xml"
        generate_sitemap(fileName)

        #Also add it to sitemapIndex file
        tree = ET.parse("sitemap_index.xml")
        root = tree.getroot()

        new_sitemap_element = get_sitemap_element(fileName)
        root.append(new_sitemap_element)

        # Write back the updated siemapindex file to the same location
        tree.write("sitemap_index.xml",encoding="utf-8", xml_declaration=True)
        # print(f"New sitemap file named sitemap{sitemapIndex}.xml is created and  added to sitemap_index.xml")
    sitemap_fileName = f"sitemap{sitemapIndex}.xml" 
    tree = ET.parse(sitemap_fileName)
    root = tree.getroot()

    url_element = get_url_element(url)

    root.append(url_element)
    tree.write(sitemap_fileName, encoding="utf-8", xml_declaration=True)
    # print(f"Added the url to the sitemap{sitemapIndex}.xml")
    # print("url added successfully to sitemapfile")

add_url_to_sitemap("http://kushalswebiste.com",0)