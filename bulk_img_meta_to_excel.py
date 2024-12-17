import os
from PIL import (Image)
import piexif
from GPSPhoto import gpsphoto
import operator
import pandas as pd

codec = 'ISO-8859-1'  # or latin-1


def exif_to_tag(exif_dict):
    exif_tag_dict = {}
    thumbnail = exif_dict.pop('thumbnail')
    if thumbnail:
        exif_tag_dict['thumbnail'] = thumbnail.decode(codec)

    for ifd in exif_dict:
        exif_tag_dict[ifd] = {}
        for tag in exif_dict[ifd]:
            try:
                element = exif_dict[ifd][tag].decode(codec)

            except AttributeError:
                element = exif_dict[ifd][tag]

            exif_tag_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element

    return exif_tag_dict


# Freshly imports images
def get_image_meta_data(dir_path):
    arr = []
    img_dir = os.fsencode(dir_path)

    for file in os.listdir(img_dir):
        filename = os.fsdecode(file)
        if filename.endswith('.jpg') or filename.endswith('.JPEG'):
            # save to db
            image = Image.open(os.path.join(dir_path, filename))

            try:
                exif_dict = piexif.load(image.info.get('exif'))
                exif_dict = exif_to_tag(exif_dict)

                gps = exif_dict['GPS']
                date = exif_dict['0th']['DateTime']

                if not gps:
                    raise ValueError('Missing GPS data')
                else:
                    coords = gpsphoto.getGPSData(os.path.join(dir_path, filename))

                    img_meta = {
                        'name': filename,
                        'date': date,
                        'lat': coords['Latitude'],
                        'lng': coords['Longitude'],
                    }

                    arr.append(img_meta)

            except Exception as error:
                #print('Error: ', error)
                #print('Skipping ', filename, '...')
                pass
        else:
            continue

    return arr


def generate_thumbnails(input_dir, output_dir):
    MAX_SIZE = (100, 100)

    print('Start Cleanup')

    if not os.path.exists(output_dir + '/dialog_thumb'):
        os.makedirs(output_dir + '/dialog_thumb')

    # clean up output dir
    # for file in os.listdir(output_dir + '/dialog_thumb'):
    #     print('Delete: ' + file)
    #     os.remove(output_dir + '/dialog_thumb/' + file)

    print('Generate Thumbnails')
    for file in os.listdir(input_dir):
        filename = os.fsdecode(file)
        if filename.endswith('.jpg') or filename.endswith('.JPEG'):
            # save to db
            image = Image.open(os.path.join(input_dir, filename))
            image.thumbnail(MAX_SIZE)
            image.save(os.path.join(output_dir + '/dialog_thumb', filename))
            print('Save Thumbnail ' + file)

def export_excel(input_dir_path, output_dir_path):
    generate_thumbnails(input_dir_path, output_dir_path)
    arr = get_image_meta_data(input_dir_path)
    print(arr)
    arr.sort(key=operator.itemgetter('date', 'lat', 'lng'))
    print(arr)

    df = pd.DataFrame(arr)

    writer = pd.ExcelWriter(output_dir_path + '/output.xlsx', engine='xlsxwriter')

    df.to_excel(writer, sheet_name='data')

    worksheet = writer.sheets['data']

    for i in range(len(arr)):
        worksheet.insert_image('F' + str(i + 2), output_dir_path + '/dialog_thumb/' + arr[i]['name'])
        # if i > 400:
        #     break

    writer.book.close()
