import xmltodict
import pyvips
import numpy as np


class GetROIdata:
    
    def __init__(self, slide_dir, slide_name):
        with open(slide_dir + slide_name + ".xml") as fd:
            self.slide_xml = xmltodict.parse(fd.read())
        
        self.img_vips = pyvips.Image.new_from_file(slide_dir + slide_name + ".svs", page=17, access='sequential')
        
        
    def get_roi_coordinates(self, region_idx:int)-> tuple:
        x = []; y = []
        for i in range(4):
            x.append(int(float(self.slide_xml['Annotations']['Annotation']['Regions']['Region'][region_idx]['Vertices']['Vertices'][i]['@X'])))
            y.append(int(float(self.slide_xml['Annotations']['Annotation']['Regions']['Region'][region_idx]['Vertices']['Vertices'][i]['@Y'])))
        return x,y

    
    def get_xywh(self, region_idx:int)-> tuple:
        x,y = self.get_roi_coordinates(region_idx)
        
        width = max(x) - min(x)
        height = max(y) - min(y)
        roi_center_x = (max(x) + min(x))//2
        roi_center_y = (max(y) + min(y))//2
        return roi_center_x, roi_center_y, width, height


    def get_patch(self, region_idx:int)-> np.ndarray:
        x,y,h,w = self.get_xywh(region_idx)
        patch_vips = self.img_vips.extract_area(x - w//2, y - h//2, w, h)
        patch = np.ndarray(buffer=patch_vips.write_to_memory(), dtype=np.uint8,
                           shape=[patch_vips.height, patch_vips.width, patch_vips.bands])
        return patch

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    