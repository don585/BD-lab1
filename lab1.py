#!/usr/bin/python
# -*- coding:cp866 -*-

import requests
import lxml.etree as etree


def task1():
    count = 1
    URL = 'http://www.ukr.net/'
    root = etree.Element("root")
    doc = etree.SubElement(root, "data")
    tree = etree.HTML(requests.get(URL).text)
    urls = tree.xpath('/html/body//a//@href')

    for url in urls:
        if url.find('www.ukr.net/') != -1 and url.find('javascript') == -1 and count <= 20:
            #print("http:"+url)
            tree = etree.HTML(requests.get("http:"+url).text)
            img = tree.xpath('/html/body//img//@src')
            text = tree.xpath('/html/body//a//text()')
            #text1 = tree.xpath('/html/body//a[@class="CadetBlueLink"]')
            text2 = tree.xpath('/html/body//a[@class="im-tl_a"]')
            el = etree.SubElement(doc, "page", url=url)
            for i in img:
               etree.SubElement(el, "fragmemt", type="image").text = i
            for i in text:
                etree.SubElement(el, "fragment", type="text").text= i
            for i in text2:
                etree.SubElement(el, "fragment", type="text").text = i.text
            count += 1
    tree = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)
    f = open("task1.xml","w",  encoding='utf-8')
    print(tree.decode('cp866'), file=f)
    f.close()
    return ("Task1 done")


def task2():
    tree = etree.parse('task1.xml')
    count2 = 0
    nodes = tree.xpath('/root/data//page') # Открываем раздел
    for node in nodes:
        elements = node.xpath('.//*[@type="text"]/text()')
        for el in elements:
            count2 += 1
    print("Everage amount:  "+str(int(count2/20)))
    return ("Task2 done")


def task3():
    url = "https://repka.ua/products/noutbuki/filters/class-geymerskie/?view=grid"
    root = etree.Element("root")
    tree = etree.HTML(requests.get(url).text)
    doc = etree.SubElement(root, "data")
    name = tree.xpath('//*[@class="catalog-product-name"]/a/text()')
    image = tree.xpath('//*[@class="catalog-product-images"]/a/img[1]/@src')
    price = tree.xpath('//*[@class="price-uah"]/span/text()' )

    for i in range(len(name)):
        node = etree.SubElement(doc, 'product', id = str(i+1))
        etree.SubElement(node, 'name').text = name[i]
        etree.SubElement(node, 'price').text = price[i]
        etree.SubElement(node, 'image').text = image[i]
    tree = etree.tostring(root, pretty_print = True, encoding = 'utf-8', xml_declaration = True)
    f = open("task3.xml","w", encoding="utf-8")
    print(tree.decode('utf-8'), file=f)
    f.close()
    return ("Task3 done")


def task4():
    data = open('task4.xsl')
    xslt_content = data.read()
    xslt_content = xslt_content.encode('ascii')
    xslt_root = etree.XML(xslt_content)
    dom = etree.parse('task3.xml')
    transform = etree.XSLT(xslt_root)
    result = transform(dom)
    f = open('result.html', 'w')
    f.write(str(result))
    f.close()
    return ("Task4 done")


task1()
task2()
task3()
task4()



