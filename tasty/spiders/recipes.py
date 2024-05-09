import scrapy
import re

class RecipesSpider(scrapy.Spider):
    name = "recipesspider"
    allowed_domains = ["tasty.co"]
    start_urls = ["https://tasty.co"]

    def parse(self, response):
        recipes = response.css("li.feed-item__6-col")
    
        for recipe in recipes: 
            image_url = recipe.css("div.feed-item__img img::attr(src)").get()
            yield {
                "title": recipe.css("div.feed-item__title::text").get(),
                "url": recipe.css("a").attrib['href'],
                "image_url": image_url
            }

            recipe_url = recipe.css("a").attrib['href']

            if recipe_url is not None:
                next_page_url = response.urljoin(recipe_url)
                yield response.follow(next_page_url, callback=self.parse_recipe)
            

    def parse_recipe(self, response):
        ingredients = response.css("li.ingredient").getall()
        ingredients = [re.sub('<.*?>', '', ingredient) for ingredient in ingredients]
        ingredients = [re.sub('<!--.*?-->', '', ingredient).strip() for ingredient in ingredients]
        
        nutritions = response.css("div.nutrition-details li").getall()
        nutritions = [re.sub('<[^<]+?>', '', nutrition).strip() for nutrition in nutritions]

        times = {}
        for div in response.css('div.recipe-time'):
            time_type = div.css('h5::text').get().split()[0].lower() + "Time"  
            time_value = div.css('p::text').get().strip() 
            times[time_type] = time_value


        preparation = response.css("div.preparation li::text").getall()
        yield {
            "title": response.css("h1.recipe-name::text").get(),
            "description": response.css("p.description::text").get(),
            "ingredients": ingredients,
            "preparation": preparation,
            "nutritions": nutritions
            "totalTime": times["totalTime"],
            "prepTime": times["prepTime"],
            "cookTime": times["cookTime"]
        }
