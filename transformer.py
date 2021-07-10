import os

from objectmapper import ObjectMapper
from reader import Reader


class Transformer(object):
    def __init__(self, xml_dir, out_dir, id_Person = 0, id_Officer = 0, id_Clear_head = 0, id_Mask_head = 0,
                 id_Help = 0, id_Unclear_head = 0, id_Wheel_chair = 0, id_fall=0, id_fight=0, id_Red_Light=0):
        self.xml_dir = xml_dir
        self.out_dir = out_dir

        self.id_Person_ = id_Person
        self.id_Officer_ = id_Officer
        self.id_Clear_head_ = id_Clear_head
        self.id_Mask_head_ = id_Mask_head
        self.id_Help_ = id_Help
        self.id_Unclear_head_ = id_Unclear_head
        self.id_Wheel_chair_ = id_Wheel_chair
        self.id_fall_ = id_fall
        self.id_fight_ = id_fight
        self.id_Red_Light_ = id_Red_Light

    def transform(self):
        reader = Reader(xml_dir=self.xml_dir)
        xml_files = reader.get_xml_files()
        classes = reader.get_classes()
        object_mapper = ObjectMapper()
        annotations = object_mapper.bind_files(xml_files, xml_dir=self.xml_dir)
        self.write_to_txt(annotations, classes)

    def write_to_txt(self, annotations, classes):
        for annotation in annotations:
            output_path = os.path.join(self.out_dir, self.darknet_filename_format(annotation.filename))
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))
            with open(output_path, "w+") as f:
                f.write(self.to_darknet_format(annotation, classes))

    def to_darknet_format(self, annotation, classes):
        result = []
        for obj in annotation.objects:
            # print(classes)
            # replace wrong lable
            if obj.name == 'play_phone':
                obj.name = obj.name.replace("play_phone", "body_play_phone")
            if obj.name == 'body_call':
                obj.name = obj.name.replace("body_call", "body_play_phone")
            elif obj.name == 'sleep':
                obj.name = obj.name.replace("sleep", "body_sleep")
            # elif obj.name == 'face_sleep':
            #     obj.name = obj.name.replace("face_sleep", "body_sleep")
            elif obj.name == 'suspected_play_phone':
                obj.name = obj.name.replace("suspected_play_phone", "body_suspected_play_phone")
            elif obj.name == 'no_mask':
                obj.name = obj.name.replace("no_mask", "face_no_mask")
            elif obj.name == 'body_body_no_mask':
                obj.name = obj.name.replace("body_body_no_mask", "face_no_mask")
            elif obj.name == 'body_no_mask':
                obj.name = obj.name.replace("body_no_mask", "face_no_mask")
            elif obj.name == 'face_body_no_mask':
                obj.name = obj.name.replace("face_body_no_mask", "face_no_mask")
            elif obj.name == 'body_body_no_mask':
                obj.name = obj.name.replace("body_body_no_mask", "face_no_mask")
            elif obj.name == 'eat_something':
                obj.name = obj.name.replace("eat_something", "body_eating")
            elif obj.name == 'wear_staff_card':
                obj.name = obj.name.replace("wear_staff_card", "body_wear_staff_card")
            elif obj.name == 'staff_card':
                obj.name = obj.name.replace("staff_card", "card")
            if obj.name not in classes:
                print('obj.name not in classes:')
                print(annotation.filename, obj.name, classes)
                print('\n')
                # print('not exist:', obj.name, annotation.filename)

            #  查看各ID对应的数量，注意在保存为txt时，将以下内容注释掉
            # -----------------------------------------
            # if obj.name == 'play_phone':
            #     self.id_Person_ += 1
            # elif obj.name == 'phone':
            #     self.id_Officer_ += 1
            # elif obj.name == 'sleep':
            #     self.id_Clear_head_ += 1
            # elif obj.name == 'suspected_play_phone':
            #     self.id_Mask_head_ += 1
            # elif obj.name == 'no_mask':
            #     self.id_Help_ += 1
            # elif obj.name == 'body_gathering':
            #     self.id_Unclear_head_ += 1
            # elif obj.name == 'eat_something':
            #     self.id_Wheel_chair_ += 1
            # elif obj.name == 'food':
            #     self.id_fall_ += 1
            # elif obj.name == 'wear_staff_card':
            #     self.id_fight_ += 1
            # elif obj.name == 'staff_card':
            #     self.id_Red_Light_ += 1
            # ------------------------------------------
            else:
                x, y, width, height = self.get_object_params(obj, annotation.size)  # 归一化的坐标
                result.append("%d %.6f %.6f %.6f %.6f" % (classes[obj.name], x, y, width, height))

                # x0, y0, x1, y1 = self.get_x0y0x1y1(obj, annotation.size)
                # info = str(obj.name) +' '+ str(x0) +' '+ str(y0) +' '+ str(x1) +' ' +str(y1)
                # print(info)
                # result.append(info)

                # print(annotation.filename)

            # print(self.id_Mask_head_,  self.id_Clear_head_, self.id_Unclear_head_, self.id_Help_,
            #       self.id_Person_, self.id_Officer_, self.id_Wheel_chair_,
            #       self.id_fall_, self.id_fight_, self.id_Red_Light_)

            # print('各个类别的数量如下：')
            # print('play_phone、phone、sleep、suspected_play_phone、no_mask、eat_something、'
            #       'food、wear_staff_card、staff_card')
            # print(self.id_Mask_head_,  self.id_Clear_head_, self.id_Help_,
            #       self.id_Person_, self.id_Officer_, self.id_Wheel_chair_,
            #       self.id_fall_, self.id_fight_, self.id_Red_Light_)
            # print('OK!')
        return "\n".join(result)

    @staticmethod
    def get_object_params(obj, size):
        try:
            # image_width = 1.0 * size.width
            # image_height = 1.0 * size.height
            image_width = 1280
            image_height = 720

            box = obj.box
            absolute_x = box.xmin + 0.5 * (box.xmax - box.xmin)

            absolute_y = box.ymin + 0.5 * (box.ymax - box.ymin)

            absolute_width = box.xmax - box.xmin
            absolute_height = box.ymax - box.ymin

            x = absolute_x / image_width
            y = absolute_y / image_height
            width = absolute_width / image_width
            height = absolute_height / image_height

            return x, y, width, height

        except:
            print(obj)
            pass

    @staticmethod
    def get_x0y0x1y1(obj, size):
        try:
            image_width = 1.0 * size.width
            image_height = 1.0 * size.height

            box = obj.box
            # absolute_x = box.xmin + 0.5 * (box.xmax - box.xmin)
            #
            # absolute_y = box.ymin + 0.5 * (box.ymax - box.ymin)
            #
            # absolute_width = box.xmax - box.xmin
            # absolute_height = box.ymax - box.ymin
            #
            # x = absolute_x / image_width
            # y = absolute_y / image_height
            # width = absolute_width / image_width
            # height = absolute_height / image_height

            return int(box.xmin), int(box.ymin), int(box.xmax), int(box.ymax)


        except:
            print(obj)
            pass


    @staticmethod
    def darknet_filename_format(filename):
        pre, ext = os.path.splitext(filename)
        return "%s.txt" % pre

if __name__ == '__main__':
    xmldir = 'xml'
    outdir = 'out'
    Transformer(xmldir, outdir)
    print('ok')
