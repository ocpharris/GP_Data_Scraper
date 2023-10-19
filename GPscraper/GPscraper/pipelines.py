# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class GpscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
       
 
        field_names = adapter.field_names()


        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value.strip()
   

        # name_string = adapter.get('name')
        # adapter['name'] = name_string.strip()
       

        # # Catergory & Product Type --> switch to lowercase
        # lowercase_keys = ['category', 'product_type']
        # for lowercase_key in lowercase_keys:
        #     value = adapter.get(lowercase_key)
        #     adapter[lowercase_key] = value.lower()



        # extract number of miles away 
        miles_away_string = adapter.get('miles_away')
        strip_miles_away_string = miles_away_string.strip()
        split_string_array = strip_miles_away_string.split(' ')
        adapter['miles_away'] = float(split_string_array[0])

        # # Reviews --> convert string to integer
        # num_reviews_string = adapter.get('num_reviews')
        # adapter['num_reviews'] = int(num_reviews_string)


        # # Stars --> convert text to number 
        # star_string = adapter.get('stars')
        # split_stars_array = star_string.split(' ')
        # stars_text_value = split_stars_array[1].lower()
        # if stars_text_value == "zero":
        #     adapter['stars'] = 0
        # elif stars_text_value == "one":
        #     adapter['stars'] = 1
        # elif stars_text_value == "two":
        #     adapter['stars'] = 2
        # elif stars_text_value == "three":
        #     adapter['stars'] = 3
        # elif stars_text_value == "four":
        #     adapter['stars'] = 4
        # elif stars_text_value == "five":
        #     adapter['stars'] = 5
    


        return item
