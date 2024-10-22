class Rating_System:
    def __init__ (self):
        #should initialize the multiple category system
        #param categories: a list of the categories being rated by the user

        self.categories = ["Location", "Parking", "Merch", "Sound Quality", "Set List", "Ticket Price", "Facilities", "Security"]
        self.ratings = {category: None for category in self.categories}

    def rate(self, category, stars):
        #param category:
        #param stars:
        #raises ValueError: if the rating isn't between 1 and 5
        if category not in self.categories:
            raise ValueError(f"Invalid Category: {category}. Choose from {self.categories}")
        if stars < 1 or stars > 5:
            raise ValueError(f"Rating must be in between 1 star and 5 stars.")
        self.ratings[category] = stars
        print(f"Rated {category}: {stars} stars.")

    def average_rating(self):
        #calculates the average rating of all categories.
        #returns average rating as a float , or None if no criteria are rated.

        rated_category = [rating for rating in self.ratings.values() if rating is not None]
        if not rated_category:
            return None
        return sum(rated_category) / len(rated_category)
    
    def display_ratings(self): #displays the ratings for all categories
        for category, rating in self.ratings.items():
            if rating is not None:
                print(f"{category}: {rating} stars")
            else:
                print(f"{category}: Not rated")