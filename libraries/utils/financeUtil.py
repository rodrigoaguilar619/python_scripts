
def calculate_percentage_increase(current_price, target_price):
    percentage_increase = ((target_price - current_price) / current_price) * 100
    return percentage_increase

def calculate_average_rating(strong_buy, buy, hold, sell, strong_sell):
    # Define the numerical values for each recommendation type
    ratings = {
        'Strong Buy': 5,
        'Buy': 4,
        'Hold': 3,
        'Sell': 2,
        'Strong Sell': 1
    }
    
    # Calculate the weighted average
    total_recommendations = strong_buy + buy + hold + sell + strong_sell
    total_weighted_score = (ratings['Strong Buy'] * strong_buy + 
                            ratings['Buy'] * buy + 
                            ratings['Hold'] * hold + 
                            ratings['Sell'] * sell + 
                            ratings['Strong Sell'] * strong_sell)
    
    # Compute the average rating
    average_rating = total_weighted_score / total_recommendations
    
    # Classify based on the average rating
    if average_rating <= 1.5:
        classification = "Strong Sell"
    elif average_rating <= 2.5:
        classification = "Sell"
    elif average_rating <= 3.5:
        classification = "Hold"
    elif average_rating <= 4.5:
        classification = "Buy"
    else:
        classification = "Strong Buy"
    
    return average_rating, classification