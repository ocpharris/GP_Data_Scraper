# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class GpscraperPipeline:
    def process_item(self, item, spider):
        print('@@@@@@@@@@@@@@')
        print('Pipeline executed.')
        adapter = ItemAdapter(item)
       
 
        field_names = adapter.field_names()

   
        # strip name 
        name_string = adapter.get('name')
        adapter['name'] = name_string.strip()


        # extract number of miles away 
        miles_away_string = adapter.get('miles_away')
        strip_miles_away_string = miles_away_string.strip()
        split_string_array = strip_miles_away_string.split(' ')
        adapter['miles_away'] = float(split_string_array[0])

        # 'this gp is currently accepting new patients' --> yes etc 
        accepting_patients_string = adapter.get('accepting_patients')
        split_accepting_patients_string = accepting_patients_string.split(' ')
        if split_accepting_patients_string[4] == 'not':
            adapter['accepting_patients'] = 'no'
        else:
            adapter['accepting_patients']= 'yes'

        not_available_keys = ['gp_website', 'phone_number']
        for not_available_key in not_available_keys:
            value = adapter.get(not_available_key)
            if value == None:
                adapter[not_available_key] = 'Not available'
        


        return item
