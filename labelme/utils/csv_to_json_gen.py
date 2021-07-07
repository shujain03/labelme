import csv
import cv2
import os
import json


def generate_json_using_csv(global_csv_dict, dirListPath, progress):
    '''
        goes to the target path
        generates the .json files to create polygon around the doi locations
        '''
    # parse through self.dirListPaths
    # generate respective json
    if global_csv_dict is None:
        return
    offset = 5
    directory_count = len(dirListPath)
    for index, each_dir in enumerate(dirListPath):
        json_dict = {}
        json_dict['version'] = '4.5.7'
        json_dict['flags'] = {}
        json_dict['shapes'] = []  # list of dicts
        json_dict['imagePath'] = ''
        json_dict['imageData'] = None
        json_dict['imageHeight'] = 4084
        json_dict['imageWidth'] = 480
        cur_dir_code = each_dir.split('/')[-2]
        if cur_dir_code in global_csv_dict:
            pass
        else:
            continue
        print(cur_dir_code)
        print(each_dir)
        print(global_csv_dict[cur_dir_code])
        progress_percentage = (index + 1) * 100 / directory_count
        print(progress_percentage)
        progress.setValue(progress_percentage)

        # a given directory may have more than 1 doi
        # iterate through each doi (csv_data_dict)
        for csv_data_dict in global_csv_dict[cur_dir_code]:
            x_loc = int(csv_data_dict['loc_x'])
            y_loc = int(csv_data_dict['loc_y'])

            pt1 = [x_loc - offset, y_loc - offset]
            pt2 = [x_loc + offset, y_loc - offset]
            pt3 = [x_loc + offset, y_loc]
            pt4 = [x_loc + offset, y_loc + offset]
            pt5 = [x_loc - offset, y_loc + offset]
            pt6 = [x_loc - offset, y_loc]
            frame_id = str(int(csv_data_dict['frame_id']))
            img_fname = 'BrightField_TDI_Frame' + str(frame_id) + '(of3).png'
            json_fname = 'BrightField_TDI_Frame' + str(frame_id) + '(of3).json'
            img = cv2.imread(each_dir + '/' + img_fname, 0)
            imageHeight = img.shape[0]
            imageWidth = img.shape[1]
            json_dict['imageHeight'] = img.shape[0]
            json_dict['imageWidth'] = img.shape[1]
            json_dict['imagePath'] = img_fname
            json_dict['imageData'] = None

            if os.path.exists(each_dir + '/' + json_fname) is False:

                # json_dict['shapes'] a list of dictionaries
                # a given shape is a dictionary
                new_shape_dict = {}
                new_shape_dict['label'] = '1'  # assume it is 1 always
                new_shape_dict['group_id'] = None  # assume it is None
                new_shape_dict['shape_type'] = 'polygon'  # assume polygon
                new_shape_dict['flags'] = {}  # assume no flags
                new_shape_dict['points'] = [pt1, pt2, pt3, pt4, pt5, pt6]

                # add a single new_shape_dict
                json_dict['shapes'] = [new_shape_dict]
                # write dictionary to disk in form of a json
                with open(each_dir + '/' + json_fname, 'w') as outfile:
                    json.dump(json_dict, outfile, indent=4)
            else:
                # already exists, just append to the shapes list
                new_shape_dict = {}
                new_shape_dict['label'] = '1'  # assume it is 1 always
                new_shape_dict['group_id'] = None  # assume it is None
                new_shape_dict['shape_type'] = 'polygon'  # assume polygon
                new_shape_dict['flags'] = {}  # assume no flags
                new_shape_dict['points'] = [pt1, pt2, pt3, pt4, pt5, pt6]
                # read the current json
                fp = open(each_dir + '/' + json_fname, 'r')
                json_dict = json.load(fp)
                fp.close()
                if new_shape_dict not in json_dict['shapes']:
                    json_dict['shapes'].append(new_shape_dict)
                with open(each_dir + '/' + json_fname, 'w') as outfile:
                    json.dump(json_dict, outfile, indent=4)
                pass
            print('--')
    # draw a polygon shape


def generate_mapping_from_csv(csv_file_name):
    # csv_file_name = 'KlarfMapping.csv'
    # csv_data_dict = {}
    global_dict = {}
    with open(csv_file_name, newline='') as csv_file_fp:
        csv_reader = csv.reader(csv_file_fp, delimiter=',')
        # store the headers in a separate variable,
        # move the reader object to point on the next row
        headings = next(csv_reader)
        # headers = ['defect_id', 'folder_id', 'frame_id', 'loc_x', 'loc_y']

        for each_row in csv_reader:
            # print(each_row)
            # data_list = each_row.split(',')
            cur_dict = {}
            cur_dict['defect_id'] = each_row[0]
            cur_dict['folder_id'] = each_row[1]
            cur_dict['frame_id'] = each_row[2]
            cur_dict['loc_x'] = each_row[3]
            cur_dict['loc_y'] = each_row[4]
            # if this folder already exists in global_dict, append else create
            if each_row[1] not in global_dict:
                global_dict[each_row[1]] = [cur_dict]
            else:
                global_dict[each_row[1]].append(cur_dict)
        # print(list(global_dict.keys()))
    return global_dict


if __name__ == '__main__':
    global_dict = generate_mapping_from_csv(csv_file_name='KlarfMapping.csv')
    generate_json_using_csv(global_dict)
