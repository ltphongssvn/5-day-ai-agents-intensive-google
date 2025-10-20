def place_pizza_order(size: str, crust: str, toppings: list[str]) -> str:
    """
    Places the final pizza order once all information is collected.
    
    You MUST NOT call this function until you have the size,
    the crust type, and at least one topping.
    
    Args:
        size (str): The size of the pizza (e.g., "large", "medium").
        crust (str): The type of crust (e.g., "thin", "stuffed").
        toppings (list[str]): A list of toppings (e.g., ["pepperoni", "mushrooms"]).
        
    Returns:
        str: A confirmation message that the order was placed.
    """
    # In a real app, this would call an API. We'll just return a success message.
    confirmation = f"Success! Order placed for one {size} {crust} crust pizza with {', '.join(toppings)}."
    return confirmation