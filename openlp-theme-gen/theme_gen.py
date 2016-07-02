import argparse, zipfile, os, lxml.etree as ET


def calc_name(filename):
    base = os.path.basename(filename)
    raw = os.path.splitext(base)[0]
    spaced = raw.replace('_', ' ').replace('-', ' ')
    return spaced.title()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--border_color', default='#000000')
    parser.add_argument('theme_template_file')
    parser.add_argument('img_file', nargs='+')
    parsed = parser.parse_args()

    with zipfile.ZipFile(parsed.theme_template_file) as theme_folder:
        contents = theme_folder.filelist
        assert len(contents) > 0, 'Expected at least one file'
        template_name = os.path.dirname(contents[0].filename)
        desired_filename = os.path.join(template_name, template_name + '.xml')
        xml_bytes = theme_folder.read(desired_filename)
        root = ET.fromstring(xml_bytes)

    name = root[0]
    assert name.tag == 'name', 'Expected <name> tag to be first'
    background = root[1]
    assert background.tag == 'background', 'Expected <background> tag to be second'
    background.clear()
    background.attrib['type'] = 'image'
    filename = ET.SubElement(background, 'filename')
    bordercolor = ET.SubElement(background, 'borderColor')
    bordercolor.text = parsed.border_color

    print('Generating', len(parsed.img_file), 'themes with template',  template_name, '...')
    for img in parsed.img_file:
        # TODO: Need to catch exception, output nice message and continue on.
        theme_name = calc_name(img)
        print(theme_name + ":")
        name.text = theme_name
        img_base = os.path.basename(img)
        filename.text = img_base
        # Don't know why but pretty_print does not seem to work for custom 'background' element
        content = ET.tostring(root, encoding="UTF-8", xml_declaration=True, pretty_print=True)

        with zipfile.ZipFile(theme_name + '.otz', "w", zipfile.ZIP_DEFLATED) as op_zip:
            op_zip.writestr(os.path.join(theme_name, theme_name + ".xml"), content)
            op_zip.write(img, os.path.join(theme_name, img_base))

    print("Done.")


if __name__ == "__main__":
    main()